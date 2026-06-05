from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_add_excerpt'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='meta_title',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='blog',
            name='meta_description',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='blog',
            name='schema',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
    ]
