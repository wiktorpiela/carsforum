# Generated by Django 4.1.7 on 2023-02-28 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('desc', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(choices=[('F1', 'F1'), ('NA', 'NASCAR'), ('TR', 'Trucks'), ('EN', 'Engines'), ('MU', 'Muscle Cars')], default='F1', max_length=2)),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('likes', models.ManyToManyField(blank=True, related_name='answerLikes', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='forumapp.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]