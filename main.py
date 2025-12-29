"""
Основное приложение FastAPI для библиотечной системы
"""

import logging
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.endpoints.books import books, books_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Запуск приложения...")
    yield
    logger.info("👋 Остановка приложения...")


app = FastAPI(
    title="Библиотечная система",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(books_router)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="src/templates")

@app.get("/", tags=["Главная"])
async def root():
    return {"message": "Добро пожаловать в библиотечную систему API"}


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Главная страница библиотечной системы
    Возвращает HTML шаблон с примерными данными для демонстрации
    """
    # Данные для демонстрации (примерные)
    context = {
        "request": request,
        "current_year": datetime.now().year
    }

    return templates.TemplateResponse("dashboard.html", context)

@app.get("/users_dashboard", response_class=HTMLResponse)
async def users_dashboard(request: Request):
    """
    Главная страница библиотечной системы
    Возвращает HTML шаблон с примерными данными для демонстрации
    """
    # Данные для демонстрации (примерные)
    context = {
        "request": request,
        "current_year": datetime.now().year
    }

    return templates.TemplateResponse("users_dashboard.html", context)




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



print("🔍 Зарегистрированные пути:")
for route in app.routes:
    if hasattr(route, 'path'):
        methods = getattr(route, 'methods', ['?'])
        print(f"  {methods} {route.path}")

# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

# uvicorn main:app --reload --port 8001
# uvicorn main:app --reload --port 8000

# sqlalchemy.url = postgresql+asyncpg://postgres:password@localhost:5432/er_db

