# Generated by Django 4.1.6 on 2023-02-12 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_purchase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='item',
        ),
        migrations.AddField(
            model_name='purchase',
            name='product',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='home.product'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]