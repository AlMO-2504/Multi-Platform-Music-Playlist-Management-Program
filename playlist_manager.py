"""
Playlist manager
AlMoOl

The following program is a prototype that should be able of registering songs, creating playlists, and playing back playlists
For now, all these actions are separated and locally stored, so if a playlist was created, it won't appear in playback, nor will registered songs appear for playlist creation
"""

# main menu display
def action_menu():
    """
Function for displaying and selecting an option from main action menu
in: action
out: action options, error message if option isn't valid
1. display actions
2. ask user for action
3. check if action is valid
4. if not, display error message and return to step 1. If yes, continue to step 5
5. store action
    """
    valid_action = False # establish that the input(which has not been given yet) is not valid
    while (valid_action == False):
        print("1. register song") # display menu actions
        print("2. create playlist")
        print("3. edit playlist")
        print("4. playback playlists")
        action = int(input("Choose an option: ")) # ask user to choose option
        if(action <= 0 or action > 4): # check if option is not valid, is not in range of action options
            print("Please, choose a valid option.\n") # send error message
        else:
            valid_action = True
            return action # store chosen action
        
# Register song
def register_menu():
    """
Function for registering songs
in: song name, artist name, song location
out: successful registration message
1. ask for name
2. ask for artist
3. ask for location
4. store song info
5. print success message
    """
    name = str(input("song name: "))
    artist = str(input("artist name: "))
    directory = str(input("song location: "))
    song = [name, artist, directory]
    print(f"Registering song: {name} by {artist} in {directory}")
    print("Successful registration")

#Playlist creation
"""
songs are stored under the following format: name, artist, in_playlist (true or false), this is only for this section
"""
def disp_avlbl_songs(song_matrix): # function to display songs availaible/currently registered
    """
function for displaying songs registered in a main matrix
in: song matrix
out: display of song list
1. start a counter, i
2. go through the list of songs
3. for every song, print {i}. {song name}, {song artist}
4. check if song is in playlist
5. add (already in playlist) if true
6. add 1 to i every time the cycle is repeated
    """
    print("\n") # adds a line to distinguish this info from everything else
    i = 1 # count variable
    for song_info in song_matrix: # goes through every song info stored in matrix
        if (song_info[2] == False): # checks if song is not in playlist, which is stored in the third element of the song list
            print(f"{i}. {song_info[0]}, {song_info[1]}") # song are stored as [song name (pos = 0), song artist (pos = 1)]
        else:
            print(f"{i}. {song_info[0]}, {song_info[1]} (song already in playlist)") # adds extra message
        i = i + 1

def validate_song(song, song_mtx_size):
    """
function for validating song if song is in list range
in: song position, song matrix size
out: valid song position
1. convert natural language position to list position
2. check if song is within range of list
3. if not, send error message and return False
4. if yes, return True
    """
    song = song - 1 # since options start at 1 and list order starts at 0
    if(song < 0 or song >= song_mtx_size):
        print("Choose a valid option\n")
        return False
    else:
        return True

def create_pl_menu():
    """
main function for creating playlists section
in: playlist name, songs in playlist
out: new playlist
1. ask for playlist (pl) name
2. disp registered songs
3. ask user to choose a song to include in playlist
4. change state of song to already in playlist in song matrix
5. ask user if they want to continue choosing songs
6. if yes, repeat from step 2
7. if not, display final info of the playlist (songs and order)
    """
    print("\nPlaylist creation: ")
    #assuming the following registered songs
    songs = [["zen ball master", "john powell", False], ["jezebel", "sade", False], ["green eggs and jam", "dunkey", False], ["georgy porgy", "toto", False]]
    songs_chosen = [] # empty vector for song positions
    pl_name = str(input("playlist name: "))
    pl_done = False # assume user is not done choosing songs
    while(pl_done == False):
        disp_avlbl_songs(songs) # call display songs function
        valid_song = False # assume chosen song is not a valid option (not in range of list)
        while(valid_song == False):
            chosen = int(input(f"Type the number of the song you'd like to add to {pl_name}: ")) # ask for song position in displayed list
            valid_song = validate_song(chosen, len(songs)) # call validating function, loop will stop once a valid option is received
        songs_chosen.append(chosen - 1) # adds the list position (natural language - 1) to the songs_chosen list
        songs[chosen - 1][2] = True # changes inclusion state of song in main song matrix
        valid_done = False # asume user doesn't give a valid response to being done 
        while(valid_done == False):
            done = str(input("Would you like to continue adding songs? [Y/N]: "))
            if(done.upper() == 'Y'): # transforms to capital letters to avoid case sensitivity
                valid_done = True # the answer is valid (Y or N)
                pl_done = False # user is not done yet, they want to continue
            elif(done.upper() == 'N'):
                valid_done = True # the answer is valid (Y or N)
                pl_done = True # user is done, they don't want to continue
        if(pl_done == True): # if user is done, print final info of the playlist
            print(f"\n{pl_name}:") # prints playlist title in a new line to avoid messy shell
            i = 1 # uses a count variable to order displayed list
            for ch in songs_chosen: # ch is the position of the song chosen in the main song matrix
                print(f"{i}. {songs[ch][0]}, by {songs[ch][1]}")
                i = i + 1
                
def edit_pl_menu():
    print("not available yet")

def playback_menu():
    """
function for playing songs in playlists
in: playlist, starting song, music command
out: song being currently played
1. display playlists
2. ask for playlist they want to listen to
3. display songs in playlist
4. ask for song where to start
5. display currently playing song
6. ask user if they want to skip, go back to previous song, or stop
7. if they want to stop, stop the loop
8. if they want to skip, move over to the next position in the playlist
9. if they want to go back to previous song, move back to the previous position in the playlist
    """
    # assume the following songs
    songs = [["zen ball master", "john powell"], ["jezebel", "sade"], ["green eggs and jam", "dunkey"], ["georgy porgy", "toto"]]
    # assume the following playlists
    pl1 = ["Playlist 1", 0, 1, 3] # the numbers are the positions of the song inside the songs matrix
    pl2 = ["Playlist 2", 2, 1, 1]
    pl3 = ["Playlist 3", 3, 2, 1, 0]
    pl_total = [pl1, pl2, pl3]
    i = 1
    for playlist in pl_total: # display every playlist with an ordered number
        print(f"{i}. {playlist[0]}")
        i = i + 1
    valid_playlist = False
    while(valid_playlist == False):
        pl = int(input("Choose a playlist: ")) # ask user for playlist
        valid_playlist = validate_song(pl, len(pl_total)) # call validate_song function with the number of elements in pl_total as the range
    i = 1
    for s in range(1, len(pl_total[pl - 1])): # create a vector that goes from 1 to the end of pl_total[pl] so it skips the first position, the first position stores the name of the pl
        #pl_total[pl-1] is the playlist info, -1 because it is stored using natural language, it starts from 1, not 0, as lists do
        song_info = pl_total[pl - 1][s] # it collects the position of each song stored inside the playlist matrix
        print(f"{i}. {songs[song_info][0]}, {songs[song_info][1]}") # as stated before, song info is stored as [name, artist]
        i = i + 1
    valid_song = False
    while(valid_song == False):
        s = int(input("Choose song to start on: "))
        if(s <= 0 or s >= len(pl_total[pl-1])): # validate_song is not aplicable because of <=, s cannot be zero because that's where the name is stored
            valid_song = False
            print("Not a valid option")
        else:
            valid_song = True
    play = True # start play condition
    while(play == True):
        current_song = pl_total[pl - 1][s] # collect song position from playlist list
        print(f"Now playing {songs[current_song][0]} by {songs[current_song][1]}") # use song position to collect info from song matrix 
        print("[S] for stop, [N] for next, [P] for previous: ") # display possible commands
        action = str(input()) # ask for command
        if(action.upper() == 'S'): # upper of input to avoid case sensitivity
            play = False # break loop condition
        elif(action.upper() == 'N'): 
            s = s + 1 # add 1 to go to the next position in playlist list
            if(s == len(pl_total[pl - 1])):
                s = 1 # resets s to one to avoid list errors, and because the first position is stored in 1, zero is reserved for pl name
        elif(action.upper() == 'P'):
            s = s - 1 # substracts 1 to fo to the previous position in playlist list
            if(s == 0):
                s = len(pl_total[pl - 1]) - 1 # once again, since zero is reserved for name, it goes all the way back to the end of the playlist
        else:
            print("not a command")

def main():
    act = action_menu()
    if(act == 1):
        register_menu()
    elif(act == 2):
        create_pl_menu()
    elif(act == 3):
        edit_pl_menu()
    else:
        playback_menu()
main()

"""
test cases:
1.
inputs: 1, a, b, c
expected output: Registering song: a by b in c
actual output: Registering song: a by b in c
2.
input: 67
expected output: please choose a valid option
actual output: Please, choose a valid option.
3.
inputs: 2, pl, 5, 3, y, 1, y, 1, n
expected outputs: (Playlist creation), (1. zenball master... 4. georgy porgy, toto), (choose a valid option), (... 3. green eggs and ham, dunkey (already in playlist)), (1. zenball master,
john powell (already in playlist)), (pl: 1. green eggs and ham, by dunkey 2. zen ball master, by john powell 3. zen ball master, by john powell)
actual output: "Playlist creation: "; "Choose a valid option"; "3. green eggs and jam, dunkey (song already in playlist)"; "1. zen ball master, john powell (song already in playlist)";
"pl:
1. green eggs and jam, by dunkey
2. zen ball master, by john powell
3. zen ball master, by john powell"

4.
inputs: 4, 2, 3, n, n, n, p, p, s
expected outputs:
"1. Playlist 1
2. Playlist 2
3. Playlist 3";
"1. green eggs and ham, dunkey
2. jezebel, sade
3. jezebel, sade";
"Now playing jezebel by sade";
"Now playing green eggs and ham by dunkey";
"Now playing jezebel by sade";
"Now playing green eggs and ham by dunkey";
"Now playing jezebel by sade";
actual outputs:
"1. Playlist 1
2. Playlist 2
3. Playlist 3";
"1. green eggs and jam, dunkey
2. jezebel, sade
3. jezebel, sade";
"Now playing jezebel by sade";
"Now playing green eggs and jam by dunkey";
"Now playing jezebel by sade";
"Now playing green eggs and jam by dunkey";
"Now playing jezebel by sade";

"""