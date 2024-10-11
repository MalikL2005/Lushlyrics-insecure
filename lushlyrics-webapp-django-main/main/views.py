from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import playlist_user
from django.urls.base import reverse
from django.contrib.auth import authenticate,login,logout
from youtube_search import YoutubeSearch
import json
# import cardupdate



f = open('card.json', 'r')
CONTAINER = json.load(f)

def start(request):
    return render(request, 'start.html')

def signup(request):
    return render(request, 'registration/signup.html')

def create_user(request):
    if request.method == 'POST':
        new_user = User(username=request.POST['username'], email = request.POST['email'])
        new_user.set_password(request.POST['password'])
        try: 
            new_user.save()
            print("Saved new User")
            # create user-playlist

            # import playlist_user from models.py
            playlist_user(username=request.POST['username'])

            # keep user logged in after signup 
            authenticated_user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if authenticated_user is not None:
                login(request, authenticated_user)
                print("User is authenticated")
                return redirect("default")
        except:
            return redirect("signup", sign_up_failed_message="Wrong parameters, could not create user")
        return redirect("login")


# login via Email does not work yet 
def process_login(request):
    if request.method == 'POST':
        authenticated_user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if authenticated_user is not None: 
            login(request, authenticated_user)
            return redirect("default")
    return HttpResponse("wrong")



def default(request):
    global CONTAINER


    if request.method == 'POST':

        add_playlist(request)
        return HttpResponse("")
    if not request.user.is_authenticated: 
        return redirect("start")
    song = 'kSFJGEHDCrQ'
    return render(request, 'player.html',{'CONTAINER':CONTAINER, 'song':song})




def playlist(request):
    try: 
        cur_user = playlist_user.objects.get(username = request.user)
    except: 
        # return render ("page to create playlist objects")
        return render(request, "playlist.html")
    try:
      song = request.GET.get('song')
      song = cur_user.playlist_song_set.get(song_title=song)
      song.delete()
    except:
      return HttpResponse("Hi")
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    song = 'kSFJGEHDCrQ'
    user_playlist = cur_user.playlist_song_set.all()
    # print(list(playlist_row)[0].song_title)
    return render(request, 'playlist.html', {'song':song,'user_playlist':user_playlist})


def search(request):
  if request.method == 'POST':

    add_playlist(request)
    return HttpResponse("")
  try:
    search = request.GET.get('search')
    song = YoutubeSearch(search, max_results=10).to_dict()
    song_li = [song[:10:2],song[1:10:2]]
    # print(song_li)
  except:
    return redirect('/')

  return render(request, 'search.html', {'CONTAINER': song_li, 'song':song_li[0][0]['id']})




def add_playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):

        songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc=songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(song_title=request.POST['title'],song_dur=request.POST['duration'],
        song_albumsrc = song__albumsrc,
        song_channel=request.POST['channel'], song_date_added=request.POST['date'],song_youtube_id=request.POST['songid'])
