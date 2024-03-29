# Generated by Django 2.2.3 on 2019-11-23 08:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_total_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='名称')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='total_views',
            field=models.PositiveIntegerField(default=0, verbose_name='浏览'),
        ),
        migrations.AddField(
            model_name='post',
            name='column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='blog.Column'),
        ),
    ]
