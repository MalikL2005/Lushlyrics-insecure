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
    path("playlist/add-new", views.add_playlist, name="add_playlist"),
    path("search/", views.search, name='search_page'),
]
