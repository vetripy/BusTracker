# Generated by Django 4.1.3 on 2022-11-22 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_remove_route_route_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcements',
            name='for_user',
            field=models.CharField(choices=[('bus', 'Bus'), ('hos', 'Hostel')], default='bus', max_length=3),
        ),
    ]