# Generated by Django 5.1.6 on 2025-02-11 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
