# Generated by Django 5.1.1 on 2024-09-25 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_customuser_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="role",
            field=models.CharField(
                choices=[
                    ("user", "User"),
                    ("admin", "Admin"),
                    ("executive", "Executive"),
                ],
                default="admin",
                max_length=20,
            ),
        ),
    ]
