from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_content_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('number', models.CharField(max_length=30)),
                ('project_detail', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('website', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_queries', to='blog.website')),
            ],
            options={
                'verbose_name': 'Contact Query',
                'verbose_name_plural': 'Contact Queries',
                'ordering': ['-created_at'],
            },
        ),
    ]
