# Generated by Django 4.0.3 on 2022-06-24 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_solicitacao_endereco_alter_solicitacao_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animal',
            name='especie',
        ),
        migrations.RemoveField(
            model_name='raca',
            name='especie',
        ),
        migrations.RemoveField(
            model_name='servico_animal_disponibilidade',
            name='especie',
        ),
        migrations.DeleteModel(
            name='Especie',
        ),
    ]