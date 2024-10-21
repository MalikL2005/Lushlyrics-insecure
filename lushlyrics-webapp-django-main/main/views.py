from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import playlist_user,playlist_model 
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
        # create user 
        new_user = User(username=request.POST['username'], email = request.POST['email'])
        new_user.set_password(request.POST['password'])
        try: 
            new_user.save()
            print("Saved new User")
            # create user-playlist
            # add playlists in player.html 
            playlist_new_user = playlist_user.objects.create(username=request.POST['username'])
            # keep user logged in after signup 
            authenticated_user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if authenticated_user is not None:
                login(request, authenticated_user)
                print("User is authenticated")
                return redirect("default")
        except:
            return redirect("signup", sign_up_failed_message="Wrong parameters, could not create user")
        return redirect("login")


# login using email (not username) does not work yet 
def process_login(request):
    if request.method == 'POST':
        authenticated_user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if authenticated_user is not None: 
            login(request, authenticated_user)
            return redirect("default")
    return HttpResponse("wrong")




def delete_song_from_liked_songs(request, song_title):
    print("reached remove_song_view")
    print(request.user)
    if request.method == 'GET':
        #liked_songs = playlist_user.objects.get(username = request.user)
        #remove song
#        remove_song = playlist_user.objects.filter(username=request.user, song=song_title).delete()
        print(song_title)
        #print(liked_songs)
        return HttpResponse(song_title)




def playlist_test(request):
    user_playlist = playlist_model.objects.filter(user=request.user).all()
    for pl in user_playlist:
        print(pl)

    if request.method == 'GET':
        print(user_playlist)
        return render(request, "add_playlist.html", {"user_playlist": user_playlist})
    
    if request.method == 'POST':
        print(f'user: {request.user}, PLname: {request.POST["name"]}')
        playlist_model.objects.create(name=request.POST['name'], user=request.user)
        print("Added new playlist")
        # add request.song to request.playlist 
        return redirect("home")



def display_playlist(request, title):
    playlist = playlist_model.objects.filter(user=request.user, name=title).first()
    print(playlist)
    if playlist is not None:
        return HttpResponse(playlist)
    return HttpResponse("No such playlist")



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
        return render(request, "playlist.html")
    if request.method == 'GET':
        user_playlist = playlist_user.objects.get(username = request.user)
        users_liked_songs = user_playlist.get_liked_songs()
        print(users_liked_songs)
        try:
            song = request.GET.get('song')
            song = cur_user.playlist_song_set.get(song_title=song)
            # song.delete()
        except:
            pass
        return render(request, 'playlist.html', {'song':song,'user_playlist':users_liked_songs})

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
    if request.method == "POST":
        cur_user = playlist_user.objects.get(username = request.user)

        if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):
            songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
            song__albumsrc=songdic['thumbnails'][0]
            cur_user.playlist_song_set.create(song_title=request.POST['title'],song_dur=request.POST['duration'],
            song_albumsrc = song__albumsrc,
            song_channel=request.POST['channel'], song_date_added=request.POST['date'],song_youtube_id=request.POST['songid'])
        else: 
            cur_user.playlist_song_set.filter(song_title=request.POST['title']).delete()
            print("removed sucessfully")


