# Generated by Django 4.0.1 on 2022-01-20 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaypalApp', '0011_alter_transactionsmodel_payout_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionsmodel',
            name='payout_fee',
            field=models.FloatField(),
        ),
    ]
