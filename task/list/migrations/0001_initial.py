# Generated by Django 4.2.2 on 2024-01-30 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('isCompleted', models.BooleanField(default=False)),
            ],
        ),
    ]
