# Generated by Django 5.0.4 on 2024-05-12 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0003_alter_comment_user_customer_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_path',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
