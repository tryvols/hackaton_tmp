# Generated by Django 4.0.1 on 2022-01-14 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ver_email_code',
            field=models.CharField(db_index=True, default='1011351825780', max_length=48, unique=True),
        ),
    ]
