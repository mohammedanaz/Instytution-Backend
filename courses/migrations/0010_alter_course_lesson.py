# Generated by Django 5.1.1 on 2024-09-14 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_alter_course_description_alter_course_prerequisite_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='lesson',
            field=models.ManyToManyField(blank=True, related_name='course_lessons', to='courses.lesson'),
        ),
    ]
