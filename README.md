# Multi-Platform-Music-Playlist-Manager

Streaming platforms' promise has been to offer access to every single piece of media ever created. In the case of the music industry, that would be songs. However, as someone who enjoys listening to both video game music and indie remixes, the songs I like tend to be excluded from official streaming platforms. For example, I have the premium version of Apple Music, but if I were to want to listen to Mario Kart World's, a Nintendo game, soundtrack, I would have to go to either YouTube Music and listen to an unofficial upload that can be taken down at any time, or go to the Nintendo Music app to listen to the songs. Furthermore, songs not available in a streaming platform cannot be included in playlists made in that platform. As a result, I have to constantly be changing apps to be able to listen to my favorite songs.

My project for this semester involves creating a program that can create, manage, and play playlists with songs from streaming services the user is subscribed to and songs they have already downloaded to their device by storing the file address or website, along with other relevant information such as title, artist, and release date. After a playlist has been created, it would allow the user to add and remove songs, change the song order manually or through a pre-programmed sort (alphabetical, by release date, by duration, etc.), and select songs to create a new playlist. It would also keep record of the most listened songs by the user for them to see and to create a Top 10 list.

__Inputs:__ user instruction (creating playlist, registering song, etc.); song location, title, release date, and artist; songs to delete or to add; new song order.\
__Outputs:__ new or altered playlist; song registration.

__Algorithm:__
1. Ask for what the user wants to do: a) register song, b) create playlist, c) edit playlist, d) playback playlists.\

&emsp;1.a) For registering a song:\
&emsp;&emsp;1.a.1. ask for title, artist, release date, and location.\
&emsp;&emsp;1.a.2. add new entry to file that stores every other song and store the information\
&emsp;&emsp;1.a.3. display "Song successfully registered"\

&emsp;&emsp;1.b) For creating a playlist:\
&emsp;&emsp;&emsp;1.b.1. ask for playlist name\
&emsp;&emsp;&emsp;1.b.2. display registered songs\
&emsp;&emsp;&emsp;1.b.3. ask user to choose which songs to include\
&emsp;&emsp;&emsp;1.b.4. store playlist name and song list\
&emsp;&emsp;&emsp;1.b.5. display "Playlist succesfully registered"\
  
&emsp;&emsp;1.c) For editing a playlist:\
&emsp;&emsp;&emsp;1.c.1. ask if the user wants to: a) add song, b) delete song, c) edit song order, d) delete playlist\
&emsp;&emsp;&emsp;&emsp;1.c.1.a) For adding a song:\
&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.a.1. display registered songs\
&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.a.2. ask user which songs to add\
&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.a.3. add songs to the end of the playlist data file\
&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.a.4. display "Succesfully added songs"\
&emsp;&emsp;&emsp;&emsp;1.c.1.b) For deleting a song:\
&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.b.1. display registered songs\
&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.b.2. ask user which songs to delete\
&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.b.3. look for songs in the playlist data file\
&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.b.3. remove songs from the playlist data file\
&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.b.4. display "Succesfully deleted songs"\
&emsp;&emsp;&emsp;&emsp;1.c.1.c) For editing song order:\
&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.c.1. ask user if they want to change it a) manually or through a b) pre-programmed sort\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.c.1.a) For manual changes:\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.c.1.a.1. display songs in the playlist\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.c.1.a.2. ask user to choose a song\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.c.1.a.3. ask user to choose a different song to change positions with\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.c.1.a.4. change positions in playlist data file and save\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.c.1.a.5. ask user if he wants to continue: if yes, return to step 1.c.1.c.1., else, continue\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.c.1.b) For pre-programmed sorts:\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.c.1.b.1. display pre-programmed sorts\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.c.1.b.2. ask user to choose sort\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.c.1.b.3. apply sort\
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.c.1.b.4. save changes in playlist data file\
&emsp;&emsp;&emsp;&emsp;1.c.1.d) For deleting a playlist:\
&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.d.1. ask user for confirmation\
&emsp;&emsp;&emsp;&emsp;&emsp;1.c.1.d.2. delete entry from playlist data file\

&emsp;&emsp;1.d) For playing back playlists\
&emsp;&emsp;&emsp;1.d.1. ask user for song where to start\
&emsp;&emsp;&emsp;1.d.2. ask user if they want a) a random order, b) or not\
&emsp;&emsp;&emsp;&emsp;1.d.2.a) For a random order\
&emsp;&emsp;&emsp;&emsp;&emsp;1.d.2.a.1. generate a list with numbers from 1 to the number of songs in playlists\
&emsp;&emsp;&emsp;&emsp;&emsp;1.d.2.a.2. follow that order for that playback\
&emsp;&emsp;&emsp;&emsp;1.d.2.b) For a not random order\
&emsp;&emsp;&emsp;&emsp;&emsp;1.d.2.a.1. follow the order in the list\
&emsp;&emsp;&emsp;1.d.3. add 1 to the number of times the song has been played

2. go back to step 1

Songs registered will be stored using matrixes, where one element is also the list of all the information of the songs (artist, date, etc.) as strings, a unique numerical identifier, and the number of times the song has been played. Playlists will also be stored using matrixes where one element is the list of songs included, and the other the order of the songs, both using only numbers. The program itself is a loop and for every action described before there will be a corresponding function as to avoid code repetition.
