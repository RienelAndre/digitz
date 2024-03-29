# Generated by Django 4.2.6 on 2024-01-05 16:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('onlinegradetracker', '0004_grade_course_grade_student_studentprofile_courses_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentprofile',
            old_name='courses',
            new_name='courses_enrolled',
        ),
        migrations.RenameField(
            model_name='studentprofile',
            old_name='Picture',
            new_name='picture',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='DateReleased',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='Grade',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='grade',
            name='grade_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='grade',
            name='grade_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='student',
            name='courses_enrolled',
            field=models.ManyToManyField(to='onlinegradetracker.course'),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='student',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='onlinegradetracker.student'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='course_taught',
            field=models.ManyToManyField(to='onlinegradetracker.course'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10),
        ),
        migrations.AlterField(
            model_name='grade',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='onlinegradetracker.course'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='onlinegradetracker.student'),
        ),
        migrations.AlterField(
            model_name='student',
            name='Status',
            field=models.CharField(choices=[('regular', 'Regular'), ('irregular', 'Irregular')], default=0, max_length=50),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='onlinegradetracker.teacher'),
        ),
    ]
