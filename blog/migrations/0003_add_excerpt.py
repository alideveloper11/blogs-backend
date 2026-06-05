from django.db import migrations, connection


def add_excerpt_if_not_exists(apps, schema_editor):
    vendor = schema_editor.connection.vendor
    with connection.cursor() as cursor:
        if vendor == 'sqlite':
            cursor.execute("PRAGMA table_info(blog_blog)")
            columns = [row[1] for row in cursor.fetchall()]
            exists = 'excerpt' in columns
        else:
            cursor.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='blog_blog' AND column_name='excerpt'
            """)
            exists = cursor.fetchone() is not None

        if not exists:
            cursor.execute("ALTER TABLE blog_blog ADD COLUMN excerpt TEXT NOT NULL DEFAULT ''")


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blog_content'),
    ]

    operations = [
        migrations.RunPython(add_excerpt_if_not_exists, migrations.RunPython.noop),
    ]
