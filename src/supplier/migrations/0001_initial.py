# Generated by Django 4.1.3 on 2023-10-26 21:33


import django.core.validators
import django.db.models.deletion
from django.db import models, migrations


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierModel',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=50, verbose_name='name of the supplier')),
                (
                    'creation_year',
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(1900)],
                        verbose_name='creation year',
                    ),
                ),
                (
                    'customers_count',
                    models.PositiveIntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name='number of customers',
                    ),
                ),
                (
                    'number_of_sales',
                    models.PositiveIntegerField(
                        default=20,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name='number of sales after which discount is provided',
                    ),
                ),
                (
                    'discount_for_unique_customers',
                    models.DecimalField(
                        decimal_places=2,
                        default=0.2,
                        max_digits=3,
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(0.5),
                        ],
                        verbose_name='discount precent for unique customers',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Suppliers',
                'db_table': 'Supplier',
            },
        ),
        migrations.CreateModel(
            name='SupplierHistory',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('car', models.CharField(max_length=50, verbose_name='car')),
                (
                    'sale_price',
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=14,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                        verbose_name='sale price',
                    ),
                ),
                ('showroom', models.CharField(max_length=50, verbose_name='showroom')),
                (
                    'supplier',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='history',
                        related_query_name='history',
                        to='supplier.suppliermodel',
                        verbose_name='supplier which owns history entry',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Supplier history entry',
                'verbose_name_plural': 'Supplioer history',
                'db_table': 'SupplierHistory',
            },
        ),
        migrations.CreateModel(
            name='SupplierCarDiscount',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=50, verbose_name='discount name')),
                ('description', models.TextField(verbose_name='discount description')),
                (
                    'precent',
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=3,
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(0.5),
                        ],
                        verbose_name='discount precent',
                    ),
                ),
                ('start_date', models.DateTimeField(verbose_name='start date of the discount')),
                ('finish_date', models.DateTimeField(verbose_name='finish date of the discount')),
                (
                    'cars',
                    models.ManyToManyField(
                        related_name='supplier_discounts',
                        related_query_name='supplier_discounts',
                        to='core.carmodel',
                        verbose_name='cars with discounts',
                    ),
                ),
                (
                    'supplier',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='discounts',
                        related_query_name='discounts',
                        to='supplier.suppliermodel',
                        verbose_name='supplier which provides discount',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Supplier discount',
                'verbose_name_plural': 'Supplier discounts',
                'db_table': 'SupplierDiscount',
            },
        ),
        migrations.CreateModel(
            name='SupplierCar',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                (
                    'price',
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=14,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                        verbose_name='price of the car',
                    ),
                ),
                (
                    'car',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='supplier_cars',
                        related_query_name='supplier_cars',
                        to='core.carmodel',
                        verbose_name='supplier car',
                    ),
                ),
                (
                    'supplier',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='cars',
                        related_query_name='cars',
                        to='supplier.suppliermodel',
                        verbose_name='supplier that owns cars',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Supplier car',
                'verbose_name_plural': 'Supplier cars',
                'db_table': 'SupplierCar',
            },
        ),
    ]