# Generated by Django 3.1.4 on 2021-02-03 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20210203_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pic',
            field=models.ImageField(default='./static/img/default.png', null=True, upload_to='images/'),
        ),
    ]
