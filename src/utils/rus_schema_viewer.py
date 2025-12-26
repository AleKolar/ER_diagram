"""
Утилита для просмотра схемы БД с русскими комментариями
"""
from sqlalchemy import inspect
from src.database.er_db import engine
import asyncio


async def print_russian_schema():
    """Вывести схему БД с русскими комментариями"""

    async with engine.connect() as conn:
        inspector = inspect(conn.sync_connection)

        print("=" * 80)
        print("СХЕМА БАЗЫ ДАННЫХ БИБЛИОТЕКИ")
        print("=" * 80)

        # Получаем все таблицы
        tables = inspector.get_table_names()

        for table_name in tables:
            # Получаем комментарий таблицы
            table_comment = inspector.get_table_comment(table_name)
            rus_table_name = table_comment.get('text', table_name) if table_comment else table_name

            print(f"\n📚 Таблица: {table_name}")
            if rus_table_name and rus_table_name != table_name:
                print(f"   📝 Русское название: {rus_table_name}")

            # Получаем колонки
            columns = inspector.get_columns(table_name)

            print(f"   📊 Колонки ({len(columns)}):")
            for col in columns:
                col_name = col['name']
                col_type = str(col['type'])
                col_comment = col.get('comment', '')

                print(f"      • {col_name} ({col_type})", end="")
                if col_comment:
                    print(f" → {col_comment}")
                else:
                    print()

            # Получаем индексы
            indexes = inspector.get_indexes(table_name)
            if indexes:
                print(f"   🔑 Индексы ({len(indexes)}):")
                for idx in indexes:
                    idx_name = idx['name']
                    idx_cols = ', '.join(idx['column_names'])
                    idx_unique = "УНИКАЛЬНЫЙ" if idx.get('unique') else "неуникальный"
                    print(f"      • {idx_name}: {idx_cols} ({idx_unique})")

            # Получаем внешние ключи
            foreign_keys = inspector.get_foreign_keys(table_name)
            if foreign_keys:
                print(f"   🔗 Внешние ключи ({len(foreign_keys)}):")
                for fk in foreign_keys:
                    fk_cols = ', '.join(fk['constrained_columns'])
                    ref_table = fk['referred_table']
                    ref_cols = ', '.join(fk['referred_columns'])
                    print(f"      • {fk_cols} → {ref_table}({ref_cols})")

            print("-" * 80)


if __name__ == "__main__":
    asyncio.run(print_russian_schema())