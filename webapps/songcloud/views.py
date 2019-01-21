from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from django.http import HttpResponse, Http404

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from mimetypes import guess_type
from django.contrib import auth
from django.shortcuts import render_to_response
from django.urls import reverse
from songcloud.forms import *

from django.db import transaction

@login_required
@csrf_protect
def home(request, id):
	# print(request.user)
	user_profile = Profile.objects.get(user=request.user)
	context = {}
	context['current_user'] = request.user
	context['profile'] = user_profile
	# print(user_profile.roomtype)

	if user_profile.roomtype == 0:
		# print("0")
		return render(request, "current_room.html", context)

	elif user_profile.roomtype == 1:
		# print("1")
		room = VirtualRoom.objects.get(id=user_profile.roomid)
		profiles = Profile.objects.filter(roomid=room.id)
	elif user_profile.roomtype == 2:
		# print("2")
		room = RealRoom.objects.get(id=user_profile.roomid)
		profiles = Profile.objects.filter(roomid=room.id)

	print("home")
	print(room.id)
	print(room.roomSongs.all())

	context['room'] = room
	context['profiles'] = profiles
	song_id = room.currentSong
	print(song_id)
	if song_id == 0:
		return render(request, "current_room.html", context)
	else:
		song = room.roomSongs.get(idInRoom=song_id, )
		context['song'] = song
		return render(request, "current_room.html", context)


@csrf_protect
def register(request):
	context = {}

	if request.method == 'GET':
		context['registerform'] = RegisterForm()
		return render(request, 'register.html', context)

	form = RegisterForm(request.POST)
	context['registerform'] = form

	try:
		new_user = User.objects.get(username = request.POST['username'])
		if new_user.is_active == False:
			new_user.delete()
	except User.DoesNotExist:
		new_user = None

	# Validate the form
	if not form.is_valid():
		return render(request, 'register.html', context)

	new_user = User.objects.create_user(username=request.POST['username'], \
										password=request.POST['password1'], \
										first_name=request.POST['first_name'], \
										last_name=request.POST['last_name'], \
										email=request.POST['email'], \

										)
	new_user.is_active = False
	new_user.save()

	#If we get here the form data was valid. Creates the new user. Register and login the user
	user_profile = Profile(user=new_user, \
						   roomtype=int("0"))
	user_profile.save()

	send_account_activation_email(request, new_user)
	context['user'] = new_user.username

	return render(request, "email_confirmation.html", context)


def login(request):
	context = {}
	if request.method == 'GET':
		context['loginform'] = LoginForm()
		return render(request, 'login.html', context)

	errors = []
	context['errors'] = errors

	form = LoginForm(request.POST)
	context['loginform'] = form

	if not form.is_valid():
		return render(request, 'login.html', context)

	user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
	if user is not None and user.is_active:
		auth.login(request, user)
		return redirect('virtual_room_enter')
	else:
		errors.append("Invalid Username or Wrong password!")
		return render(request, 'login.html', context)


@login_required
def logout(request):
	auth.logout(request)
	return redirect('/login')


def send_account_activation_email(request, user):
	text_content = 'Account Activation Email'
	subject = 'Email Activation'
	template_name = "activation.html"
	from_email = settings.DEFAULT_FROM_EMAIL
	recipients = [user.email]
	kwargs = {
		"uidb64": urlsafe_base64_encode(force_bytes(user.pk)).decode(),
		"token": default_token_generator.make_token(user)
	}
	activation_url = reverse("activate_user_account", kwargs=kwargs)

	activate_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), activation_url)

	context = {
		'user': user,
		'activate_url': activate_url
	}

	html_content = render_to_string(template_name, context)
	email = EmailMultiAlternatives(subject, text_content, from_email, recipients)
	email.attach_alternative(html_content, "text/html")
	email.send()

def activate_user_account(request, uidb64=None, token=None):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)

	except User.DoesNotExist:
		user = None
	if user and default_token_generator.check_token(user, token):
		user.is_email_verified = True
		user.is_active = True
		user.save()
		auth.login(request, user)
		return redirect('virtual_room_enter')
	else:
		return HttpResponse("Activation link has expired")

@login_required
def profile(request, id):
	try:
		profile = Profile.objects.get(user=request.user)
	except Profile.DoesNotExist:
		raise Http404

	return render(request, 'profile.html', {'current_user': request.user, 'profile': profile})

@login_required
def edit_profile(request):
	try:
		profile = Profile.objects.get(user=request.user)
	except Profile.DoesNotExist:
		raise Http404
	context = {'profile': profile, 'current_user': request.user}
	return render(request, 'edit_profile.html', context)


def edit_confirmation(request):
	context = {}
	context['current_user'] = request.user
	try:
		user_profile = Profile.objects.get(user=request.user)
	except Profile.DoesNotExist:
		raise Http404
	if request.method == 'GET':
		context['form'] = EditProfileForm()
		context['profile'] = user_profile
		return render(request, 'edit_profile.html', context)
	user_profile.user.first_name = request.POST.get('first_name', user_profile.user.first_name)
	user_profile.user.last_name = request.POST.get('first_name', user_profile.user.last_name)
	user_profile.tag = request.POST.get('style_tag', user_profile.tag)
	user_profile.bio = request.POST.get('bio', user_profile.bio)
	user_profile.photo = request.FILES.get('picture', user_profile.photo)
	user_profile.save()
	context['profile'] = user_profile
	context['current_user'] = request.user
	return redirect(reverse('profile', args=[request.user.id]))


@login_required
def photo(request, id):
    profile = get_object_or_404(Profile, id=id)
    content_type = guess_type(profile.photo.name)
    return HttpResponse(profile.photo, content_type=content_type)


@login_required
@transaction.atomic
def update_dislike(request):
	roomType = request.POST['roomType']
	if int(roomType) == 1:
		room = get_object_or_404(VirtualRoom, id=request.POST['roomId'])
	else:
		room = get_object_or_404(RealRoom, id=request.POST['roomId'])

	song_id = room.currentSong
	song = room.roomSongs.get(idInRoom=song_id)

	if song != None:
		song.dislike = song.dislike + 1
		song.save()
	return HttpResponse('')


@login_required
@transaction.atomic
def update_like(request):
	roomType = request.POST['roomType']
	if int(roomType) == 1:
		room = get_object_or_404(VirtualRoom, id=request.POST['roomId'])
	else:
		room = get_object_or_404(RealRoom, id=request.POST['roomId'])

	song_id = room.currentSong
	song = room.roomSongs.get(idInRoom=song_id)

	if song != None:
		song.like = song.like + 1
		song.save()
	return HttpResponse('')

@login_required
@transaction.atomic
def get_like_dislike(request):
	roomType = request.POST['roomType']
	if int(roomType) == 1:
		room = get_object_or_404(VirtualRoom, id=request.POST['roomId'])
	else:
		room = get_object_or_404(RealRoom, id=request.POST['roomId'])

	song_id = room.currentSong
	if song_id == 0:
		return HttpResponse('')
	else:
		song = room.roomSongs.get(idInRoom=song_id)
		memberNum = room.members.count()
		context = {}
		context['song'] = song
		context['memberNum'] = memberNum
		return render(request, 'dislike.json', context, content_type='application/json')

@login_required
#if roomtype != 0  cannot create
def real_room_create(request):
	context = {'current_user': request.user}
	user_profile = Profile.objects.get(user=request.user)
	# if user_profile.roomtype:
	# 	return render(request, 'current_room.html', context)

	latitude=40.0000
	longtitude=-79.97542
	context={'latitude': latitude, 'longtitude': longtitude, 'current_user': request.user}

	return render(request, 'create_real_room.html', context)


@login_required
#if roomtype != 0  cannot create
def virtual_room_create(request):
	context = {'current_user': request.user}
	user_profile = Profile.objects.get(user=request.user)
	# if user_profile.roomtype:
	#
    #      return render(request, 'current_room.html', context)
	return render(request, 'create_virtual_room.html', context)


@login_required
def create_virtual_room(request):
	context = {}
	user = request.user
	user_profile = Profile.objects.get(user=user)
	errors = []
	context['errors'] = errors
	context['current_user'] = user


	if request.method == 'GET':
		print("get")
		return render(request, 'create_virtual_room.html', context)

	if user_profile.roomtype:
		print("roomtype")
		room = VirtualRoom.objects.get(id=user_profile.roomid)
		context['room'] = room
		errors.append("You are in a room now. Please leave before creating a room !")
		return render(request, 'create_virtual_room.html', context)

	errors = []
	context['errors'] = errors

	# form = VirtualRoomForm(request.POST)
	# context['virtualroomform'] = form

	# print("here")
	room_name = request.POST['room_name']
	# print(room_name)
	for virtualroom in VirtualRoom.objects.all():
		if virtualroom.name == room_name:
			print("exist")
			errors.append("Room with this name is exists!")
			return render(request, 'create_virtual_room.html', context)

	# if not form.is_valid():
	# 	return render(request, 'create_virtual_room.html', context)

	print("success")
	new_virtual_room = VirtualRoom(admin=request.user, \
									name=request.POST['room_name'], \
									description=request.POST['introduction'], \
									maxMembers=int(request.POST['member_number']), \
									tag=request.POST['style_tag'], \
									playmode=int(request.POST['playlist_settings']),  #update later
								    roommode=int(request.POST['room_mode'])
								   )
	new_virtual_room.save()
	user_profile.roomtype = 1
	user_profile.roomid = new_virtual_room.id
	user_profile.save()

	new_virtual_room.members.add(request.user)
	context['room'] = new_virtual_room
	context['profile'] = user_profile
	profiles = Profile.objects.filter(roomid=new_virtual_room.id)
	context['profiles'] = profiles

	# store songs in playlist into roomSongs
	playlist = request.POST['playlist']
	id = playlist.split()[1]
	pl = get_object_or_404(Playlist, id=id)
	songs = pl.songs.all()
	idInRoom = 1
	for song in songs:
		songInRoom = SongInRoom(song=song, idInRoom=idInRoom)
		songInRoom.save()
		new_virtual_room.roomSongs.add(songInRoom)
		idInRoom = idInRoom + 1

	return redirect(reverse('home', args=[user.id]))

@login_required
def virtual_room_enter(request):
	context = {}
	context['current_user'] = request.user
	context['rooms'] = VirtualRoom.objects.all()
	return render(request, 'enter_virtual_room.html', context)

@login_required
def real_room_enter(request):
	context = {}
	context['current_user'] = request.user
	return render(request, 'enter_real_room.html', context)

@login_required
#search for real room
def enter_real_room(request):
	real_rooms = RealRoom.objects.all()
	context = {'real_rooms': real_rooms}
	return render(request, 'real_rooms.json', context, content_type="application/json")

@login_required
def virtual_room_setting(request):
	context = {}
	context['current_user'] = request.user
	try:
		user_profile = Profile.objects.get(user=request.user)
	except Profile.DoesNotExist:
		raise Http404
	if request.method == 'GET':
		context['profile'] = user_profile
		return render(request, 'virtual_room_setting.html', context)
	virtual_room = VirtualRoom.objects.get(admin=request.user)
	virtual_room.description = request.POST.get('introduction', virtual_room.description)
	virtual_room.maxMembers = request.POST.get('member_number', virtual_room.maxMembers)
	virtual_room.tag = request.POST.get('style_tag', virtual_room.tag)
	virtual_room.playmode = request.POST.get('playlist_settings', virtual_room.playmode)
	virtual_room.roommode = request.POST.get('room_mode', virtual_room.roommode)
	virtual_room.save()
	context['room'] = virtual_room
	context['profile'] = user_profile
	profiles = Profile.objects.filter(roomid=virtual_room.id)
	context['profiles'] = profiles
	return redirect(reverse('home', args=[request.user.id]))


@login_required
def real_room_setting(request):
	context = {}
	context['current_user'] = request.user
	try:
		user_profile = Profile.objects.get(user=request.user)
	except Profile.DoesNotExist:
		raise Http404
	if request.method == 'GET':
		context['profile'] = user_profile
		return render(request, 'real_room_setting.html', context)
	real_room = RealRoom.objects.filter(admin=request.user)[0]
	real_room.description = request.POST['introduction']

	# update playlist
	playlist = request.POST['playlist']
	id = playlist.split()[1]
	print("FFFFFFFFFFFFFFFFFFFF")
	print(id)
	pl = get_object_or_404(Playlist, id=id)
	songs = pl.songs.all()
	real_room.roomSongs.clear()
	print(real_room.roomSongs.count())
	idInRoom = 1
	for song in songs:
		songInRoom = SongInRoom(song=song, idInRoom=idInRoom)
		songInRoom.save()
		real_room.roomSongs.add(songInRoom)
		idInRoom = idInRoom + 1
	print(real_room.id)
	print(real_room.roomSongs.all())
	real_room.save()

	context['room'] = real_room
	context['profile'] = user_profile
	profiles = Profile.objects.filter(roomid=real_room.id)
	context['profiles'] = profiles
	return redirect(reverse('home', args=[request.user.id]))


########## playlist related starts ##########
def create_playlist(request):
    if request.method == 'GET':
        context = {}
        context['form'] = PlaylistForm(initial={'owner': request.user})
        context['current_user'] = request.user
        return render(request, 'create_playlist.html', context)

    form = PlaylistForm(request.POST, request.FILES)

    if not form.is_valid():
        context = {}
        context['form'] = form
        return render(request, 'create_playlist.html', context)

    newpl = form.save(commit=False)
    newpl.owner = request.user
    newpl.save()
    return redirect(reverse('playlist', args=[newpl.id]))

def get_playlist(request, id):
	context = {}
	playlist = get_object_or_404(Playlist, id = id)
	context['playlist'] = playlist
	context['current_user'] = request.user
	return render(request, 'playlist.html', context)

def get_pl_photo(request, id):
    playlist = get_object_or_404(Playlist, id = id)
    if not playlist.photo:
        raise Http404
    content_type = guess_type(playlist.photo.name)
    return HttpResponse(playlist.photo, content_type=content_type)

def search_music(request):
    context = {}
    context['type'] = request.POST['type']
    context['id'] = request.POST['id']
    return render(request, 'search_music.html', context)

def add_music(request):
    song, created = Song.objects.get_or_create(
        songId=request.POST['songId'], name=request.POST['name'],
        artist=request.POST['artist'], album=request.POST['album'])
    if request.POST['type'] == "playlist" :
        playlist = get_object_or_404(Playlist, id=request.POST['id'])
        playlist.songs.add(song)
        return HttpResponse('')
    else:
        if request.POST['type'] == "real_room" :
            room = get_object_or_404(RealRoom, id=request.POST['id'])
        else:
            room = get_object_or_404(VirtualRoom, id=request.POST['id'])
        songNum = room.roomSongs.count()
        songInRoom = SongInRoom(song=song, idInRoom=songNum + 1)
        songInRoom.save()
        room.roomSongs.add(songInRoom)
        return HttpResponse('')

########## playlist related ends ##########

########## real room related starts ##########
@login_required
def create_real_room(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    context = {}
    errors = []
    context['errors'] = errors
    context['current_user'] = user
    if request.method == 'GET':
        return render(request, 'create_real_room.html', context)

    if user_profile.roomtype:
        print(user_profile.roomtype)
        errors.append("You are in a room now. Please leave before creating a room !")
        room = RealRoom.objects.get(id=user_profile.roomid)
        context['room'] = room
        return render(request, 'create_real_room.html', context)

    room_name = request.POST['room_name']
    for realroom in RealRoom.objects.all():
        if realroom.name == room_name:
            errors.append("Room with this name is exists!")
            return render(request, 'create_real_room.html', context)

    # create new_real_room
    new_real_room = RealRoom(admin=request.user,\
                        	name=request.POST['room_name'],\
                        	description=request.POST['introduction'],\
                        	latitude=request.POST['latitude'],\
                        	longtitude=request.POST['longtitude'])
    new_real_room.save()
    user_profile.roomtype = 2
    user_profile.roomid = new_real_room.id
    user_profile.save()


    new_real_room.members.add(request.user)


    # store songs in playlist into roomSongs
    playlist = request.POST['playlist']
    id = playlist.split()[1]
    pl = get_object_or_404(Playlist, id=id)
    songs = pl.songs.all()
    idInRoom = 1
    for song in songs:
        songInRoom = SongInRoom(song=song, idInRoom=idInRoom)
        songInRoom.save()
        new_real_room.roomSongs.add(songInRoom)
        idInRoom = idInRoom + 1
    profiles = Profile.objects.filter(roomid=new_real_room.id)
    context['profiles'] = profiles
    return redirect(reverse('home', args=[user.id]))

@login_required
#roomtype !=0 cannot join
def get_real_room(request, id):
    context = {}
    errors = []
    context['errors'] = errors
    context['current_user'] = request.user
    room = get_object_or_404(RealRoom, id=id)
    user = request.user
    user_profile = Profile.objects.get(user=user)
    if user_profile.roomtype != 0 and str(user_profile.roomid) != id:
        errors.append("You are in a room now. Please leave before entering another room !")
        room = RealRoom.objects.get(id=user_profile.roomid)
        context['room'] = room
        return render(request, 'enter_real_room.html', context)
    else:
        room.members.add(user)
        user_profile.roomtype = 2
        user_profile.roomid = room.id
        user_profile.save()

    print("get_real_room")
    print(room.roomSongs.all())
    context['room'] = room
    context['profile'] = user_profile
    profiles = Profile.objects.filter(roomid=room.id)
    context['profiles'] = profiles
    return redirect(reverse('home', args=[user.id]))
########## real room related ends ##########

@login_required
#roomtype !=0 cannot join
def leave_room(request, id):
    context = {}
    user = request.user
    user_profile = Profile.objects.get(user=user)
    profiles = Profile.objects.filter(roomid=id)
    if user_profile.roomtype == 2:
        room = get_object_or_404(RealRoom, id=id)
        print(id)
        room.members.remove(user)
        user_profile.roomtype = 0
        user_profile.roomid = 0
        user_profile.save()
        context['current_user'] = user
        context['room'] = room
        if user == room.admin:
            RealRoom.objects.get(id=id).delete()
            for profile in profiles:
                profile.roomtype = 0
                profile.roomid = 0
                profile.save()
        return render(request, 'enter_real_room.html', context)
    else:
        room = get_object_or_404(VirtualRoom, id=id)
        room.members.remove(user)
        user_profile.roomtype = 0
        user_profile.roomid = 0
        user_profile.save()
        context['current_user'] = user
        context['room'] = room
        if user == room.admin:
            VirtualRoom.objects.get(id=id).delete()
            for profile in profiles:
                profile.roomtype = 0
                profile.roomid = 0
                profile.save()
        context['rooms'] = VirtualRoom.objects.all()
        return render(request, 'enter_virtual_room.html', context)



@login_required
#roomtype !=0 cannot join
def get_virtual_room(request, id):
    context = {}
    errors = []
    context['errors'] = errors
    context['current_user'] = request.user
    room = get_object_or_404(VirtualRoom, id=id)
    user = request.user
    user_profile = Profile.objects.get(user=user)
    if user_profile.roomtype != 0 and str(user_profile.roomid) != id:
        errors.append("You are in a room now. Please leave before entering another room !!")
        room = VirtualRoom.objects.get(id=user_profile.roomid)
        context['room'] = room
        context['rooms'] = VirtualRoom.objects.all()
        return render(request, 'enter_virtual_room.html', context)
    else:
        room.members.add(user)
        user_profile.roomtype = 1
        user_profile.roomid = room.id
        user_profile.save()


    context['room'] = room
    context['profile'] = user_profile
    profiles = Profile.objects.filter(roomid=room.id)
    context['profiles'] = profiles
    return redirect(reverse('home', args=[user.id]))



########## play music related starts ##########
def fetch_current_song(request):
	roomType = request.POST['roomType']
	if int(roomType) == 1:
		room = get_object_or_404(VirtualRoom, id=request.POST['roomId'])
	else:
		room = get_object_or_404(RealRoom, id=request.POST['roomId'])

	if room.currentSong == 0:
		context = {"songId": 0, "time":0, "message":"Waiting admin to start, click Start button later"}
		return render(request, 'curSong.json', context, content_type='application/json')
	else:
		curSong = room.roomSongs.get(idInRoom=room.currentSong)
		context = {"songId": curSong.song.songId, "time":room.currentTime, "message":curSong.song.name}
		return render(request, 'curSong.json', context, content_type='application/json')

def start_admin(request):
	roomType = request.POST['roomType']
	if int(roomType) == 1:
		room = get_object_or_404(VirtualRoom, id=request.POST['roomId'])
	else:
		room = get_object_or_404(RealRoom, id=request.POST['roomId'])

	if room.currentSong == 0:
		room.currentSong = 1
		room.save()

	curSong = room.roomSongs.get(idInRoom=room.currentSong)
	context = {"songId": curSong.song.songId, "time":room.currentTime, "message":curSong.song.name}
	return render(request, 'curSong.json', context, content_type='application/json')

def update_time(request):
	roomType = request.POST['roomType']
	if int(roomType) == 1:
		room = get_object_or_404(VirtualRoom, id=request.POST['roomId'])
	else:
		room = get_object_or_404(RealRoom, id=request.POST['roomId'])

	room.currentTime = request.POST['time']

	# solve race condition
	# old = room.currentSong
	# new = get_object_or_404(RealRoom, id=request.POST['roomId']).currentSong
	# print(old)
	# print("RACE CONDITION CHECK")
	# print(new)

	# if old == new:
	room.save()
	return HttpResponse('')

def update_song_default(request):
	roomType = request.POST['roomType']
	if int(roomType) == 1:
		room = get_object_or_404(VirtualRoom, id=request.POST['roomId'])
	else:
		room = get_object_or_404(RealRoom, id=request.POST['roomId'])

	# change previous song's state
	prevSong = room.roomSongs.get(idInRoom=room.currentSong)
	prevSong.state = 2
	prevSong.save()
	# played all, start from 1st
	songNum = room.roomSongs.count()
	if songNum == room.currentSong:
		room.currentSong = 1
		# reset state of all songs
		for song in room.roomSongs.all():
			song.state = 0
			song.save()
	# fetch next song
	else:
		room.currentSong = room.currentSong+1
	room.currentTime = 0
	room.save()
	curSong = room.roomSongs.get(idInRoom = room.currentSong)
	context = {"songId": curSong.song.songId, "time":room.currentTime, "message":curSong.song.name}
	return render(request, 'curSong.json', context, content_type='application/json')
########## play music related ends ##########

########## room playlist related starts ##########
def get_cur_playlist(request):
	roomType = request.GET['roomType']
	if int(roomType) == 1:
		room = get_object_or_404(VirtualRoom, id=request.GET['roomId'])
	else:
		room = get_object_or_404(RealRoom, id=request.GET['roomId'])

	songs = room.roomSongs.filter(state = 0).order_by('idInRoom') # waiting songs
	context = {"songs": songs}
	return render(request, 'playlist.json', context, content_type='application/json')

########## room playlist related ends ##########