# Generated by Django 4.2.7 on 2023-12-31 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playrecord',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='playrecord',
            name='score',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='playrecord',
            name='username',
            field=models.CharField(max_length=20),
        ),
    ]
