# Generated by Django 4.0 on 2022-06-03 03:08

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.functions.datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familymember',
            name='date_of_birth',
            field=models.DateField(validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today)]),
        ),
        migrations.AddConstraint(
            model_name='familymember',
            constraint=models.CheckConstraint(check=models.Q(('date_of_birth__lte', django.db.models.functions.datetime.Now())), name='date_of_birth_cannot_be_future_dated'),
        ),
    ]