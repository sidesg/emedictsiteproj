# Generated by Django 5.0.1 on 2024-02-21 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emedict", "0005_remove_lemma_oid"),
    ]

    operations = [
        migrations.AddField(
            model_name="lemma",
            name="components",
            field=models.ManyToManyField(to="emedict.lemma"),
        ),
    ]
