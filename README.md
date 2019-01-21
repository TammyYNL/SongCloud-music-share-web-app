# Team 34 Web Project: SongCloud Music Share

## Domain name: https://songcloud.ml

## Technologies used: 
1) UI design: Webstorm-Bootstrap v3.3.7 style sheets, Google fonts
2) Language: Python3, HTML5, CSS3, JavaScript
3) Framework: Django
4) API: Apple Music API, Google Map API
5) Deployment: Via Digital Ocean, based on Ubuntu 18.04, Postgres, Nginx, and Gunicorn. Using Let's Encrypt to obtain an SSL certificate is to install the Certbot software on the server.

## Introduction: 
We want to create a web application that allows multiple users to vote for and listen to songs together in real-time. The web application would allow users to create their own rooms that other users can join.

There would be two types of rooms: a ‘​virtual​ room’ and a ‘​real​ room’.
A ‘​virtual​ room’ would be for users at different locations, on different devices. This kind of room would be for friends who want to listen to the same songs together, virtually and in real-time. The ‘virtual room’ will be in charge of selecting the song and playing it across all distributed devices. 
 Users in the room can ‘like’ or ‘dislike’ the current song being played, and the current song can be skipped if more than 80 percent of the room members choose ‘dislike’ (to discourage trolling). Users can add songs to the list. The room creator can choose a default playlist, and edit room settings.
 
 A ‘​real​ room’ would be for users at the same location. This kind of room would be for places like restaurants, bars, clubs, cafes; where the music would be played through a single medium, probably the room creator’s device (i.e. the public speakers that everyone can hear at a cafe). Users can join ​‘real rooms’​ to vote for songs they’d like to be played. Our application would ensure that people are actually at the public venue they are voting for. Just like for ​virtual rooms​, the room creator can configure various options for the room: default playlist, room style tag and room description, etc.

## Fuctionality:
###  Login page:
The user can login with username and password. He/She can find password through email if he/she forgets it.

###  Register page:
By providing first name, last name, username, email address and password, people can register the application.

###  Main page:
###  Sidebar —> Playlist​​:
1) Look up all users’ playlists: The user can see all his/her playlists. By selecting one particular playlist, the user can see the list name, list image, description information and all songs in that list.

2) Add playlist add music to playlists (user’s playlists)   
 — Add user’s playlist: The user can add his/her own playlist by providing list name, list image, description information and then confirming it.   
 — Add music to user’s one particular playlist: The user can add songs to his/her one particular playlist. The user can search for songs through names and then add them.
  
###  Sidebar —> Room:
1) Create room.   
 — Virtual: The user can create a virtual room by providing the room name, room tag, room introduction, setting the default playlist.    
— Real: The user can create a real room by providing the room name, room location, room introduction and setting the default playlist.

2) Enter room.   
 — Enter real room: All the virtual rooms are shown on the enter virtual room page, user can select a certain room to enter.   
 — Enter virtual room: In the real world, the user can see nearby rooms closed to his/her location, with their distances, names and descriptions.

3) Current room: If the user is in a room, he/she can enter the room page.
  
###  Sidebar —> Profile:
Get the current logged user information (username, userpicture, style tag, short introduction), and present the information on the returned profile page.
  
###  Sidebar —> Logout:
Logout the user.
  
###  Music page:
1) Creator:  
 — Start music: Only room creator are able to start music   
 — Room setting: Room creator can reset default playlist, room introduction and style tag.
2) Every room member:   
 — Add music to playlist (room’s playlist): Users in the current room can search a song and add to the room playlist.   
 — Like vs. dislike: Users in the current room can click on like or dislike button of the playing song, store and display the amount of like or dislike of the current music.

## External Resources:
###  UI design: 
fonts: https://fonts.google.com/
###  API:
1) Apple Music API: https://developer.apple.com/documentation/musickitjs
2) Google Map API: https://developers.google.com/maps/documentation/
###  Deployment: 
1) https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04#creating-the-postgresql-database-and-user
2) https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04
3) https://certbot.eff.org/docs/
4) http://www.freenom.com/en/index.html