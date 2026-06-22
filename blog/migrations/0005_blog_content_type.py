from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blog_meta_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='content_type',
            field=models.CharField(
                choices=[('blog', 'Blog'), ('case_study', 'Case Study')],
                default='blog',
                max_length=20,
            ),
        ),
    ]
