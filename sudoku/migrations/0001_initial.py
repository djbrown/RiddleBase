# Generated by Django 2.1 on 2018-08-19 14:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('riddles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sudoku',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution', models.TextField()),
                ('pattern', models.TextField()),
                ('difficulty', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('box_rows', models.IntegerField(validators=[django.core.validators.MinValueValidator(2)], verbose_name='Number of horizontal box-rows')),
                ('riddle_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riddles.RiddleType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
