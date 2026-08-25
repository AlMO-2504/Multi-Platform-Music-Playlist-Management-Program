# Multi-Platform-Music-Playlist-Manager

Streaming platforms' promise has been to offer access to every single piece of media ever created. In the case of the music industry, that would be songs. However, as someone who enjoys listening to both video game music and indie remixes, the songs I like tend to be excluded from official streaming platforms. For example, I have the premium version of Apple Music, but if I were to want to listen to Mario Kart World's, a Nintendo game, soundtrack, I would have to go to either YouTube Music and listen to an unofficial upload that can be taken down at any time, or go to the Nintendo Music app to listen to the songs. Furthermore, songs not available in a streaming platform cannot be included in playlists made in that platform. As a result, I have to constantly be changing apps to be able to listen to my favorite songs.

My project for this semester involves creating a program that can create, manage, and play playlists with songs from streaming services the user is subscribed to and songs they have already downloaded to their device by storing the file address or website, along with other relevant information such as title, artist, and release date. After a playlist has been created, it would allow the user to add and remove songs, change the song order manually or through a pre-programmed sort (alphabetical, by release date, by duration, etc.), and select songs to create a new playlist. It would also keep record of the most listened songs by the user for them to see and to create a Top 10 list.

Inputs: user instruction (creating playlist, registering song, etc.); song location, title, release date, and artist; songs to delete or to add; new song order.
Outputs: new or altered playlist; song registration.

Algorithm:
1. Ask for what the user wants to do: a) register song, b) create playlist, c) edit playlist, d) playback playlists.\
1.a) For registering a song:\
1.a.1. ask for title, artist, release date, and location.\
1.a.2. add new entry to file that stores every other song and store the information\
1.a.3. display "Song successfully registered"\
1.b) For creating a playlist:\
1.b.1. ask for playlist name\
1.b.2. display registered songs\
1.b.3. ask user to choose which songs to include\
1.b.4. store playlist name and song list\
1.b.5. display "Playlist succesfully registered"\
1.c) For editing a playlist:\
1.c.1. ask if the user wants to: a) add song, b) delete song, c) edit song order, d) delete playlist\
1.c.1.a) For adding a song:\
1.c.1.a.1. display registered songs\
1.c.1.a.2. ask user which songs to add\
1.c.1.a.3. add songs to the end of the playlist data file\
1.c.1.a.4. display "Succesfully added songs"\
1.c.1.b) For deleting a song:\
1.c.1.b.1. display registered songs\
1.c.1.b.2. ask user which songs to delete\
1.c.1.b.3. look for songs in the playlist data file\
1.c.1.b.3. remove songs from the playlist data file\
1.c.1.b.4. display "Succesfully deleted songs"\
1.c.1.c) For editing song order:\
1.c.1.c.1. ask user if they want to change it a) manually or through a b) pre-programmed sort\
1.c.1.c.1.a) For manual changes:\
1.c.1.c.1.a.1. display songs in the playlist\
1.c.1.c.1.a.2. ask user to choose a song\
1.c.1.c.1.a.3. ask user to choose a different song to change positions with\
1.c.1.c.1.a.4. change positions in playlist data file and save\
1.c.1.c.1.a.5. ask user if he wants to continue: if yes, return to step 1.c.1.c.1., else, continue\
1.c.1.c.1.b) For pre-programmed sorts:\
1.c.1.c.1.b.1. display pre-programmed sorts\
1.c.1.c.1.b.2. ask user to choose sort\
1.c.1.c.1.b.3. apply sort\
1.c.1.c.1.b.4. save changes in playlist data file\
1.c.1.d) For deleting a playlist:\
1.c.1.d.1. ask user for confirmation\
1.c.1.d.2. delete entry from playlist data file\
1.d) For playing back playlists\
1.d.1. ask user for song where to start\
1.d.2. ask user if they want a) a random order, b) or not\
1.d.2.a) For a random order  
