# tests/test_books.py
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import Book


# Фикстура setup_database в conftest автоматически создала таблицы

@pytest.mark.asyncio
async def test_database_connection(db_session: AsyncSession):
    """Проверяем, что БД работает и таблицы созданы."""
    # Простой запрос для проверки
    result = await db_session.execute(text("SELECT 1"))
    value = result.scalar()
    assert value == 1
    print("✓ База данных подключена корректно")

@pytest.mark.asyncio
async def test_tables_created(db_session: AsyncSession):
    """Проверяем, что таблицы созданы в БД."""
    # Проверяем существование таблиц через системные таблицы SQLite
    result = await db_session.execute(
        text("SELECT name FROM sqlite_master WHERE type='table'")
    )
    tables = result.fetchall()

    # Выводим список таблиц для отладки
    table_names = [table[0] for table in tables]
    print(f"✓ Найдены таблицы: {table_names}")

    # Проверяем, что есть хотя бы одна таблица
    assert len(tables) > 0


@pytest.mark.asyncio
async def test_create_book(db_session: AsyncSession):
    """Тест создания книги."""
    # Создаем новую книгу
    new_book = Book(title="Test Book", author="Test Author")
    db_session.add(new_book)
    await db_session.commit()

    # Проверяем, что книга создана
    book = await db_session.get(Book, new_book.id)
    assert book is not None
    assert book.title == "Test Book"

