# Generated by Django 5.1.1 on 2024-09-25 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_alter_batch_created_by_alter_batch_updated_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_programs', to='courses.program'),
        ),
    ]
