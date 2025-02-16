# Generated by Django 5.1.4 on 2025-01-11 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_blog_is_active_alter_blog_section_alter_blog_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='author_email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='section',
            field=models.CharField(choices=[('Trending', 'Trending'), ('Recent', 'Recent'), ('Popular', 'Popular')], max_length=100),
        ),
        migrations.AlterField(
            model_name='blog',
            name='status',
            field=models.CharField(choices=[('1', 'Publish'), ('0', 'Draft')], default=0, max_length=1),
        ),
    ]
