# Generated by Django 5.2.1 on 2025-06-30 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryApp', '0003_alter_register_user_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(default='General', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='copies',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
