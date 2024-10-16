from django.db import models


# Create your models here.
class playlist_user(models.Model):
    username = models.CharField(max_length=200)

    def __str__(self):
        return f'Username = {self.username}, Liked Songs = {list(self.playlist_song_set.all())}'
    
    def get_liked_songs(self):
        return list(self.playlist_song_set.all())


class playlist_song(models.Model):
    user = models.ForeignKey(playlist_user, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=200)
    song_youtube_id =  models.CharField(max_length=20)
    song_albumsrc = models.CharField(max_length=255)
    song_dur = models.CharField(max_length=7)
    song_channel = models.CharField(max_length=100)
    song_date_added = models.CharField(max_length=12)

    def __str__(self):
      return f'Title = {self.song_title}, Date = {self.song_date_added}'


class playlist(models.Model):
    name = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(playlist_user, on_delete=models.CASCADE)
    songs_in_playlist = models.ManyToManyField(playlist_song, related_name="playlist_to_songs")

    def __str__(self):
        return f'{self.name} - user: {self.user.username}'
