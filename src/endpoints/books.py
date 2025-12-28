from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.database.er_db import get_db
from src.models.library_models import Book, Issue, BookCopy, Catalog
from src.schemas.library_schemas import BookCreate, BookBase

books_router = APIRouter(prefix="/books", tags=["books"])

@books_router.get("/", tags=["books"])
async def books(db: AsyncSession = Depends(get_db)
    ):
    result = await db.execute(select(Book))
    all_books = result.scalars().all()
    return all_books


@books_router.post(
    "/create_book",
    response_model=BookBase,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую книгу",
    description="Создает новую книгу с указанным количеством экземпляров"
)
async def create_book(
        book_data: BookCreate,  # Теперь используем Pydantic модель
        db: AsyncSession = Depends(get_db)
):
    """
    Создать новую книгу

    Параметры:
    - **title**: Название книги (обязательно)
    - **author**: Автор книги (обязательно)
    - **year**: Год издания (опционально)
    - **catalog_id**: ID каталога (обязательно)
    - **description**: Описание книги (опционально)
    - **copies_count**: Количество экземпляров (по умолчанию 1)

    Возвращает:
    - Созданную книгу с информацией о количестве экземпляров
    """

    # 1. Проверяем существование каталога
    catalog_result = await db.execute(
        select(Catalog).where(Catalog.catalog_id == book_data.catalog_id)
    )
    catalog = catalog_result.scalar_one_or_none()

    if not catalog:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Каталог с ID {book_data.catalog_id} не существует"
        )

    # 2. Создаем книгу (исключаем copies_count - это не поле таблицы Book)
    book_dict = book_data.model_dump(exclude={'copies_count'})
    new_book = Book(**book_dict)
    db.add(new_book)
    await db.flush()  # Получаем book_id до commit

    # 3. Создаем указанное количество экземпляров
    copies_count = book_data.copies_count or 1
    copies_created = []

    for i in range(copies_count):
        # Генерируем инвентарный номер: BOOK-{book_id}-{i+1}
        inventory_number = f"BOOK-{new_book.book_id}-{i + 1:03d}"

        copy = BookCopy(
            book_id=new_book.book_id,
            inventory_number=inventory_number
        )
        db.add(copy)
        copies_created.append(copy)

    # 4. Коммитим всё
    await db.commit()

    # 5. Обновляем объект книги
    await db.refresh(new_book)

    # 6. Подгружаем связанные данные
    result = await db.execute(
        select(Book)
        .where(Book.book_id == new_book.book_id)
        .options(selectinload(Book.catalog))
    )
    book_with_relations = result.scalar_one()

    # 7. Считаем экземпляры
    copies_result = await db.execute(
        select(func.count(BookCopy.copy_id))
        .where(BookCopy.book_id == new_book.book_id)
    )
    total_copies = copies_result.scalar()

    # 8. Считаем доступные экземпляры
    available_result = await db.execute(
        select(func.count(BookCopy.copy_id))
        .where(
            BookCopy.book_id == new_book.book_id,
            BookCopy.copy_id.not_in(
                select(Issue.copy_id)
                .where(Issue.return_date.is_(None))
            )
        )
    )
    available_copies = available_result.scalar()

    # 9. Возвращаем с дополнительными полями
    return {
        **book_dict,
        "book_id": book_with_relations.book_id,
        "created_at": book_with_relations.created_at,
        "catalog": catalog,
        "copies_count": total_copies,
        "available_copies_count": available_copies
    }


@books_router.get("/{book_id}", response_model=None, tags=["books"])
async def get_book(
        unique_id: int,
        db: AsyncSession = Depends(get_db)
) -> Book:
    result = await db.execute(
        select(Book).where(Book.book_id == unique_id)
    )
    book = result.scalar()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {unique_id} не найдена"
        )

    return book