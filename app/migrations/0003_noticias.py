# Generated by Django 2.2.4 on 2019-08-25 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Noticias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField()),
                ('titulo', models.TextField(max_length=200)),
                ('resumo', models.TextField()),
                ('imagem', models.TextField()),
            ],
        ),
    ]
