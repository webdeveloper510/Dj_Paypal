# Generated by Django 4.0.1 on 2022-01-21 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PaypalApp', '0013_transactionsmodel_recipient_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionsmodel',
            old_name='reciever_email',
            new_name='reciever',
        ),
    ]