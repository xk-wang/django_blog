# Generated by Django 2.2.3 on 2019-11-23 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='post/%Y%m%d'),
        ),
    ]