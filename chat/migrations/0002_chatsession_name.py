# Generated by Django 3.0.4 on 2020-03-11 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatsession',
            name='name',
            field=models.CharField(default='My ChatRoom', max_length=100),
        ),
    ]