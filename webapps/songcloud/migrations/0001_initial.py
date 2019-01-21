# Generated by Django 2.1.1 on 2018-11-19 17:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.IntegerField()),
                ('dislike', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=420)),
                ('photo', models.ImageField(blank=True, default='playlist-photos/default.png', upload_to='playlist-photos')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=420)),
                ('photo', models.ImageField(blank=True, default='profile-photos/default.png', upload_to='profile-photos')),
                ('tag', models.CharField(blank=True, max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RealRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=420)),
                ('latitude', models.FloatField()),
                ('longtitude', models.FloatField()),
                ('roomtype', models.IntegerField()),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='real_room_admin', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='real_room_member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('songId', models.CharField(max_length=20)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('artist', models.CharField(blank=True, max_length=100)),
                ('album', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SongInRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField(blank=True, default=0)),
                ('like', models.IntegerField(blank=True, default=0)),
                ('dislike', models.IntegerField(blank=True, default=0)),
                ('state', models.IntegerField(blank=True, default=0)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='songcloud.Song')),
            ],
        ),
        migrations.CreateModel(
            name='VirtualRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=420)),
                ('maxMembers', models.IntegerField()),
                ('tag', models.CharField(blank=True, max_length=20)),
                ('roommode', models.IntegerField()),
                ('playmode', models.IntegerField()),
                ('roomtype', models.IntegerField()),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='virtual_room_admin', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='virtual_room_member', to=settings.AUTH_USER_MODEL)),
                ('roomSongs', models.ManyToManyField(to='songcloud.SongInRoom')),
            ],
        ),
        migrations.AddField(
            model_name='realroom',
            name='roomSongs',
            field=models.ManyToManyField(to='songcloud.SongInRoom'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(to='songcloud.Song'),
        ),
    ]