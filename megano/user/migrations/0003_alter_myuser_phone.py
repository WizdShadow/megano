# Generated by Django 5.2 on 2025-04-26 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_myuser_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="myuser",
            name="phone",
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
