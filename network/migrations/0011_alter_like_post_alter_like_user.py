# Generated by Django 4.1 on 2023-01-03 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_post_likesnumber_delete_userfollowing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.ManyToManyField(related_name='LikedPost', to='network.post'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='LikedUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
