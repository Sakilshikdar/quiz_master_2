# Generated by Django 4.2.7 on 2024-01-24 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizm', '0003_alter_quiz_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
