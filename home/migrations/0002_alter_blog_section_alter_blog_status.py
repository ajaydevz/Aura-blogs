# Generated by Django 5.1.4 on 2025-01-10 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='section',
            field=models.CharField(choices=[('Recent', 'Recent'), ('Trending', 'Trending'), ('Popular', 'Popular')], max_length=100),
        ),
        migrations.AlterField(
            model_name='blog',
            name='status',
            field=models.CharField(choices=[('0', 'Draft'), ('1', 'Publish')], default=0, max_length=1),
        ),
    ]
