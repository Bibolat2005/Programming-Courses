# Generated by Django 5.1.1 on 2024-10-19 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0020_remove_video_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
