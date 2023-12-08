# Generated by Django 4.2.4 on 2023-11-04 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SBDcrud', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regbodegafardo',
            name='codBode',
        ),
        migrations.AddField(
            model_name='regbodegafardo',
            name='codUbi',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='SBDcrud.bodega'),
            preserve_default=False,
        ),
    ]
