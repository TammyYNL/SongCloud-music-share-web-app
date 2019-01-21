from django.db import models

from django.contrib.auth.models import User

# User model (built-in)
# field: username, password, first_name, last_name

class Profile(models.Model):
    # user: every user has a profile associated with his/her
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # bio: display on user's homepage, the maximum number of characters is 420
    bio = models.CharField(max_length=420, blank=True)
    # photo: display on user's homepage and when they enter a music room
    photo = models.ImageField(upload_to="profile-photos", blank=True, default='profile-photos/default.png')
    # tag: eg. classical, hip-hop, country
    tag = models.CharField(max_length=20, blank=True)
    # roomtype: 0 - no room; 1 - virtual room; 2 - real room
    roomtype = models.IntegerField(default = 0)
    # roomid
    roomid = models.IntegerField(null=True)
    def _unicode_(self):
        return self.first_name + " " + self.last_name

    @staticmethod
    def get_profiles(user):
        return Profile.objects.filter(user=user).order_by('last_name', 'first_name')


class Like(models.Model):
    # like: the number of people in the room who like this song
    like = models.IntegerField()
    # dislike: the number of people in the room who dislike this song
    dislike = models.IntegerField()

class Song(models.Model):
    # songId: the id defined by Apple music API
    songId = models.CharField(max_length=20)
    # name of the song
    name = models.CharField(max_length=100, blank=True)
    # artist of the song
    artist = models.CharField(max_length=100, blank=True)
    # album of the song
    album = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.name + \
            "-" + self.artist

class SongInRoom(models.Model):
    # song
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    # idInRoom, set during creation
    idInRoom = models.IntegerField(default=0)
    # vote: the number of people in the room who vote for this song
    vote = models.IntegerField(default=0, blank=True)
    # like: the number of like during its playing
    like = models.IntegerField(default=0, blank=True)
    # dislike: the number of dislike during its playing
    dislike = models.IntegerField(default=0, blank=True)
    # state: 0-waiting, 1-playing, 2-played
    state = models.IntegerField(default=0, blank=True)
    def __str__(self):
        return str(self.idInRoom) + " " + self.song.name

class VirtualRoom(models.Model):
    # admin: the user who created the room
    admin = models.ForeignKey(User, related_name="virtual_room_admin", on_delete=models.CASCADE)
    # name: room's name specified by the admin, the maximum number of characters is 50
    name = models.CharField(max_length=50)
    # description: description of the room, the maximum number of characters is 420
    description = models.CharField(max_length=420, blank=True)
    # maxMembers: the maximum number of member in the room
    maxMembers = models.IntegerField()
    # members: users in the room
    members = models.ManyToManyField(User, related_name="virtual_room_member")
    # tag: eg. classical, hip-hop, country
    tag = models.CharField(max_length=20, blank=True)
    # roommode: 0-private, 1-public
    roommode = models.IntegerField()
    # question: to enter private room, user needs to correctly answer a question
    # question = models.CharField(max_length=100, blank=True)
    # answer: the answer to the entrance question
    # answer = models.CharField(max_length = 20, blank=True)
    # playmode: 0-default, 1-round robin, 2-vote
    playmode = models.IntegerField()
    # roomtype = models.IntegerField()
    # songs: songs to be played
    roomSongs = models.ManyToManyField(SongInRoom)
    # currentSong: the idInRoom field of the song playing
    currentSong = models.IntegerField(default=0, blank=True)
    # currentTime: the time of the current song, in seconds
    currentTime = models.IntegerField(default=0, blank=True)

class RealRoom(models.Model):
    # admin: the user who created the room
    admin = models.ForeignKey(User, related_name="real_room_admin", on_delete=models.CASCADE)
    # name: room's name specified by the admin, the maximum number of characters is 50
    name = models.CharField(max_length=50)
    # description: description of the room, the maximum number of characters is 420
    description = models.CharField(max_length=420, blank=True)
    # maxMembers: the maximum number of member in the room
    # maxMembers = models.IntegerField()
    # members: users in the room
    members = models.ManyToManyField(User, related_name="real_room_member")
    # tag: eg. classical, hip-hop, country
    # tag = models.CharField(max_length=20, blank=True)
    # postion
    latitude = models.FloatField()
    longtitude = models.FloatField()
    # 1 means real room
    # roomtype = models.IntegerField()
    # songs: songs to be played
    roomSongs = models.ManyToManyField(SongInRoom)
    # currentSong: the idInRoom field of the song playing
    currentSong = models.IntegerField(default=0, blank=True)
    # currentTime: the time of the current song, in seconds
    currentTime = models.IntegerField(default=0, blank=True)

class Playlist(models.Model):
    # owner: the user who created the playlist
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # songs: a list of songs in the playlist
    songs = models.ManyToManyField(Song)
    # name: playlist's name specified by the owner, the maximum number of characters is 50
    name = models.CharField(max_length=50)
    # description: description of the playlist, the maximum number of characters is 420
    description = models.CharField(max_length=420, blank=True)
    # photo: the cover photo for playlist
    photo = models.ImageField(upload_to="playlist-photos", blank=True, default='playlist-photos/default.png')
    # date: the date playlist created
    date = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return "user is " + self.owner.username + \
               ", name is " + self.name + \
               ", decription is " + self.description + \
               ", date is " + self.date.strftime("%Y-%m-%d %H:%M:%S")


