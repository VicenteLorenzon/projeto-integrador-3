# Generated by Django 4.0.3 on 2022-06-16 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_pessoa_user_dados'),
    ]

    operations = [
        migrations.RenameField(
            model_name='animal',
            old_name='tutor',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='carrinho',
            old_name='pessoa',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='cartao',
            old_name='pessoa',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='endereco',
            old_name='pessoa',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='venda',
            old_name='pessoa',
            new_name='user',
        ),
    ]
