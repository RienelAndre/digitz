# Generated by Django 4.2.6 on 2024-01-29 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinegradetracker', '0017_alter_teacherprofile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherprofile',
            name='Picture',
            field=models.ImageField(default='default.png', upload_to=''),
        ),
    ]
