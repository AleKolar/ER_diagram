# src/schemas/library_schemas
"""
Pydantic схемы для библиотечной системы с русскими комментариями
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


# Базовые схемы
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


# Схемы для Каталога
class CatalogBase(BaseSchema):
    name: str = Field(
        ...,
        max_length=200,
        description="Название каталога"
    )
    description: Optional[str] = Field(
        None,
        description="Описание каталога"
    )
    parent_id: Optional[int] = Field(
        None,
        description="Идентификатор родительского каталога (для иерархии)"
    )


class CatalogCreate(CatalogBase):
    pass


class CatalogUpdate(BaseSchema):
    name: Optional[str] = Field(
        None,
        max_length=200,
        description="Название каталога"
    )
    description: Optional[str] = Field(
        None,
        description="Описание каталога"
    )
    parent_id: Optional[int] = Field(
        None,
        description="Идентификатор родительского каталога"
    )


class Catalog(CatalogBase):
    catalog_id: int = Field(
        ...,
        description="Уникальный идентификатор каталога"
    )
    created_at: datetime = Field(
        ...,
        description="Дата и время создания записи"
    )
    books_count: Optional[int] = Field(
        None,
        description="Количество книг в каталоге"
    )
    children: List['Catalog'] = Field(
        default_factory=list,
        description="Дочерние каталоги"
    )


# Схемы для Книги
class BookBase(BaseSchema):
    title: str = Field(
        ...,
        max_length=500,
        description="Название книги"
    )
    author: str = Field(
        ...,
        max_length=300,
        description="Автор книги"
    )
    year: Optional[int] = Field(
        None,
        ge=0,
        le=2100,
        description="Год издания книги"
    )
    catalog_id: int = Field(
        ...,
        description="Идентификатор каталога, к которому относится книга"
    )
    description: Optional[str] = Field(
        None,
        description="Описание книги (аннотация)"
    )


class BookCreate(BookBase):
    copies_count: Optional[int] = Field(
        1,
        ge=1,
        le=100,
        description="Количество экземпляров для создания (по умолчанию 1)"
    )


class BookUpdate(BaseSchema):
    title: Optional[str] = Field(
        None,
        max_length=500,
        description="Название книги"
    )
    author: Optional[str] = Field(
        None,
        max_length=300,
        description="Автор книги"
    )
    year: Optional[int] = Field(
        None,
        ge=0,
        le=2100,
        description="Год издания книги"
    )
    catalog_id: Optional[int] = Field(
        None,
        description="Идентификатор каталога"
    )
    description: Optional[str] = Field(
        None,
        description="Описание книги"
    )


class Book(BookBase):
    book_id: int = Field(
        ...,
        description="Уникальный идентификатор книги"
    )
    created_at: datetime = Field(
        ...,
        description="Дата и время создания записи"
    )
    copies_count: Optional[int] = Field(
        None,
        description="Общее количество экземпляров этой книги"
    )
    available_copies_count: Optional[int] = Field(
        None,
        description="Количество доступных (не выданных) экземпляров"
    )
    catalog: Optional[Catalog] = Field(
        None,
        description="Каталог, к которому относится книга"
    )


# Схемы для Экземпляра книги
class BookCopyBase(BaseSchema):
    book_id: int = Field(
        ...,
        description="Идентификатор книги, к которой относится экземпляр"
    )
    inventory_number: str = Field(
        ...,
        max_length=50,
        description="Инвентарный номер экземпляра (уникальный)"
    )


class BookCopyCreate(BookCopyBase):
    pass


class BookCopyUpdate(BaseSchema):
    inventory_number: Optional[str] = Field(
        None,
        max_length=50,
        description="Инвентарный номер экземпляра"
    )


class BookCopy(BookCopyBase):
    copy_id: int = Field(
        ...,
        description="Уникальный идентификатор экземпляра книги"
    )
    created_at: datetime = Field(
        ...,
        description="Дата и время создания записи"
    )
    book: Optional[Book] = Field(
        None,
        description="Книга, к которой относится экземпляр"
    )
    is_available: Optional[bool] = Field(
        None,
        description="Доступен ли экземпляр для выдачи"
    )
    current_issue: Optional['Issue'] = Field(
        None,
        description="Текущая активная выдача этого экземпляра"
    )


# Схемы для Читателя
class ReaderBase(BaseSchema):
    full_name: str = Field(
        ...,
        max_length=200,
        description="Фамилия, имя и отчество читателя"
    )
    address: Optional[str] = Field(
        None,
        max_length=500,
        description="Адрес проживания читателя"
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Контактный телефон читателя"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Электронная почта читателя"
    )


class ReaderCreate(ReaderBase):
    pass


class ReaderUpdate(BaseSchema):
    full_name: Optional[str] = Field(
        None,
        max_length=200,
        description="Фамилия, имя и отчество читателя"
    )
    address: Optional[str] = Field(
        None,
        max_length=500,
        description="Адрес проживания читателя"
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Контактный телефон читателя"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Электронная почта читателя"
    )


class Reader(ReaderBase):
    reader_id: int = Field(
        ...,
        description="Уникальный идентификатор читателя"
    )
    created_at: datetime = Field(
        ...,
        description="Дата и время регистрации читателя"
    )
    active_issues_count: Optional[int] = Field(
        None,
        description="Количество активных выдач у читателя"
    )
    total_issues_count: Optional[int] = Field(
        None,
        description="Общее количество выдач у читателя"
    )


# Схемы для Сотрудника
class EmployeeBase(BaseSchema):
    full_name: str = Field(
        ...,
        max_length=200,
        description="Фамилия, имя и отчество сотрудника"
    )
    position: str = Field(
        ...,
        max_length=100,
        description="Должность сотрудника"
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Контактный телефон сотрудника"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Электронная почта сотрудника"
    )


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseSchema):
    full_name: Optional[str] = Field(
        None,
        max_length=200,
        description="Фамилия, имя и отчество сотрудника"
    )
    position: Optional[str] = Field(
        None,
        max_length=100,
        description="Должность сотрудника"
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Контактный телефон сотрудника"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Электронная почта сотрудника"
    )


class Employee(EmployeeBase):
    employee_id: int = Field(
        ...,
        description="Уникальный идентификатор сотрудника"
    )
    created_at: datetime = Field(
        ...,
        description="Дата и время приема сотрудника на работу"
    )
    issued_count: Optional[int] = Field(
        None,
        description="Количество оформленных выдач"
    )
    received_count: Optional[int] = Field(
        None,
        description="Количество принятых возвратов"
    )


# Схемы для Выдачи
class IssueBase(BaseSchema):
    copy_id: int = Field(
        ...,
        description="Идентификатор экземпляра книги для выдачи"
    )
    reader_id: int = Field(
        ...,
        description="Идентификатор читателя, которому выдается книга"
    )
    employee_issued_id: int = Field(
        ...,
        description="Идентификатор сотрудника, оформляющего выдачу"
    )
    due_date: datetime = Field(
        ...,
        description="Дата, до которой книга должна быть возвращена"
    )
    copies_count: int = Field(
        1,
        ge=1,
        description="Количество выданных экземпляров (по умолчанию 1)"
    )


class IssueCreate(IssueBase):
    pass


class IssueUpdate(BaseSchema):
    employee_received_id: Optional[int] = Field(
        None,
        description="Идентификатор сотрудника, принявшего книгу обратно"
    )
    return_date: Optional[datetime] = Field(
        None,
        description="Фактическая дата возврата книги"
    )
    copies_count: Optional[int] = Field(
        None,
        ge=1,
        description="Количество выданных экземпляров"
    )


class IssueReturn(BaseSchema):
    employee_received_id: int = Field(
        ...,
        description="Идентификатор сотрудника, принимающего книгу"
    )
    return_date: Optional[datetime] = Field(
        None,
        description="Дата возврата (по умолчанию текущая дата)"
    )


class IssueExtend(BaseSchema):
    new_due_date: datetime = Field(
        ...,
        description="Новая дата возврата (продление срока)"
    )
    employee_issued_id: Optional[int] = Field(
        None,
        description="Идентификатор сотрудника, продлевающего срок"
    )


class Issue(IssueBase):
    issue_id: int = Field(
        ...,
        description="Уникальный идентификатор выдачи"
    )
    employee_received_id: Optional[int] = Field(
        None,
        description="Идентификатор сотрудника, принявшего книгу обратно"
    )
    issue_date: datetime = Field(
        ...,
        description="Дата и время выдачи книги"
    )
    return_date: Optional[datetime] = Field(
        None,
        description="Фактическая дата возврата книги"
    )
    created_at: datetime = Field(
        ...,
        description="Дата и время создания записи"
    )

    # Вложенные объекты
    book_copy: Optional[BookCopy] = Field(
        None,
        description="Экземпляр книги, который был выдан"
    )
    reader: Optional[Reader] = Field(
        None,
        description="Читатель, которому выдана книга"
    )
    issued_by: Optional[Employee] = Field(
        None,
        description="Сотрудник, оформивший выдачу"
    )
    received_by: Optional[Employee] = Field(
        None,
        description="Сотрудник, принявший книгу обратно"
    )

    # Вычисляемые поля
    is_returned: bool = Field(
        False,
        description="Возвращена ли книга (вычисляется по return_date)"
    )
    is_overdue: Optional[bool] = Field(
        None,
        description="Просрочена ли выдача (вычисляется по due_date)"
    )


# Схемы для статистики
class Statistics(BaseSchema):
    total_books: int = Field(
        ...,
        description="Общее количество книг в библиотеке"
    )
    total_readers: int = Field(
        ...,
        description="Общее количество читателей"
    )
    total_employees: int = Field(
        ...,
        description="Общее количество сотрудников"
    )
    active_issues: int = Field(
        ...,
        description="Количество активных (не возвращенных) выдач"
    )
    overdue_issues: int = Field(
        ...,
        description="Количество просроченных выдач"
    )
    books_by_catalog: List[dict] = Field(
        default_factory=list,
        description="Статистика по книгам в разрезе каталогов"
    )
    popular_books: List[dict] = Field(
        default_factory=list,
        description="Самые популярные книги (по количеству выдач)"
    )
    active_readers: List[dict] = Field(
        default_factory=list,
        description="Самые активные читатели"
    )


# Схемы для поиска
class SearchQuery(BaseSchema):
    query: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Поисковый запрос"
    )
    search_in: List[str] = Field(
        ["title", "author"],
        description="Поля для поиска: title (название), author (автор)"
    )
    limit: Optional[int] = Field(
        20,
        ge=1,
        le=100,
        description="Количество результатов (по умолчанию 20)"
    )
    offset: Optional[int] = Field(
        0,
        ge=0,
        description="Смещение для пагинации (по умолчанию 0)"
    )


# Схемы для фильтрации
class BookFilter(BaseSchema):
    catalog_id: Optional[int] = Field(
        None,
        description="Фильтр по каталогу"
    )
    author: Optional[str] = Field(
        None,
        description="Фильтр по автору"
    )
    year_from: Optional[int] = Field(
        None,
        ge=0,
        description="Год издания (от)"
    )
    year_to: Optional[int] = Field(
        None,
        ge=0,
        description="Год издания (до)"
    )
    available_only: Optional[bool] = Field(
        False,
        description="Только книги с доступными экземплярами"
    )


class IssueFilter(BaseSchema):
    reader_id: Optional[int] = Field(
        None,
        description="Фильтр по читателю"
    )
    employee_issued_id: Optional[int] = Field(
        None,
        description="Фильтр по сотруднику, выдавшему книгу"
    )
    is_returned: Optional[bool] = Field(
        None,
        description="Фильтр по статусу возврата"
    )
    is_overdue: Optional[bool] = Field(
        None,
        description="Фильтр по просроченным выдачам"
    )
    date_from: Optional[datetime] = Field(
        None,
        description="Дата выдачи (от)"
    )
    date_to: Optional[datetime] = Field(
        None,
        description="Дата выдачи (до)"
    )


# Схема для импорта данных
class ImportData(BaseSchema):
    books: Optional[List[BookCreate]] = Field(
        None,
        description="Список книг для импорта"
    )
    readers: Optional[List[ReaderCreate]] = Field(
        None,
        description="Список читателей для импорта"
    )
    employees: Optional[List[EmployeeCreate]] = Field(
        None,
        description="Список сотрудников для импорта"
    )


# Разрешаем forward references
Catalog.model_rebuild()
Book.model_rebuild()
BookCopy.model_rebuild()
Reader.model_rebuild()
Employee.model_rebuild()
Issue.model_rebuild()