# Generated by Django 5.1.7 on 2025-03-26 10:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('balance', models.IntegerField()),
                ('email', models.EmailField(max_length=100)),
                ('accountno', models.CharField(max_length=12)),
                ('account_type', models.CharField(default='Savings', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('minimum_balance', models.DecimalField(decimal_places=2, default=1000.0, max_digits=12)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bankk_app.bankaccount')),
            ],
        ),
        migrations.CreateModel(
            name='FixedDepositAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('deposit_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('interest_rate', models.DecimalField(decimal_places=2, default=7.0, max_digits=5)),
                ('duration_in_years', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bankk_app.bankaccount')),
            ],
        ),
        migrations.CreateModel(
            name='SavingsAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('minimum_balance', models.DecimalField(decimal_places=2, default=500.0, max_digits=12)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bankk_app.bankaccount')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankk_app.bankaccount')),
            ],
        ),
    ]
