# Generated by Django 3.0.7 on 2020-06-18 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20200618_1152'),
        ('blog', '0008_auto_20200617_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Account'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Account'),
        ),
    ]
