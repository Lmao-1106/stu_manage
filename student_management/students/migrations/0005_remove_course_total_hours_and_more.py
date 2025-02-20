# Generated by Django 4.2.18 on 2025-02-17 03:14

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_course_fixed_deduction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='total_hours',
        ),
        migrations.AlterField(
            model_name='course',
            name='fixed_deduction',
            field=models.DecimalField(decimal_places=1, default=Decimal('1.0'), max_digits=3, verbose_name='每次课扣除课时'),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='remaining_hours',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=5, verbose_name='剩余课时'),
        ),
    ]
