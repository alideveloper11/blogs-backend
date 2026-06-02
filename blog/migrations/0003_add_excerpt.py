from django.db import migrations, models, connection


def add_excerpt_if_not_exists(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='blog_blog' AND column_name='excerpt'
        """)
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE blog_blog ADD COLUMN excerpt TEXT NOT NULL DEFAULT ''")


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blog_content'),
    ]

    operations = [
        migrations.RunPython(add_excerpt_if_not_exists, migrations.RunPython.noop),
    ]
