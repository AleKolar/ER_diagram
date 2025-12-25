# src/library_models
"""
Модели SQLAlchemy для библиотечной системы (SQLAlchemy 2.0 style)
"""
from sqlalchemy import String, ForeignKey, Date, DateTime, Text, Boolean, func, Integer
from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
from datetime import datetime
from src.database.er_db import Model
from typing import Optional, List


class Catalog(Model):
    """Каталог книг"""
    __tablename__ = 'catalogs'

    catalog_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment='Название каталога')
    description: Mapped[Optional[str]] = mapped_column(Text, comment='Описание каталога')
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('catalogs.catalog_id'),
        nullable=True,
        comment='Родительский каталог'
    )

    # Связи
    books: Mapped[List['Book']] = relationship(
        'Book',
        back_populates='catalog',
        cascade='all, delete-orphan'
    )
    parent: Mapped[Optional['Catalog']] = relationship(
        'Catalog',
        remote_side=[catalog_id],
        back_populates='children'
    )
    children: Mapped[List['Catalog']] = relationship(
        'Catalog',
        back_populates='parent'
    )

    def __repr__(self) -> str:
        return f'<Catalog {self.catalog_id}: {self.name}>'


class Book(Model):
    """Книга (метаданные)"""
    __tablename__ = 'books'

    book_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, comment='Название книги')
    author: Mapped[str] = mapped_column(String(300), nullable=False, comment='Автор')
    year: Mapped[Optional[int]] = mapped_column(Integer, comment='Год издания')
    catalog_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('catalogs.catalog_id'),
        nullable=False,
        comment='Каталог'
    )
    description: Mapped[Optional[str]] = mapped_column(Text, comment='Описание книги')
    isbn: Mapped[Optional[str]] = mapped_column(String(13), unique=True, comment='ISBN')
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        server_default=func.now()
    )

    # Связи
    catalog: Mapped['Catalog'] = relationship('Catalog', back_populates='books')
    copies: Mapped[List['BookCopy']] = relationship(
        'BookCopy',
        back_populates='book',
        cascade='all, delete-orphan'
    )
    issues: Mapped[List['Issue']] = relationship('Issue', back_populates='book')

    @validates('year')
    def validate_year(self, key: str, year: Optional[int]) -> Optional[int]:
        if year and (year < 0 or year > datetime.now().year + 1):
            raise ValueError('Некорректный год издания')
        return year

    def __repr__(self) -> str:
        return f'<Book {self.book_id}: {self.title}>'


class BookCopy(Model):
    """Экземпляр книги"""
    __tablename__ = 'book_copies'

    copy_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('books.book_id'),
        nullable=False,
        comment='Книга'
    )
    inventory_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment='Инвентарный номер'
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default='available',
        comment='Статус: available, issued, lost, repair'
    )
    barcode: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        comment='Штрих-код'
    )
    acquired_date: Mapped[Optional[datetime]] = mapped_column(Date, comment='Дата поступления')
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        server_default=func.now()
    )

    # Связи
    book: Mapped['Book'] = relationship('Book', back_populates='copies')
    issues: Mapped[List['Issue']] = relationship('Issue', back_populates='book_copy')

    def __repr__(self) -> str:
        return f'<BookCopy {self.copy_id}: {self.inventory_number}>'


class Reader(Model):
    """Читатель"""
    __tablename__ = 'readers'

    reader_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment='ФИО читателя'
    )
    address: Mapped[Optional[str]] = mapped_column(String(500), comment='Адрес')
    phone: Mapped[Optional[str]] = mapped_column(String(20), comment='Телефон')
    email: Mapped[Optional[str]] = mapped_column(String(100), unique=True, comment='Email')
    passport_data: Mapped[Optional[str]] = mapped_column(String(100), comment='Паспортные данные')
    registration_date: Mapped[datetime] = mapped_column(
        Date,
        default=datetime.now,
        server_default=func.now()
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        comment='Активен ли читатель'
    )

    # Связи
    issues: Mapped[List['Issue']] = relationship('Issue', back_populates='reader')

    @validates('email')
    def validate_email(self, key: str, email: Optional[str]) -> Optional[str]:
        if email and '@' not in email:
            raise ValueError('Некорректный email')
        return email

    def __repr__(self) -> str:
        return f'<Reader {self.reader_id}: {self.full_name}>'


class Employee(Model):
    """Сотрудник библиотеки"""
    __tablename__ = 'employees'

    employee_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment='ФИО сотрудника'
    )
    position: Mapped[str] = mapped_column(String(100), nullable=False, comment='Должность')
    phone: Mapped[Optional[str]] = mapped_column(String(20), comment='Телефон')
    email: Mapped[str] = mapped_column(String(100), unique=True, comment='Email')
    hire_date: Mapped[datetime] = mapped_column(
        Date,
        default=datetime.now,
        comment='Дата приема на работу'
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        comment='Активен ли сотрудник'
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, comment='Логин для входа')
    password_hash: Mapped[Optional[str]] = mapped_column(String(200), comment='Хеш пароля')
    role: Mapped[str] = mapped_column(
        String(20),
        default='librarian',
        comment='Роль: admin, librarian'
    )

    # Связи
    issued_issues: Mapped[List['Issue']] = relationship(
        'Issue',
        foreign_keys='Issue.employee_issued_id',
        back_populates='issued_by'
    )
    received_issues: Mapped[List['Issue']] = relationship(
        'Issue',
        foreign_keys='Issue.employee_received_id',
        back_populates='received_by'
    )

    @validates('role')
    def validate_role(self, key: str, role: str) -> str:
        valid_roles = ['admin', 'librarian']
        if role not in valid_roles:
            raise ValueError(f'Роль должна быть одной из: {valid_roles}')
        return role

    def __repr__(self) -> str:
        return f'<Employee {self.employee_id}: {self.full_name}>'


class Issue(Model):
    """Выдача книги"""
    __tablename__ = 'issues'

    issue_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    copy_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('book_copies.copy_id'),
        nullable=False,
        comment='Экземпляр книги'
    )
    reader_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('readers.reader_id'),
        nullable=False,
        comment='Читатель'
    )
    employee_issued_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('employees.employee_id'),
        nullable=False,
        comment='Сотрудник, выдавший книгу'
    )
    employee_received_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('employees.employee_id'),
        nullable=True,
        comment='Сотрудник, принявший книгу'
    )
    book_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('books.book_id'),
        nullable=False,
        comment='Книга (для удобства)'
    )
    issue_date: Mapped[datetime] = mapped_column(
        Date,
        default=datetime.now,
        nullable=False,
        comment='Дата выдачи'
    )
    due_date: Mapped[datetime] = mapped_column(Date, nullable=False, comment='Срок возврата')
    return_date: Mapped[Optional[datetime]] = mapped_column(
        Date,
        nullable=True,
        comment='Дата фактического возврата'
    )
    is_returned: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment='Возвращена ли книга'
    )
    is_extended: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment='Продлена ли книга'
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, comment='Примечания')
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        server_default=func.now()
    )

    # Связи
    book_copy: Mapped['BookCopy'] = relationship('BookCopy', back_populates='issues')
    reader: Mapped['Reader'] = relationship('Reader', back_populates='issues')
    issued_by: Mapped['Employee'] = relationship(
        'Employee',
        foreign_keys=[employee_issued_id],
        back_populates='issued_issues'
    )
    received_by: Mapped[Optional['Employee']] = relationship(
        'Employee',
        foreign_keys=[employee_received_id],
        back_populates='received_issues'
    )
    book: Mapped['Book'] = relationship('Book', back_populates='issues')

    @validates('due_date')
    def validate_due_date(self, key: str, due_date: datetime) -> datetime:
        if due_date and self.issue_date and due_date < self.issue_date:
            raise ValueError('Срок возврата не может быть раньше даты выдачи')
        return due_date

    def __repr__(self) -> str:
        return f'<Issue {self.issue_id}: Book {self.book_id} to Reader {self.reader_id}>'