# Generated by Django 4.1.1 on 2022-09-21 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="category",
            field=models.ManyToManyField(
                related_name="post", through="news.PostCategory", to="news.category"
            ),
        ),
    ]