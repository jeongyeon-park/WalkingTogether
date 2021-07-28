# Generated by Django 3.2.5 on 2021-07-26 13:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('age_range', models.CharField(blank=True, max_length=16, null=True, verbose_name='연령대')),
                ('nickname', models.CharField(blank=True, max_length=64, null=True, verbose_name='닉네임')),
                ('gender', models.CharField(blank=True, choices=[('male', '남'), ('female', '여')], max_length=8, null=True, verbose_name='성별')),
                ('profile_public', models.BooleanField(default=True, verbose_name='프로필 공개 허용 여부')),
                ('number_of_pet', models.IntegerField(default=0, verbose_name='등록 반려동물 수')),
                ('warning_stack', models.IntegerField(default=0, verbose_name='신고 누적 횟수')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '회원',
                'verbose_name_plural': '회원',
                'db_table': 'user',
            },
        ),
    ]
