# Generated by Django 2.2.7 on 2019-12-26 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('httpapitest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DebugTalk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('debugtalk', models.TextField(default='#debugtalk.py', null=True)),
                ('belong_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='httpapitest.Project')),
            ],
            options={
                'verbose_name': '驱动py文件',
                'db_table': 'DebugTalk',
            },
        ),
    ]
