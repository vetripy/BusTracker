# Generated by Django 4.1.3 on 2022-11-22 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_remove_bookings_user_bookings_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookings',
            old_name='user',
            new_name='users',
        ),
    ]
