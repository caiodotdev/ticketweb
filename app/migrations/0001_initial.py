# Generated by Django 3.1.7 on 2021-12-13 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('price_per_adult', models.DecimalField(decimal_places=2, max_digits=6)),
                ('total_price_per_adult', models.DecimalField(decimal_places=2, max_digits=6)),
                ('taxes', models.DecimalField(decimal_places=2, max_digits=6)),
                ('final_total_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('hour_leave', models.CharField(max_length=255)),
                ('hour_arrive', models.CharField(max_length=255)),
                ('stops', models.CharField(max_length=255)),
                ('durations', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True, null=True)),
                ('data_trip', models.DateField(blank=True, null=True)),
                ('origin', models.CharField(max_length=255)),
                ('destination', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
