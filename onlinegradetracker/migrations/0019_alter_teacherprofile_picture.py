# Generated by Django 4.2.6 on 2024-01-29 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinegradetracker', '0018_alter_teacherprofile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherprofile',
            name='Picture',
            field=models.ImageField(default='images/default.png', upload_to='images/'),
        ),
    ]