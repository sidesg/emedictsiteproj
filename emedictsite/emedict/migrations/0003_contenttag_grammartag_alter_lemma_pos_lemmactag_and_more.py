# Generated by Django 5.0.2 on 2024-02-08 16:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emedict', '0002_auto_20240203_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=200)),
                ('definition', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='GrammarTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=200)),
                ('definition', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='lemma',
            name='pos',
            field=models.CharField(choices=[('V', 'Verb'), ('N', 'Noun'), ('ADJ', 'Adjective'), ('CNJ', 'Conjunction'), ('QP', 'Question Particle'), ('O', 'Other')], max_length=200),
        ),
        migrations.CreateModel(
            name='LemmaCTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citation', models.TextField()),
                ('lemma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emedict.lemma')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emedict.contenttag')),
            ],
        ),
        migrations.CreateModel(
            name='LemmaGTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citation', models.TextField()),
                ('lemma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emedict.lemma')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emedict.grammartag')),
            ],
        ),
        migrations.DeleteModel(
            name='LemmaTag',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
