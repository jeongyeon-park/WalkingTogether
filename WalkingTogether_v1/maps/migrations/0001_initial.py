# Generated by Django 3.2.5 on 2021-07-26 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WalkingTrails',
            fields=[
                ('category', models.CharField(max_length=50, verbose_name='카테고리')),
                ('region', models.CharField(max_length=50, verbose_name='지역구')),
                ('distance', models.CharField(max_length=50, verbose_name='거리')),
                ('time_required', models.CharField(max_length=50, verbose_name='소요시간')),
                ('_level', models.IntegerField(verbose_name='코스레벨')),
                ('subway', models.CharField(max_length=255, verbose_name='연계 지하철')),
                ('Transportation', models.CharField(max_length=5000, verbose_name='교통편')),
                ('course_name', models.CharField(max_length=255, verbose_name='코스명')),
                ('course_detail', models.CharField(max_length=5000, verbose_name='세부코스')),
                ('_explain', models.CharField(max_length=5000, verbose_name='포인트설명')),
                ('point_number', models.IntegerField(primary_key=True, serialize=False, verbose_name='포인트순번')),
                ('point_name', models.CharField(max_length=255, verbose_name='포인트명칭')),
                ('longitude', models.DecimalField(decimal_places=14, max_digits=17, verbose_name='경도')),
                ('latitude', models.DecimalField(decimal_places=14, max_digits=16, verbose_name='위도')),
            ],
            options={
                'db_table': 'walkingtrails',
                'managed': False,
            },
        ),
    ]
