# Generated by Django 5.0.6 on 2024-08-31 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shops", "0007_alter_customuser_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="address",
            field=models.CharField(default="", max_length=100),
        ),
    ]
