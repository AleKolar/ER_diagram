# src/library_models
"""
Модели SQLAlchemy для библиотечной системы с русскими комментариями
"""
from sqlalchemy import String, ForeignKey, DateTime, Text, Integer, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from src.database.er_db import Model
from typing import Optional, List


class Catalog(Model):
    """Каталог книг"""
    __tablename__ = 'catalogs'
    __table_args__ = {'comment': 'Каталоги книг'}

    catalog_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True,
        comment='Уникальный идентификатор каталога'
    )
    name: Mapped[str] = mapped_column(
        String(200), nullable=False,
        comment='Название каталога'
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, comment='Описание каталога'
    )
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey('catalogs.catalog_id'),
        nullable=True,
        comment='Ссылка на родительский каталог (для иерархии)'
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, server_default=func.now(),
        comment='Дата и время создания записи'
    )

    books: Mapped[List['Book']] = relationship(
        'Book', back_populates='catalog', cascade='all, delete-orphan'
    )
    parent: Mapped[Optional['Catalog']] = relationship(
        'Catalog', remote_side=[catalog_id], back_populates='children'
    )
    children: Mapped[List['Catalog']] = relationship(
        'Catalog', back_populates='parent'
    )


class Book(Model):
    """Книга (метаданные)"""
    __tablename__ = 'books'
    __table_args__ = {'comment': 'Книги (основные метаданные)'}

    book_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True,
        comment='Уникальный идентификатор книги'
    )
    title: Mapped[str] = mapped_column(
        String(500), nullable=False,
        comment='Название книги'
    )
    author: Mapped[str] = mapped_column(
        String(300), nullable=False,
        comment='Автор книги'
    )
    year: Mapped[Optional[int]] = mapped_column(
        Integer, comment='Год издания книги'
    )
    catalog_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('catalogs.catalog_id'), nullable=False,
        comment='Ссылка на каталог, к которому относится книга'
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, comment='Описание книги (аннотация)'
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, server_default=func.now(),
        comment='Дата и время создания записи'
    )

    catalog: Mapped['Catalog'] = relationship('Catalog', back_populates='books')
    copies: Mapped[List['BookCopy']] = relationship(
        'BookCopy', back_populates='book', cascade='all, delete-orphan'
    )


class BookCopy(Model):
    """Физический экземпляр книги"""
    __tablename__ = 'book_copies'
    __table_args__ = {'comment': 'Физические экземпляры книг'}

    copy_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True,
        comment='Уникальный идентификатор экземпляра книги'
    )
    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('books.book_id'), nullable=False,
        comment='Ссылка на книгу, к которой относится экземпляр'
    )
    inventory_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False,
        comment='Инвентарный номер экземпляра (уникальный)'
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, server_default=func.now(),
        comment='Дата и время создания записи'
    )

    book: Mapped['Book'] = relationship('Book', back_populates='copies')
    issues: Mapped[List['Issue']] = relationship('Issue', back_populates='book_copy')


class Reader(Model):
    """Читатель библиотеки"""
    __tablename__ = 'readers'
    __table_args__ = {'comment': 'Читатели библиотеки'}

    reader_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True,
        comment='Уникальный идентификатор читателя'
    )
    full_name: Mapped[str] = mapped_column(
        String(200), nullable=False,
        comment='Фамилия, имя и отчество читателя'
    )
    address: Mapped[Optional[str]] = mapped_column(
        String(500), comment='Адрес проживания читателя'
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(20), comment='Контактный телефон читателя'
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(100), comment='Электронная почта читателя'
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, server_default=func.now(),
        comment='Дата и время регистрации читателя'
    )

    issues: Mapped[List['Issue']] = relationship('Issue', back_populates='reader')


class Employee(Model):
    """Сотрудник библиотеки"""
    __tablename__ = 'employees'
    __table_args__ = {'comment': 'Сотрудники библиотеки'}

    employee_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True,
        comment='Уникальный идентификатор сотрудника'
    )
    full_name: Mapped[str] = mapped_column(
        String(200), nullable=False,
        comment='Фамилия, имя и отчество сотрудника'
    )
    position: Mapped[str] = mapped_column(
        String(100), nullable=False,
        comment='Должность сотрудника'
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(20), comment='Контактный телефон сотрудника'
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(100), comment='Электронная почта сотрудника'
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, server_default=func.now(),
        comment='Дата и время приема сотрудника на работу'
    )

    issued_issues: Mapped[List['Issue']] = relationship(
        'Issue', foreign_keys='Issue.employee_issued_id', back_populates='issued_by'
    )
    received_issues: Mapped[List['Issue']] = relationship(
        'Issue', foreign_keys='Issue.employee_received_id', back_populates='received_by'
    )


class Issue(Model):
    """Выдача книги читателю"""
    __tablename__ = 'issues'
    __table_args__ = {'comment': 'Выдачи книг читателям'}

    issue_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True,
        comment='Уникальный идентификатор выдачи'
    )
    copy_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('book_copies.copy_id'), nullable=False,
        comment='Ссылка на экземпляр книги, который выдается'
    )
    reader_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('readers.reader_id'), nullable=False,
        comment='Ссылка на читателя, которому выдается книга'
    )
    employee_issued_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('employees.employee_id'), nullable=False,
        comment='Ссылка на сотрудника, который оформил выдачу'
    )
    employee_received_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey('employees.employee_id'), nullable=True,
        comment='Ссылка на сотрудника, который принял книгу обратно'
    )
    issue_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False,
        comment='Дата и время выдачи книги'
    )
    due_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False,
        comment='Дата, до которой книга должна быть возвращена'
    )
    return_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True,
        comment='Фактическая дата возврата книги'
    )
    copies_count: Mapped[int] = mapped_column(
        Integer, default=1, nullable=False,
        comment='Количество выданных экземпляров (по умолчанию 1)'
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, server_default=func.now(),
        comment='Дата и время создания записи'
    )

    book_copy: Mapped['BookCopy'] = relationship('BookCopy', back_populates='issues')
    reader: Mapped['Reader'] = relationship('Reader', back_populates='issues')
    issued_by: Mapped['Employee'] = relationship(
        'Employee', foreign_keys=[employee_issued_id], back_populates='issued_issues'
    )
    received_by: Mapped[Optional['Employee']] = relationship(
        'Employee', foreign_keys=[employee_received_id], back_populates='received_issues'
    )