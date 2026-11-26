# Multi-Platform-Music-Playlist-Management-Program

Streaming platforms' promise has been to offer access to every single piece of media ever created. In the case of the music industry, that would be songs. However, as someone who enjoys listening to both video game music and indie remixes, the songs I like tend to be excluded from official streaming platforms. For example, I have the premium version of Apple Music, but if I were to want to listen to Mario Kart World's, a Nintendo game, soundtrack, I would have to go to either YouTube Music and listen to an unofficial upload that can be taken down at any time, or go to the Nintendo Music app to listen to the songs. Furthermore, songs not available in a streaming platform cannot be included in playlists made in that platform. As a result, I have to constantly be changing apps to be able to listen to my favorite songs.

My project for this semester involves creating a program that can create, manage, and play playlists with songs from streaming services the user is subscribed to and songs they have already downloaded to their device by storing the file address or website, along with other relevant information such as title, artist, and release date. After a playlist has been created, it would allow the user to add and remove songs, change the song order manually or through a pre-programmed sort (alphabetical, by release date, by duration, etc.), and select songs to create a new playlist. It would also keep record of the most listened songs by the user for them to see and to create a Top 10 list.

**Installation instructions**\
Ensure your system has the playsound3 and mutagen libraries. If you are not sure they are already installed, on the windows terminal run the following commands:\
python -m pip install playsound3\
python -m pip install mutagen

**Running the Program**\
The .py file can be run from any python interpreter that uses Windows, including VsCode and Windows powershell. Linux and MacOs is not guaranteed due to the sys library using different parameters for functions. Furthermore, Thonny is not supported.\
To run the program, open your selected terminal and change directory (cd) to the folder that stores the playlist_manager.py file. The following command is merely illustrative:\
cd C:\Users\user\Desktop\python\pl_mngr\
Once there, simply type:\
py playlist_manager.py\
This should start the program.

**Important**\
The program uses a .txt file called 'song_data.txt' to store both song info an playlist order. If the file were to be deleted, there is no backup to restore the information.\
When first launching the program, 'song_data.txt' will include a dummy song list and playlist for testing purposes. These can be deleted at any time. Finally, changes are only saved when terminating the program from the main menu (e), so don't close it beforehand.

**Used libraries**
playsound3 includes the playsound function, which is used to play music in the background without interrupting other processes.https://pypi.org/project/playsound3 \
mutagen uses the submodules mutagen.mp3 and mutagen.easyid3 to extract metadata from mp3 files, simplifying the process of collecting song info.https://mutagen.readthedocs.io/en/latest/api/index.html \
tkinter includes the filedialog module that opens a window for file selection, simplifying the process of choosing a song stored on the computer. https://docs.python.org/3/library/dialog.html#module-tkinter.filedialog \
sys includes the stdout.write function, which is used for constantly changing the content of the terminal without printing new lines. https://docs.python.org/3/library/sys.html#sys.stdout \
msvcrt includes the kbhit function, which constantly checks for new user inputs without stopping the program, and the getche function, which allows for the reading of the input. This was necessary for the implementation of the playback function. https://docs.python.org/3/library/msvcrt.html \
Finally, the time library (with time.monotonic) is used to keep a timer and, therefore, know when to stop playing back a song. https://docs.python.org/3/library/time.html#time.monotonic
