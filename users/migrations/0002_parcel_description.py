# Generated by Django 5.0.2 on 2024-03-01 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcel',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]