# Generated by Django 4.0.6 on 2022-12-16 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contragent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('town', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=120)),
                ('mol', models.CharField(max_length=120)),
                ('bulstat', models.CharField(max_length=13)),
                ('idmum', models.CharField(blank=True, max_length=15, null=True)),
                ('from_who', models.CharField(blank=True, max_length=120, null=True)),
            ],
            options={
                'db_table': 'contragents',
            },
        ),
        migrations.CreateModel(
            name='OwnerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('town', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=120)),
                ('mol', models.CharField(max_length=120)),
                ('bulstat', models.CharField(max_length=13)),
                ('idmum', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('tel', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'owner',
            },
        ),
        migrations.CreateModel(
            name='OwnerNumbers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_fak_id', models.CharField(max_length=10)),
                ('last_proform_id', models.CharField(max_length=10)),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.ownermodel')),
            ],
            options={
                'db_table': 'last_fak_number',
            },
        ),
        migrations.CreateModel(
            name='FakId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('tip', models.CharField(choices=[('1', '??????????????'), ('2', '????????????????'), ('3', '???????????????? ????????????????')], default=1, max_length=1)),
                ('pay_type', models.CharField(choices=[('1', '????????'), ('2', '??????????'), ('3', '???????????????? ??????????'), ('4', '????????????')], default=1, max_length=1)),
                ('neto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dds', models.IntegerField()),
                ('dds_suma', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fak_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_sdelka', models.DateField(auto_now_add=True)),
                ('data_padej', models.DateTimeField(blank=True, null=True)),
                ('contract_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.contragent')),
            ],
            options={
                'db_table': 'fak',
            },
        ),
        migrations.CreateModel(
            name='FakElelements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=120)),
                ('kol', models.IntegerField()),
                ('brutna_cena', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dds', models.IntegerField()),
                ('element_suma', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('dds_suma', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('element_total', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('faktura_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faktura_id', to='invoice.fakid')),
            ],
            options={
                'db_table': 'fak_elements',
            },
        ),
        migrations.CreateModel(
            name='BankAcc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banc_name', models.CharField(max_length=32)),
                ('bank_acc_kod', models.CharField(max_length=8)),
                ('bank_acc_smetka', models.CharField(max_length=30)),
                ('owner_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.ownermodel')),
            ],
            options={
                'db_table': 'bank',
            },
        ),
    ]
