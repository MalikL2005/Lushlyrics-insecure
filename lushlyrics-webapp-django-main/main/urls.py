from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("home", views.default, name='default'),
    path("", views.start, name='start'),
    path("signup", views.signup, name='signup'),
    path("signup/create-user", views.create_user, name='create_user'),
    path("login/process", views.process_login, name='process_login'),
    path("playlist/", views.playlist, name='your_playlists'),
    path("playlist/test", views.playlist_test, name='playlist_test'),
    path("playlist/<str:title>", views.display_playlist, name='single_playlist'),
    # this is to process playlist-songs via js fetch(url) 
    path("playlist/get-liked-songs", views.get_liked_songs),
    path("playlist/add-new", views.add_playlist, name="add_playlist"),
    path("search/", views.search, name='search_page'),
]
