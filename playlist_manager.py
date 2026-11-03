import time
import sys
import msvcrt
"""
Playlist manager
AlMoOl

The following program is a prototype that should be able of registering songs, creating playlists, and playing back playlists
Currently, the program should work similarly to the final product, i. e., functions work with one another
Data storage:
Songs info is stored in a matrix, where one element is the song info. For each list of song info, the data is order in the following way:
1. filepath
2. length (in seconds)
3. title
4. author
For playlists, playlists are stored in a playlist matrix. Inside a playlist, the playlist name is always the first element; also, songs are not stored themselves, but rather, their position (in list, so position 1 is 0)in the main song list:
For example: p_list[0] = ["name", 1, 7, 5], s_list[1] = ["C:...", 331, "virtual insanity", "jamiroquai"]

in a file, songs and playlists lists have been designed to store their elements in a shared file, each element contained in a single line
since their elements are lists, each element uses a separator '|' to separate their own elements. As such, they use the following structure:
    Songs    :
directory|dur|name|artist
    Playlists    :
name|song1|song2|song3|song4|song5|song6|
a heading is utilized to help the program identify what it is reading. said heading uses a lot of blank spaces since user inputs cannot contain them
"""
#storing data
def read_file():
    """
    input: no inputs
    outputs: song and playlist lists from file (system)
    function to read the file that stores info between sessions
    1. check if file 'song_data.txt' already exists, if not create the file, song_list and pl_list start with default values
    2. if it does, read the file
    3. check under what heading is the info contained (songs or playlists)
    4. for songs, separate the line string using the '|' separator into a list
        a. since dur (the second element) represents seconds, transform to int
        b. delete the \n, the character that the file uses to express a new line, from the last element
        c. add song data to song list
    5. for playlists, separate the line string using the '|' separator into a list
        a. since every element apart from the name is a position, transform the elements from 1 to end of list to ints
        b. add playlist data to playlist list
    6. return song and playlist lists
    """
    try:
        sd = open('song_data.txt', 'r')
        data = sd.readlines()
        s_list = []
        pl_list = []
        for d in data:
            if(d == "    Songs    :\n"):
                store_songs = True
                continue
            elif(d == "    Playlists    :\n"):
                store_songs = False
                continue
            if(store_songs == True):
                song = d.split("|")
                song[1] = int(song[1])
                song[3] = song[3][:-1] #removes \n from the last element
                s_list.append(song)
            else:
                playlist = d.split("|")
                playlist[-1] = playlist[-1][:-1] #removes \n from the last element
                for i in range(1, len(playlist)):
                    playlist[i] = int(playlist[i])
                pl_list.append(playlist)
        sd.close()
    except:
        file = open('song_data.txt', 'w')
        file.close()
        s_list = [
            ['', 441, "zen ball master", "glenn powell"],
            ['', 331, "jezebel", "sade"],
            ['', 81, "green eggs and jam", "dunkey"],
            ['', 252, "georgy porgy", "toto"]
        ] #default value
        pl_list = [
            ["dummy", 1, 2, 0, 3]
        ] #defalut value
    return s_list, pl_list

def join_list(list, sep):
    """
    function to turn list to string that separates its elements using a character separator
    input: list and char separator
    output: list as a string
    1. for every element, add string of element and separator to the return string
    2. for the final element, only add the element, the separator is not needed
    """
    string = ""
    for i in range(len(list) - 1):
        string += str(list[i])
        string += sep
    string += str(list[len(list) - 1])
    return string

def write_file(s_l, p_l):
    """
    function to store all the made to the main matrices during the session
    input: song and playlists lists
    output: file with new info
    1. add song heading to file
    2. for every song, join the song data to a string
    3. write the song data in the file, adding a \n char to use another line the next time
    4. add playlist headline to file
    5. steps 2 and 3, but using playlist data
    """
    with open('song_data.txt', 'w') as sd:
        sd.write("    Songs    :\n")
        sep = "|"
        for s in s_l:
            song_data = join_list(s, sep)
            sd.write(f"{song_data}\n")
        sd.write("    Playlists    :\n")
        for p in p_l:
            playlist_data = join_list(p, sep)
            sd.write(f"{playlist_data}\n")
    return
#input validation
def valid_input(inp, type):
    """
    function to check if the input given corresponds to the required data type
    input: user input
    output: true if the input is the requried data type, false if not
    1. check if there is an input
    2. try to convert input to data type
    3. if an error is raised, that means it wasn't the correct data type; return False
    4. if an error did not happen, return true
    """
    if(inp == ''):
        print("please, type something".upper())
        return False
    else:
        try:
            inp = type(inp)
        except ValueError: # checks for the specific type of error produced by converting to an invalid data type ex. int('a')
            return False
    return True

def valid_range(value, low_lim, up_lim, option):
    """
    Input: value that needs to fall within an established range, upper limit of the range, lower limit of the range, what type of range is it (includes limits or not, interval notation)
    Output: value is inside that range (true or false)
    1. if (), verifies that the value is not equal to any limit, and not greater than upper limit nor lower than lower limit
    2. if [], verifies that the value is not greater than upper limit nor lower than lower limit
    3. if (], verifies that the value is not equal or greater than upper limit nor lower than lower limit
    4. if (], verifies that the value is not equal or greater than upper limit nor lower than lower limit
    """
    match option:
        case '()':
            if(value >= up_lim or value <= low_lim):
                return False
        case '[]':
            if(value > up_lim or value < low_lim):
                return False
        case '(]':
            if(value > up_lim or value <= low_lim):
                return False
        case '[)':
            if(value >= up_lim or value < low_lim):
                return False
    return True

def cl_strinput(msg):
    """
    function to remove unnecessary blank spaces (at start, end, and more than one)
    input: input message, a string is asked for inside the function
    output: string with no spaces at the start and end, and no consecutive spaces
    1. ask for string input
    2. for each character of the input, check if the last character was a space, if so, don't add the character.
    3. remove spaces from start and end
    4. return clear string
    """
    inp = input(msg)
    try:
        cl_str = inp[0]
        for i in range(1, len(inp)):
            if(cl_str[-1] == " " and inp[i] == " "):
                continue
            else:
                cl_str += inp[i]
        if(cl_str[0] == " "):
            if(cl_str[-1] == " "):
                return cl_str[1:-1]
            else:
                return cl_str[1:]
        elif(cl_str[-1] == " "):
            return cl_str[0:-1]
        else:
            return cl_str
    except:
        return msg

# main menu display
def action_menu():
    """
    Function for displaying and selecting an option from main action menu
    input: user(action)
    output: user(action options), system(formatted user action input)
    1. display actions
    2. ask for input
    3. return input
    """
    print("main menu".upper())
    print("1. register song") # display menu actions
    print("2. create playlist")
    print("3. edit")
    print("4. playback playlists")
    print("[e]. Type e to exit")
    action = cl_strinput("Choose an option: ") # convert to string
    action = action.lower() # convert to lowercase to reduce the number of options available
    final_action = '' # temporary variable to store characters from action, does not include spaces
    for char in action:
        if(char != ' '): # if it is not a space, the character is added
            final_action += char
    return str(final_action) # this is done to avoid '2 ' not entering the '2' option
        
# Register song
def get_min_sec():
    """
    function to receive a valid min:sec input [00:00]
    input: user(min:sec)
    output: user(error message if it applies), system[total seconds from input (3:15 -> 195 s)]
    1. ask for string input
    2. if the character is not a digit, print not a valid input
    3. while ':' has not been reached, min * 10 and add the digit
    4. after ':' is reached, sec * 10 and add the digit
    5. if ':' was never encountered, print not a valid format
    6. if seconds >= 60, then print seconds can't be greater than 60
    """
    while(True):
        dur = cl_strinput("duration [min:sec]: ") # duration in 00:00
        min_sec = 'min' # working with minutes, currently
        valid = True
        min = 0
        sec = 0
        d = 0
        for char in dur:
            if(char == ':'): # changes from working with minutes to working with seconds
                min_sec = 'sec'
            else:
                if(valid_input(char, int) == False): # checks if char is a digit
                    print("type in format 00:00 using positive digits".upper())
                    valid = False
                    break
                d = int(char) # converts input to digit
                match min_sec:
                    case 'min':
                        min = min * 10
                        min += d
                    case 'sec':
                        sec = sec * 10
                        sec += d
        if(sec >= 60):
            print("seconds can't be greater than or equal to 60".upper())
        elif(valid == False):
            continue # checks if a wrong answer was given, not a digit; avoids accidentally breaking the loop, valid is reset at the start of the loop
        elif(min_sec == 'min'):
            print("please, give length in adequate format".upper())
        else:
            break # if no errors were made by the user, the loop is broken
    dur = 60 * min + sec # transforms minutes to seconds and adds them to the remaining seconds
    return dur # returns the duration in seconds

def register_menu(s_list):
    """
    Function for registering songs
    input: user(song name, artist name, song duration)
    output: user(successful registration message), system(new entry in song matrix)
    1. ask for title
    2. ask for artist
    3. ask for duration using min_sec()
    4. store song info in temporrary list
    5. store temporary list in playlist matrix
    5. print success message
    """
    print("\nsong registration".upper())
    title = cl_strinput("song title: ")
    artist = cl_strinput("artist name: ")
    duration = get_min_sec()
    directory = ''
    song = [directory, duration, title, artist]
    s_list.append(song)
    print(f"Registering song: {title} by {artist}")
    return

#Playlist creation
def disp_avlbl_songs(song_matrix, pl):
    """"
    function to display currently registered songs and if the songs have been added to the playlist
    input: none from user, system(song list, and playlist to be evaluated if songs are in there)
    output: user(song list)
    1. check what songs are already in playlist
    2. if song is already in playlist, print {song info} (already in playlist)
    3. else, print {song info}
    """
    print("\n")
    songs_pl = [] # songs in playlist list
    for i in range(1, len(pl)): # starts at 1, because playlist name is stored in pos = 0
        if(songs_pl.count(pl[i]) == 0): # checks if pl[i] appears in songs_pl
            songs_pl.append(pl[i]) # if not, it adds it to the playlist; this avoid repeat positions
    songs_pl.sort() # sorts the list in ascending order
    j = 0 # second count variable
    already = False # if song is already in playlist
    out_range = False # if the count variable has already reached the end of the songs in playlist list
    for i in range(len(song_matrix)):
        if(len(songs_pl) > 0): # if there are songs in playlist
            if(j >= len(songs_pl)): # checks the count variable does not exceed the list size
                j = len(songs_pl) - 1 # return variable to a safe state
                out_range = True
                already = False
            elif(songs_pl[j] == i and out_range == False): # checks if the pos stored in songs_pl corresponds to the current position (i)
                already = True
                j += 1 # moves j to the next element of songs_pl
            else:
                already = False
        print(f"{i+1}. {song_matrix[i][2]} by {song_matrix[i][3]} {already * '(song already in playlist)'}")
    return

def add_song(pl, s_list): # requires a playlist in list form, not position form
    """
    function to add song to playlist
    input: playlist to add song to, song list (system), song choice (user)
    output: valid song choice position (system)
    1. display avaialable songs
    2. if song is already in playlist, notify the user
    3. ask for song position
    4. check if song choice is in valid range of the song list and is a number
    5. if so, return song choice
    """
    song_added = False # if user has given a valid song to add
    cont = True # continue, if the user wants to continue
    value_error = False
    range_error = False
    c_error = False
    while (cont == True):
        while (song_added == False):
            disp_avlbl_songs(s_list, pl)
            if(value_error == True):
                print("please, type a number".upper())
                value_error = False
            elif(range_error == True):
                print("please, choose one number from the given list".upper())
                range_error =  False
            s = cl_strinput(f"type the number of the song to add to {pl[0]}: ") # 0 stores pl name
            if(valid_input(s, int) == True):
                s = int(s)
                range_error = not valid_range(s, 1, len(s_list), '[]') # valid_range return False if there has been an error and true otherwise, inverting the valuable helps readability
                if(range_error == False):
                    pl.append(s-1) # s is given in natural numbers, positions start at 0
                    song_added = True
            else:
                value_error = True
        if(c_error == True):
            print("Type either Y or N".upper())
            c_error = False
        c = cl_strinput("Would you like to add another song [Y/N]? ") # continue value
        match c.upper():
            case 'Y':
                cont = True
                song_added = False
            case 'N':
                cont = False
            case _:
                c_error = True

def pl_creation(pl_list, s_list):
    """
    function for creating and storing a playlist
    input: user(playlist name, songs in playlist)
    output: none to the user, system(new playlist)
    1. ask for playlist name
    2. display available songs
    3. ask for what song to add
    4. ask if user wants to add another song
    5. if yes, return to step 2
    6. if not, store new pl in pl matrix
    """
    print("\nplaylist creation".upper())
    pl_name = cl_strinput("playlist name: ")
    new_pl = [pl_name]
    add_song(new_pl, s_list)
    pl_list.append(new_pl)
    return

def disp_pl(pl, s_list, pl_list):
    """
    function to display playlist (songs in playlist)
    input: system(playlist position in playlist matrix)
    output: user(playlist)
    1. print every element in the playlist
    2. that's it
    """
    print("\n")
    for i in range(1, len(pl_list[pl])):
        s_pos = pl_list[pl][i] # song position
        print(f"{i}. {s_list[s_pos][2]} - {s_list[s_pos][3]}") #from song list -> s_list[s_pos] is the list of the info associated with that song
    return

def disp_pl_list(pl_list):
    """
    function to display every playlist available
    input: none
    output: user(playlist name and order)
    1. go to pl_list (main playlist matrix)
    2. print the name of every playlist
    """
    print("\nPlaylists")
    for i in range(len(pl_list)):
        print(f"{i+1}. {pl_list[i][0]}") 
    return

def choose_pl(pl_list):
    """
    function to obtain user playlist choice
    input: playlists list (system), playlist choice (user)
    output: valid playlist chocie (system)
    1. show playlists
    2. ask for playlist choice position
    3. check if choice is a number
    4. check if choice is within range
    5. return choice
    """
    disp_pl_list(pl_list)
    if(len(pl_list) == 0):
        return None
    while True:
        pl = cl_strinput("Which playlist: ")
        v_inp = valid_input(pl, int)
        if(v_inp == False):
            print("type the number of the playlist".upper())
        else:
            pl = int(pl)
            v_range = valid_range(pl, 1, len(pl_list), '[]')
            if(v_range == False):
                print("select a number from the given list".upper())
            else:
                return pl

def choose_s(pl, s_list, pl_list, msg):
    """
    function to choose song from playlist, used for deleting songs and playback song selection
    input: playlist, song list, playlist list, message for input (system), song choice (user)
    output: valid song choice (user)
    1. display songs in playlist
    2. ask for song position
    3. check if song choice is within range of the playlist and is a number
    4. if so, return song choice
    """
    disp_pl(pl, s_list, pl_list)
    while True:
        song = cl_strinput(msg)
        v_inp = valid_input(song, int)
        if(v_inp == False):
            print("type the number of the song".upper())
        else:
            song = int(song)
            v_range = valid_range(song, 1, len(pl_list[pl]), '[)')
            if(v_range == False):
                print("select a number from the given list".upper())
            else:
                return song
            
def playback_selection(pl_list, s_list):
    """
    function for choosing which playlist and which song from said playlist to start playback from
    input: user(playlist, and song to start from)
    output: system(playlist, and song to start from)
    1. display playlists
    2. ask for playlist to user
    3. check if answer is coherent, if not return to 2
    4. display songs in chosen playlist
    5. ask for song where to start from from user
    6. return pl and song values
    """
    print("\nplayback".upper())
    if(len(pl_list) > 0):
        pl = choose_pl(pl_list) - 1 # answers are given in natural numbers, positions start at 0
    else:
        print("not enough playlists")
        input("press enter to continue".upper())
        return
    if(len(pl_list[pl]) > 1):
        song = choose_s(pl, s_list, pl_list, "Which song to start from [type the number]: ")
    else:
        print("not enough songs in playlist")
        input("press enter to continue".upper())
        return
    return song, pl

def playback(s_length):
    """
    playback function (this is not the playback menu, it is the function that plays back the current song)
    input: user(command, next, previous or exit), system(song length in seconds)
    output: user(percentage of completion, instructions)
    1. start timer
    2. check if time since timer started is greater or equal to s_lenght
    3. if true, exit
    4. if not, print commands
    5. update the percentage every x seconds (check p variable below)
    6. check if user has given any commands
    7. if yes, return what option the user has chosen
    8. if not, continue
    """
    speed = 10 # how fast the songs are going, 10 = 10x speed
    p = 2 # how (p)recise the updating should be, it expresses a power of 10^-p, for example, 2 means every 0.01 the percentage will update, but also the time precision of calculations. A lower p means greater precision and more updates per second
    start_time = round(time.monotonic(), p) * speed # time.monotonic gives back time in seconds; it is then rounded to the established precision and multiplied by the speed
    past_time = round(time.monotonic(), p) * speed - start_time # the last time recorded, it is relative to start_time so it start at 0 from start time
    error_time_s = 0 # start time for error message (invalid input), after time, the message disappears
    error_time_c = 0 # how much time has passed since start time: error_time_(c)urrent
    error_bool = False # if an invalid input has been given by the user
    command = '' # user input
    msg = "Option: " # the msg given to the user to ask for input
    sys.stdout.write(f"0.0%\nType [e] for exit, [n] for next, [p] for previous.\n{msg}") # prints three lines, one for percentage, one for command list, and one for user input
    while True:
        current_time = round(time.monotonic(), p) * speed - start_time # records how many time has passed since the timer started
        if(current_time >= s_length): # if the time is greater to the duration of the songs, return with [N]ext command
            return 'N'
        else:
            if(error_bool == True): 
                error_time_c = round(time.monotonic(), p) * speed - error_time_s # counts how many time has passed since an invalid input was given
            if(error_time_c > 10): # if 10 seconds have passed, resets error conditions and deletes message
                error_bool = False
                error_time_s = 0
                error_time_c = 0
                sys.stdout.write(f"\033[B\r\033[K\033[1A\r\033[{len(msg)}C")
                """
                to explain stdout.write, consider the following
                {
                0.0%
                Type [e] for exit, [n] for next, [p] for previous.
                Option: [Cursor is here]
                Error message
                }
                \033[B moves cursor down a line
                \r moves cursor to the start of the line
                \033[K wipes the line from the current cursor position, hence \r
                \033[1A moves the cursor up one line
                \r moves the cursor to the start of the line
                \033[{len(msg)}C moves cursor to the right, after "Option: " that is why msg is stored as a string, to calculate its length and move to the right length units
                this returns cursor to the original position 
                """
            if(round(current_time - past_time, p) > 10**(-p)): # if the difference in time between the last time recorded and the current time recorded is greater than the unit established by (p)recision
                # the conditional makes it so every 10**(-p) units the percentage is updated. monotonic gives time with microsecond precision, if every time the time changed the percentage was updated, there would be a lot of uneeded updates
                past_time = current_time # resets past_time
                pg = round(past_time/s_length * 100, 1) # calculates the percentage of the song with a decimal of precition
                sys.stdout.write(f"\033[2A\r\033[K{pg}%\033[2B\r\033[{len(msg)}C")
                """
                consider the following
                {
                0.0%
                Type [e] for exit, [n] for next, [p] for previous.
                Option: [Cursor is here]
                Error message
                }
                \033[A moves cursor up two lines
                \r moves cursor to the start of the line
                \033[K wipes the line
                {
                [Cursor is here]
                Type [e] for exit, [n] for next, [p] for previous.
                Option:
                Error message
                }
                sys prints the percentage, then
                \033[2B moves the cursor down two lines
                \r moves the cursor to the start of the line
                \033[{len(msg)}C moves cursor to the right, after "Option: "
                this returns cursor to the original position 
                """
                sys.stdout.flush() # it updates the changes made by stdout.write() if they had not been written yet
            if(msvcrt.kbhit()): # checks if the user has hit a key in the keyboard
                command = msvcrt.getche() # getche gets and repeats the character, the character is stored as bytes
                command = command.decode(encoding="ascii") # since the character is stored as bytes, it needs to be converted to a string. decode() decodes the bytes using ascii
                command = command.upper() # converts command string to uppercase to facilitate match
            match (command):
                case 'N':
                    return 'N' # next
                case '':
                    continue
                case 'P':
                    return 'P' # previous
                case 'E':
                    return 'E' # exit
                case _:
                    sys.stdout.write(f"\n{command} is NOT AN OPTION\033[1A\r\033[{len(msg)}C\033[K") # writes [KEY] is NOT AN OPTION below the "Option: " line, moves the cursor back up again
                    sys.stdout.flush()
                    error_bool = True
                    error_time_s = round(time.monotonic(), p) * speed # start error timer
                    command = '' # resets command

def pl_playback(start_s, pl, pl_list, s_list):
    """
    function for playing back a playlist
    input: system(start song, playlist)
    output: user(song playback)
    1. print enough space for the terminal to look clean
    2. print current song
    3. print next song
    4. call playback function and store the return value
    5. if return = N, go to the next song
    6. if return = P, go to the previous song
    7. if return = E, exit the playback loop
    """
    option = ''
    i = start_s # count variable 1, for the current song
    j = i + 1 # count variable 2, for the next song
    pl = pl_list[pl] # creates a local copy of the playlist (which are song positions)
    for n in range(6): # prints empty lines to make enough for the following writes
        print("")
    while (option != 'E'):
        sys.stdout.write("\r\033[K\033[A\r\033[K\033[A\r\033[K\033[A\r\033[K\033[A\r\033[K") # clears the past 5 lines
        sys.stdout.flush() # applies changesz if they had not been applied yet
        if(i > len(pl) - 1): # checks if i is bigger than list length to avoid range errors
            i = 1 # return i to the first song position
        elif(i < 1): # if i is lower than 1, which is the lowest position that stores songs, it moves it back up to the end of the list
            i = len(pl) - 1
        if(j > len(pl) - 1): # same for j
            j = 1
        elif(j < 1):
            j = len(pl) - 1
        title = s_list[pl[i]][2] # looks for title of current song
        artist = s_list[pl[i]][3] # looks for artist of current song
        sec = s_list[pl[i]][1] # looks for duration of current song
        title2 = s_list[pl[j]][2] # looks for title of next song
        artist2 = s_list[pl[j]][3] # looks for artist of next song
        min = sec//60 # calculates minutes from the seconds
        sec = sec - min * 60 # calculates the remaining seconds 
        print(f"NOW PLAYING {title} BY {artist} - {min}:{sec}") # prints info of current song
        print(f"Next, {title2} by {artist2}") # prints info of next song
        option = playback(s_list[pl[i]][1]) #saves the return value of playback()
        match option:
            case 'N': # moves to the next song by adding 1 to the count variables
                i += 1
                j += 1
            case 'P': # moves to the previous song by substracting 1 from the count variable
                i -= 1
                j -= 1
    print("\n")
    return

def del_pl_songs(pl, s_list, pl_list):
    """
    function for deleting songs in playlist
    input: playlist position in pl_list, song list, playlist list (system), songs to delete (user)
    output: changed playlist (system)
    1. display songs in playlist
    2. ask for a song to delete
    3. ask for confirmation
    4. remove song from playlist
    5. ask if user wants to continue deleting songs, if so, return to 1
    """
    next = True
    while next and len(pl_list[pl]) > 1:
        s = choose_s(pl, s_list, pl_list, "Which song to delete [type the number]: ")
        while True:
            confirm = cl_strinput(f"Delete {s_list[pl_list[pl][s]][2]} from {pl_list[pl][0]} [Y/N]: ")
            confirm = confirm.lower()
            match confirm:
                case 'y':
                    pl_list[pl].pop(s)
                    break
                case 'n':
                    break
                case _:
                    print("choose a valid option".upper())
        while True:
            cont = cl_strinput(f"Continue deleting songs? [Y/N]: ")
            cont = cont.lower()
            match cont:
                case 'y':
                    next = True
                    break
                case 'n':
                    next = False
                    break
                case _:
                    print("not a valid option".upper())
    return

def ed_pl_name(pl, pl_list):
    """
    function for editing playlist name
    input: playlist, and playlist list (system), new name(user)
    output: changed name in playlist list
    1. display current name
    2. ask for new name
    3. confirm the user wants to change the name
    4. change the name in playlist list
    """
    print(f"\nCurrent name: {pl_list[pl][0]}")
    while True:
        name = cl_strinput("Type a new name: ")
        confirm = cl_strinput(f"Change playlist name from {pl_list[pl][0]} to {name} [Y]es/[N]o/[R]ename: ")
        confirm.lower()
        match confirm:
            case 'y':
                pl_list[pl][0] = name
                break
            case 'n':
                break
            case 'r':
                continue
            case _:
                print("not a valid option")
    return

def del_pl(pl, pl_list):
    """
    function for deleting playlist from playlist list
    input: playlist to delete, playlist list (system), confirmation (user)
    output: deletion of playlist from playlist list
    1. ask user for confirmation
    2. if they really want to do it, delete playlist from playlist list
    """
    while True:
        confirm = cl_strinput(f"Do you really want to delete {pl_list[pl][0]}. This action cannot be undone. [Y/N]: ")
        confirm.lower()
        match confirm:
            case 'y':
                pl_list.pop(pl)
                break
            case 'n':
                break
            case 'r':
                continue
            case _:
                print("not a valid option")
    return

def edit_pl_menu(s_list, pl_list):
    """
    function for choosing which way to edit a playlist
    input: song list, playlist list (system), action (user)
    output: no output (unless an unvalid answer is given), this function calls other function
    1. display functions
    2. ask for action
    3. call the corresponding function
    """
    print("\nPlaylist editing menu".upper())
    pl = choose_pl(pl_list) - 1
    print("\n1. Delete songs")
    print("2. Add songs")
    print("3. Change order")
    print("4. Change name")
    print("5. Delete playlist")
    print("[e]. Return")
    while True:
        act = cl_strinput("Choose an option: ")
        act = act.lower()
        match act:
            case '1':
                if(len(pl_list[pl]) > 1):
                    del_pl_songs(pl, s_list, pl_list)
                else:
                    print("not enough songs in playlist")
                    input("press enter to continue".upper())
                break
            case '2':
                if(len(s_list) > 0):
                    add_song(pl_list[pl], s_list)
                else:
                    print("there are no songs to add")
                    input("press enter to continue".upper())
                break
            case '3':
                print("not available yet")
                break
            case '4':
                ed_pl_name(pl, pl_list)
                break
            case '5':
                del_pl(pl, pl_list)
                break
            case 'e':
                break
            case _:
                print("not a valid option".upper())
    return

def del_songs(s_list, pl_list):
    """
    function for deleting songs from system memory
    input: song list, playlist list (system), song to delete (user)
    output: song deleted from song list and playlists, playlists are also modified to account for the new song list order
    1. ask for song to delete
    2. ask for confirmation
    3. delete the song from song list
    4. delete the song from playlists
    5. shift positions stored in playlists to account for new song order
    """
    print_list = [["SONGS"]] # a simulated matrix is created so code can be reused. choose_s requires a playlist list, so a playlist list with only one lement is created
    for i in range(len(s_list)):
        print_list[0].append(i)
    del_s = choose_s(0, s_list, print_list, "Which song to delete [this will also delete it from any playlists]: ")
    del_s -= 1 # removes one to discard the position occupied by "SONGS"
    while True:
        confirm = cl_strinput("Are you sure? [Y/N]: ")
        confirm = confirm.lower()
        match confirm:
            case 'y':
                s_list.pop(del_s)
                for i in range(len(pl_list)):
                    try:
                        while True:
                            pl_list[i].remove(del_s) #removes instances of the deleted song one by one, produces an error when there are no more left
                    except:
                        for j in range(1, len(pl_list[i])): # accesses playlist, starts from 1 because 0 stores the name
                            if(pl_list[i][j] > del_s):
                                pl_list[i][j] -= 1 # to account for the removed position in the song list, since playlists only stores positions (current_pos > del_song_pos), song positions that were after the deleted song are moved back by one
                break
            case 'n':
                break
            case '_':
                print("not a valid input")
    return

def edit_m_menu(s_list, pl_list):
    """
    function that serves as main (m) editing (edit) menu (menu), displays main options available
    input: song list, playlist list (system), action (user)
    output: no real output (unless an unvalid answer is given), function calls other functions
    1. display options
    2. ask for action
    3. call corresponding function
    """
    print("\n1. Edit playlists")
    print("2. Delete songs")
    while True:
        act = cl_strinput("Choose an option: ")
        act = act.lower()
        match act:
            case '1':
                if(len(pl_list) > 0): # if there are no playlists, why edit them
                    edit_pl_menu(s_list, pl_list)
                else:
                    print("not enough playlists")
                    input("press enter to continue".upper())
                break
            case '2':
                if(len(s_list) > 0): # if there are no songs, why delete them
                    del_songs(s_list, pl_list)
                else:
                    print("not enough songs")
                    input("press enter to continue".upper())
                break
            case _:
                print("not a valid option".upper())
    return

def main():
    songs, playlists = read_file()
    while True:
        act = action_menu()
        match act:
            case '1':
                register_menu(songs)
            case '2':
                if(len(songs) > 0): # if there are no songs, no songs can be added to playlists
                    pl_creation(playlists, songs)
                else:
                    print("not enough songs to do that")
                    input("press enter to continue".upper())
            case '3':
                edit_m_menu(songs, playlists)
            case '4':
                if(len(playlists) > 0): # if there are no playlists, no playlist can be played back
                    try:
                        song, pl = playback_selection(playlists, songs)
                        pl_playback(song, pl, playlists, songs)
                    except: # uses try and except, unlike other cases, because song and pl are being assigned values. There is another validation of song and playlist sizes inside playback_selection, and if an invalid answer is given, a None value is returned
                        print("", end="") # that would cause the variable assignation to break, so this block avoids that
                else:
                    print("not enough playlists")
                    input("press enter to continue".upper())
            case 'e':
                break
            case _:
                print("not an option\n".upper())
        print("\n", end="")
    write_file(songs, playlists)
    return
main()
"""
program test case
1a.-
    inputs{
        1
        adele
        song
        1:44
        2
        pl
    }
    outputs{
        1. zen ball master by glen powell...
        5. adele by song
    }
1b.- (from 1a, after outputs)
    inputs{
        3
        y
        4
        y
        5
        y
        5
        n
        4
    }
    outputs{
        1. dummy
        2. pl
    }
1c.- (from 1b outputs):
    inputs{
        2
    }
    outputs{
        1. green eggs and jam - dunkey
        2. georgy porgy - toto
        3. adele - song
        4. adele - song
    }
1d.- (from 1c outputs)
    inputs{
        3
    }
    outputs{
        NOW PLAYING adele BY song - 1:44
        Next, adele by song
        0.0%
        Type [e] for exit, [n] for next, [p] for previous.
        Option:
    }
1d.- (from 1d outputs)
    inputs{
        n
        n
        n
        p
    }
    outputs{
        NOW PLAYING green eggs and jam BY dunkey - 1:44
        Next, georgy porgy by toto
        0.0%
        Type [e] for exit, [n] for next, [p] for previous.
        Option:
    }
"""
