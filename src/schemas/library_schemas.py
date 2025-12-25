# src/schemas/library_schemas
"""
Pydantic схемы для валидации данных библиотечной системы
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


# Базовые схемы
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


# Схемы для Каталога
class CatalogBase(BaseSchema):
    name: str = Field(..., max_length=200, description="Название каталога")
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CatalogCreate(CatalogBase):
    pass


class CatalogUpdate(CatalogBase):
    name: Optional[str] = Field(None, max_length=200)


class Catalog(CatalogBase):
    catalog_id: int
    children: List['Catalog'] = []
    books_count: Optional[int] = None


# Схемы для Книги
class BookBase(BaseSchema):
    title: str = Field(..., max_length=500, description="Название книги")
    author: str = Field(..., max_length=300, description="Автор")
    year: Optional[int] = Field(None, ge=0, le=2100, description="Год издания")
    catalog_id: int = Field(..., description="ID каталога")
    description: Optional[str] = None
    isbn: Optional[str] = Field(None, max_length=13, description="ISBN")


class BookCreate(BookBase):
    copies_count: Optional[int] = Field(1, ge=1, le=100, description="Количество экземпляров для создания")


class BookUpdate(BaseSchema):
    title: Optional[str] = Field(None, max_length=500)
    author: Optional[str] = Field(None, max_length=300)
    year: Optional[int] = Field(None, ge=0, le=2100)
    catalog_id: Optional[int] = None
    description: Optional[str] = None
    isbn: Optional[str] = Field(None, max_length=13)


class Book(BookBase):
    book_id: int
    created_at: datetime
    copies_count: Optional[int] = None
    available_copies_count: Optional[int] = None
    catalog: Optional[Catalog] = None


# Схемы для Экземпляра книги
class BookCopyBase(BaseSchema):
    book_id: int
    inventory_number: str = Field(..., max_length=50, description="Инвентарный номер")
    barcode: Optional[str] = Field(None, max_length=100, description="Штрих-код")
    acquired_date: Optional[date] = None


class BookCopyCreate(BookCopyBase):
    status: Optional[str] = Field("available", description="Статус экземпляра")


class BookCopyUpdate(BaseSchema):
    status: Optional[str] = None
    barcode: Optional[str] = Field(None, max_length=100)
    acquired_date: Optional[date] = None


class BookCopyStatus(str, Enum):
    AVAILABLE = "available"
    ISSUED = "issued"
    LOST = "lost"
    REPAIR = "repair"


class BookCopy(BookCopyBase):
    copy_id: int
    status: BookCopyStatus
    created_at: datetime
    book: Optional[Book] = None


# Схемы для Читателя
class ReaderBase(BaseSchema):
    full_name: str = Field(..., max_length=200, description="ФИО читателя")
    address: Optional[str] = Field(None, max_length=500)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    passport_data: Optional[str] = Field(None, max_length=100)


class ReaderCreate(ReaderBase):
    is_active: Optional[bool] = True


class ReaderUpdate(BaseSchema):
    full_name: Optional[str] = Field(None, max_length=200)
    address: Optional[str] = Field(None, max_length=500)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    passport_data: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class Reader(ReaderBase):
    reader_id: int
    registration_date: date
    is_active: bool
    active_issues_count: Optional[int] = None


# Схемы для Сотрудника
class EmployeeRole(str, Enum):
    ADMIN = "admin"
    LIBRARIAN = "librarian"


class EmployeeBase(BaseSchema):
    full_name: str = Field(..., max_length=200, description="ФИО сотрудника")
    position: str = Field(..., max_length=100, description="Должность")
    phone: Optional[str] = Field(None, max_length=20)
    email: EmailStr
    role: EmployeeRole = EmployeeRole.LIBRARIAN


class EmployeeCreate(EmployeeBase):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, description="Пароль")


class EmployeeUpdate(BaseSchema):
    full_name: Optional[str] = Field(None, max_length=200)
    position: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    role: Optional[EmployeeRole] = None
    is_active: Optional[bool] = None


class EmployeeLogin(BaseSchema):
    username: str
    password: str


class Employee(EmployeeBase):
    employee_id: int
    hire_date: date
    is_active: bool
    username: str


class EmployeeWithToken(Employee):
    access_token: str


# Схемы для Выдачи
class IssueBase(BaseSchema):
    copy_id: int
    reader_id: int
    book_id: int
    due_date: date
    notes: Optional[str] = None


class IssueCreate(IssueBase):
    pass


class IssueUpdate(BaseSchema):
    return_date: Optional[date] = None
    is_returned: Optional[bool] = None
    is_extended: Optional[bool] = None
    notes: Optional[str] = None


class IssueReturn(BaseSchema):
    employee_received_id: int


class IssueExtend(BaseSchema):
    new_due_date: date


class Issue(IssueBase):
    issue_id: int
    employee_issued_id: int
    employee_received_id: Optional[int] = None
    issue_date: date
    return_date: Optional[date] = None
    is_returned: bool
    is_extended: bool
    created_at: datetime

    # Вложенные объекты
    book_copy: Optional[BookCopy] = None
    reader: Optional[Reader] = None
    issued_by: Optional[Employee] = None
    received_by: Optional[Employee] = None
    book: Optional[Book] = None


# Схемы для статистики
class Statistics(BaseSchema):
    total_books: int
    total_readers: int
    total_employees: int
    active_issues: int
    overdue_issues: int
    books_by_catalog: List[dict] = []


# Схемы для поиска
class SearchQuery(BaseSchema):
    query: str = Field(..., min_length=1, max_length=100)
    search_in: List[str] = Field(["title", "author"], description="Где искать: title, author, isbn")


# Разрешаем forward references
Catalog.model_rebuild()
Book.model_rebuild()