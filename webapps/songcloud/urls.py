from . import views
from django.conf.urls import *
from django.contrib.auth import views as auth_views
from . import forms

urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^home/(?P<id>\d+)$', views.home, name='home'),

    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html',
                                                                   form_class=forms.CustomPasswordResetForm,
                                                                   email_template_name='password_reset_email.html'),
        name='password_reset_form'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/account/$',
        views.activate_user_account, name='activate_user_account'),

    url(r'^logout', views.logout, name='logout'),

    url(r'^$', views.register, name='register'),

    url(r'^update_dislike', views.update_dislike, name='update_dislike'),

    url(r'^update_like', views.update_like, name='update_like'),

    url(r'^get_like_dislike', views.get_like_dislike, name='get_like_dislike'),

    url(r'^real_room_create', views.real_room_create, name='real_room_create'),
    url(r'^virtual_room_create', views.virtual_room_create, name='virtual_room_create'),

    # url(r'^create_real_room/(?P<latitude>[^/]+)/(?P<longtitude>[^/]+)$', views.create_real_room, name='create_real_room'),
    url(r'^create_virtual_room', views.create_virtual_room, name='create_virtual_room'),

    # url(r'^current_room/(?P<roomname>[^/]+)$', views.current_room, name='current_room'),

    url(r'^virtualroom_enter', views.virtual_room_enter, name='virtual_room_enter'),
    url(r'^realroom_enter', views.real_room_enter, name='real_room_enter'),


    # url(r'^enter_virtualroom', views.enter_virtual_eneter, name='enter_virtual_room'),
    # url(r'^enter_realroom', views.enter_real_room, name='enter_real_room'),


    url(r'^virtual_room_setting', views.virtual_room_setting, name='virtual_room_setting'),
    url(r'^real_room_setting', views.real_room_setting, name='real_room_setting'),

    url(r'^profile/(?P<id>\d+)$', views.profile, name='profile'),
    url(r'^edit_profile', views.edit_profile, name='edit_profile'),

    ########## playlist related starts ##########
    url(r'^create_playlist', views.create_playlist, name='create_playlist'),

    url(r'^playlist/(?P<id>\d+)$', views.get_playlist, name='playlist'),

    url(r'^pl_photo/(?P<id>\d+)$', views.get_pl_photo, name='pl_photo'),

    url(r'^search_music', views.search_music, name='search_music'),

    url(r'^add_music', views.add_music, name='add_music'),
    ########## playlist related ends ##########


    ########## real room related starts ##########
    url(r'^create_real_room', views.create_real_room, name='create_real_room'),
    url(r'^real_room/(?P<id>\d+)$', views.get_real_room, name='real_room'),
    # join_real_room is not necessary
    ########## real room related ends ##########

    url(r'^enter_realroom', views.enter_real_room, name='enter_real_room'),
    # url(r'^join_virtualroom', views.join_virtual_room, name='join_virtual_room'),
    url(r'^virtual_room/(?P<id>\d+)$', views.get_virtual_room, name='virtual_room'),
    url(r'^leave_room/(?P<id>\d+)$', views.leave_room, name='leave_room'),

    ########## play music related starts ##########
    url(r'^fetch_current_song', views.fetch_current_song, name='fetch_current_song'),
    url(r'^start_admin', views.start_admin, name='start_admin'),
    url(r'^update_time', views.update_time, name='update_time'),
    url(r'^update_song_default', views.update_song_default, name='update_song_default'),
    ########## play music related ends ##########

    ########## room playlist related starts ##########
    url(r'^get_cur_playlist', views.get_cur_playlist, name='get_cur_playlist'),
    ########## room playlist related ends ##########

    url(r'^edit_confirmation', views.edit_confirmation, name="edit_confirmation"),
    url(r'^photo/(?P<id>\d+)$', views.photo, name='photo'),
]
