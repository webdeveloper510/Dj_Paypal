# Generated by Django 4.0.1 on 2022-01-19 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaypalApp', '0009_alter_transactionsmodel_payout_item_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionsmodel',
            name='payout_batch_id',
            field=models.CharField(default='', max_length=100),
        ),
    ]
