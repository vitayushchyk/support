# Generated by Django 4.2.11 on 2024-05-11 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_activationkey_key"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ActivationKey",
        ),
    ]