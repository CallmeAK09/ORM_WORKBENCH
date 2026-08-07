from django.db import connection, transaction, IntegrityError

from applications.compiler.models import Author, Book, Library


def reset_default_tables(env=None):
    vendor = connection.vendor             #Default db backend

    tables = [
        'compiler_library_books',
        'compiler_library',
        'compiler_book',
        'compiler_author',
    ]

    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                if vendor == 'postgresql':
                    cursor.execute(f"TRUNCATE TABLE {', '.join(tables)} RESTART IDENTITY CASCADE;")
                else:
                    for table in tables:
                        cursor.execute(f"DELETE FROM {table};")
                
            # Authors
            a1 = Author.objects.create(
                name='J.K. Rowling',
                email='jk@example.com',
                bio='British author best known for the Harry Potter series.'
            )

            a2 = Author.objects.create(
                name='George R.R. Martin',
                email='grrm@example.com',
                bio='American novelist famous for A Song of Ice and Fire.'
            )

            a3 = Author.objects.create(
                name='J.R.R. Tolkien',
                email='jrrt@example.com',
                bio='English writer known for The Hobbit and The Lord of the Rings.'
            )

            a4 = Author.objects.create(
                name='Stephen King',
                email='sking@example.com',
                bio='American author renowned for horror and supernatural fiction.'
            )

            a5 = Author.objects.create(
                name='Agatha Christie',
                email='agatha@example.com',
                bio='English writer celebrated for her detective and mystery novels.'
            )

            # Books (FK → Author)
            b1 = Book.objects.create(title='Harry Potter',              isbn='9780747532699', author=a1, pages=223, published_date='1997-06-26', language='English')
            b2 = Book.objects.create(title='Game of Thrones',           isbn='9780553103540', author=a2, pages=694, published_date='1996-08-01', language='English')
            b3 = Book.objects.create(title='The Hobbit',                isbn='9780261102217', author=a3, pages=310, published_date='1937-09-21', language='English')
            b4 = Book.objects.create(title='The Shining',               isbn='9780385121675', author=a4, pages=447, published_date='1977-01-28', language='English')
            b5 = Book.objects.create(title='And Then There Were None',  isbn='9780007136834', author=a2, pages=272, published_date='1939-11-06', language='English')

            # Libraries (M2M ↔ Book)
            l1 = Library.objects.create(name='Central Library',    location='New York',  established_at='1895-03-15')
            l2 = Library.objects.create(name='Community Library',  location='London',    established_at='1922-07-04')
            l3 = Library.objects.create(name='University Library', location='Boston',    established_at='1948-09-01')
            l4 = Library.objects.create(name='State Library',      location='Sydney',    established_at='1869-11-20')
            l5 = Library.objects.create(name='National Library',   location='Toronto',   established_at='1953-05-12')

            l1.books.set([b1, b2, b3])
            l2.books.set([b3, b5, b1])
            l3.books.set([b4, b1])
            l4.books.set([b2, b3])
            l5.books.set([b5, b4])
    except IntegrityError:
        pass


def drop_temp_tables():
    vendor = connection.vendor

    default_tables = {
        'compiler_author',
        'compiler_book',
        'compiler_library',
        'compiler_library_books',
        'django_migrations',
        'django_content_type',
        'django_session',
        'auth_permission',
        'auth_group',
        'auth_group_permissions',
        'auth_user',
        'auth_user_groups',
        'auth_user_user_permissions',
        'django_admin_log'
    }

    with connection.cursor() as cursor:
        all_tables = connection.introspection.table_names(cursor)
        for table in all_tables:
            if table.startswith('compiler_') and table not in default_tables:
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                except Exception:
                    cursor.execute(f"DROP TABLE IF EXISTS {table};")