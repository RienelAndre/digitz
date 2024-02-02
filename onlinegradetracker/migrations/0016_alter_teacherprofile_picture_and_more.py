# Generated by Django 4.2.6 on 2024-01-29 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlinegradetracker', '0015_remove_studentprofile_courses_enrolled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherprofile',
            name='Picture',
            field=models.ImageField(default='images/default.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacherprofile', to='onlinegradetracker.teacher'),
        ),
    ]
