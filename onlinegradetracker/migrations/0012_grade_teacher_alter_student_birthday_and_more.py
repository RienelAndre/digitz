# Generated by Django 4.2.6 on 2024-01-22 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlinegradetracker', '0011_alter_teacher_course_taught'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='onlinegradetracker.teacher'),
        ),
        migrations.AlterField(
            model_name='student',
            name='Birthday',
            field=models.DateField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='Birthday',
            field=models.DateField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='Other', max_length=10),
        ),
    ]