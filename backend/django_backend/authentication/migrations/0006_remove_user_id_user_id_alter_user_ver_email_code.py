# Generated by Django 4.0.1 on 2022-01-24 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_user_ver_email_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AddField(
            model_name='user',
            name='ID',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='ver_email_code',
            field=models.CharField(db_index=True, default='ITbjGbDo', max_length=48, unique=True),
        ),
    ]
