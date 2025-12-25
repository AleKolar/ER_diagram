from fastapi import FastAPI

from src.models.library_models import Book, Reader, Employee, Issue

# app = FastAPI()
#
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}


"""
Основное приложение FastAPI для библиотечной системы
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from src.database.er_db import get_db, create_tables

app = FastAPI(
    title="Библиотечная система API",
    version="1.0.0",
    description="API для управления библиотекой"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Регистрация роутеров
# app.include_router(auth.router, prefix="/auth", tags=["Аутентификация"])
# app.include_router(books.router, prefix="/books", tags=["Книги"])
# app.include_router(readers.router, prefix="/readers", tags=["Читатели"])
# app.include_router(employees.router, prefix="/employees", tags=["Сотрудники"])
# app.include_router(issues.router, prefix="/issues", tags=["Выдачи"])
# app.include_router(catalogs.router, prefix="/catalogs", tags=["Каталоги"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл приложения"""
    print("🚀 Запуск приложения...")
    # Создаем таблицы
    try:
        await create_tables()
    except Exception as e:
        print(f"⚠️ Ошибка создания таблиц: {e}")
        raise

    yield

    print("👋 Остановка приложения...")

app = FastAPI(
    title="Library API",
    description="API библиотеки",
    version="1.0.0",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    (CORSMiddleware),
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Главная"])
async def root():
    return {"message": "Добро пожаловать в библиотечную систему API"}


# @app.get("/statistics", response_model=Statistics, tags=["Статистика"])
# async def get_statistics(db: AsyncSession = Depends(get_db)):
#     """Получить статистику библиотеки"""
#     from sqlalchemy import func, select
#
#
#     # Запросы для статистики
#     total_books = await db.scalar(select(func.count()).select_from(Book))
#     total_readers = await db.scalar(select(func.count()).select_from(Reader).where(Reader.is_active == True))
#     total_employees = await db.scalar(select(func.count()).select_from(Employee).where(Employee.is_active == True))
#     active_issues = await db.scalar(select(func.count()).select_from(Issue).where(Issue.is_returned == False))
#
#     # Просроченные выдачи (упрощенно)
#     from datetime import date
#     overdue_issues = await db.scalar(
#         select(func.count()).select_from(Issue)
#         .where(Issue.is_returned == False)
#         .where(Issue.due_date < date.today())
#     )
#
#     return {
#         "total_books": total_books or 0,
#         "total_readers": total_readers or 0,
#         "total_employees": total_employees or 0,
#         "active_issues": active_issues or 0,
#         "overdue_issues": overdue_issues or 0,
#         "books_by_catalog": []
#     }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
