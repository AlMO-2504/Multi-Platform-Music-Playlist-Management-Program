"""
Playlist manager
AlMoOl

The following program is a prototype that should be able of registering songs,
creating playlists, and playing back playlists. Currently, the program should
work similarly to the final product, i. e., functions work with one another.
Data storage:
Songs info is stored in a matrix, where one element is the song info. For
each list of song info, the data is order in the following way:
1. filepath
2. length (in seconds)
3. title
4. author
For playlists, playlists are stored in a playlist matrix. Inside a playlist,
the playlist name is always the first element; also, songs are not stored
themselves, but rather, their position (in list, so position 1 is 0) in the
main song list:
For example:
p_list[0] = ["name", 1, 7, 5]
s_list[1] = ["C:...", 331, "virtual insanity", "jamiroquai"]
In a file, songs and playlists lists have been designed to store their
elements in a shared file, each element contained in a single line.
Since their elements are lists, each element uses a separator '|' to
separate their own elements. As such, they use the following structure:
    Songs    :
directory|dur|name|artist
    Playlists    :
name|song1|song2|song3|song4|song5|song6|
A heading is utilized to help the program identify what it is reading.
Said heading uses a lot of blank spaces since user inputs cannot contain them.
"""

import msvcrt
import time
from tkinter import filedialog as tk
import sys

from mutagen.mp3 import MP3 as mp3
from mutagen.easyid3 import EasyID3 as easyid3
import playsound3 as ps


DATA_FILE = "song_data.txt"
SPEED = 1  # how fast the song timer goes
T_PRECISION = 3  # time between timer updates: a negative power of 10
# storing data


def read_file():
    """
    input: no inputs
    outputs: song and playlist lists from file (system)
    function to read the file that stores info between sessions
    1. check if file 'song_data.txt' already exists, if not create the file,
       song_list and pl_list start with default values
    2. if it does, read the file
    3. check under what heading is the info contained (songs or playlists)
    4. for songs, separate the line string using the '|' separator into a list
        a. since dur (the second element) represents seconds, transform to int
        b. delete the \n, the character that the file uses to express a new
           line, from the last element
        c. add song data to song list
    5. for playlists, separate the line string using the '|' separator
       into a list
        a. since every element apart from the name is a position, transform
           the elements from 1 to end of list to ints
        b. add playlist data to playlist list
    6. return song and playlist lists
    """
    try:
        s_data = open(DATA_FILE, "r")
        data = s_data.readlines()
        s_list = []
        pl_list = []
        for line in data:
            if line == "    Songs    :\n":
                store_songs = True
                continue
            elif line == "    Playlists    :\n":
                store_songs = False
                continue
            if store_songs == True:
                song = line.split("|")
                song[1] = float(song[1])
                song[3] = song[3][:-1]  # removes \n from the last element
                s_list.append(song)
            else:
                playlist = line.split("|")
                playlist[-1] = playlist[-1][:-1]
                for i in range(1, len(playlist)):
                    playlist[i] = int(playlist[i])
                pl_list.append(playlist)
        s_data.close()
    except:
        file = open(DATA_FILE, "w")
        file.close()
        s_list = [
            ["", 441, "zen ball master", "glenn powell"],
            ["", 331, "jezebel", "sade"],
            ["", 81, "green eggs and jam", "dunkey"],
            ["", 252, "georgy porgy", "toto"],
        ]  # default value
        pl_list = [["dummy", 1, 2, 0, 3]]  # defalut value
    return s_list, pl_list


def join_list(list, sep):
    """
    function to turn list to string that separates its elements using
    a character separator
    input: list and char separator
    output: list as a string
    1. for every element, add string of element and separator to the
       return string
    2. for the final element, only add the element, the separator
       is not needed
    """
    string = ""
    for i in range(len(list) - 1):
        string += str(list[i])
        string += sep
    string += str(list[len(list) - 1])
    return string


def write_file(song_l, pl_l):
    """
    function to store all the made to the main matrices during the session
    input: song and playlists lists
    output: file with new info
    1. add song heading to file
    2. for every song, join the song data to a string
    3. write the song data in the file, adding a \n char to use another
       line the next time
    4. add playlist headline to file
    5. steps 2 and 3, but using playlist data
    """
    with open(DATA_FILE, "w") as s_data:
        s_data.write("    Songs    :\n")
        sep = "|"  # separator
        for song in song_l:
            song_data = join_list(song, sep)
            s_data.write(f"{song_data}\n")
        s_data.write("    Playlists    :\n")
        for playlist in pl_l:
            playlist_data = join_list(playlist, sep)
            s_data.write(f"{playlist_data}\n")


# input validation


def valid_input(inp, type):
    """
    function to check if the input given corresponds to the required data type
    input: user input
    output: true if the input is the requried data type, false if not
    1. check if there is an input
    2. try to convert input to data type
    3. if an error is raised, that means it wasn't the correct data
       type; return False
    4. if an error did not happen, return true
    """
    if inp == "":
        print("please, type something".upper())
        return False
    else:
        try:
            type(inp)
        except ValueError:
            # checks for converting to an invalid data type ex. int('a')
            return False
    return True


def valid_range(value, low_lim, up_lim, option):
    """
    Input: value that needs to fall within an established range, upper
    limit of the range, lower limit of the range, what type of range is it
    (includes limits or not, interval notation)
    Output: value is inside that range (true or false)
    1. if (), verifies that the value is not equal to any limit,
       and not greater than upper limit nor lower than lower limit
    2. if [], verifies that the value is not greater than upper limit
       nor lower than lower limit
    3. if (], verifies that the value is not equal or greater than upper
       limit nor lower than lower limit
    4. if (], verifies that the value is not equal or greater than upper
       limit nor lower than lower limit
    """
    match option:
        case "()":
            if value >= up_lim or value <= low_lim:
                return False
        case "[]":
            if value > up_lim or value < low_lim:
                return False
        case "(]":
            if value > up_lim or value <= low_lim:
                return False
        case "[)":
            if value >= up_lim or value < low_lim:
                return False
    return True


def cl_strinput(msg):
    """
    function to remove unnecessary blank spaces (at start, end,
    and more than one)
    input: input message, a string is asked for inside the function
    output: string with no spaces at the start and end, and no consecutive
    spaces
    1. ask for string input
    2. for each character of the input, check if the last character was a
       space, if so, don't add the character.
    3. remove spaces from start and end
    4. return clear string
    """
    inp = input(msg)
    try:
        cl_str = inp[0]
        for i in range(1, len(inp)):
            if cl_str[-1] == " " and inp[i] == " ":
                continue
            else:
                cl_str += inp[i]
        if cl_str[0] == " ":
            if cl_str[-1] == " ":
                return cl_str[1:-1]
            else:
                return cl_str[1:]
        elif cl_str[-1] == " ":
            return cl_str[0:-1]
        else:
            return cl_str
    except:
        return msg


def invalid_option(invalid):
    """
    function for printing error messages when an invalid option is sent
    input: error message (system)
    output: error message (user)
    1. print errror message
    2. go up two lines and clear the line so a new input message
       can be printed
    """
    print(invalid)
    print(f"\r\033[2A\033[K", end="")


def not_invalid_option():
    """
    function for deleting error messages when a valid option is given
    inputs: none
    outputs: clear error message line (user)
    1. since the cursor would be in the error line, if there is an error line,
       after receiving the input, only delete the current line and end with ""
       to avoid adding extra lines
    """
    print("\r\033[K", end="")


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
    print("\n")
    print("main menu".upper())
    print("1. register song")  # display menu actions
    print("2. create playlist")
    print("3. edit")
    print("4. playback playlists")
    print("[e]. Type e to exit")
    action = cl_strinput("Choose an option: ")  # convert to string
    action = (
        action.lower()
    )  # convert to lowercase to reduce the number of options available
    final_action = ""  # temporary variable to store characters from action
    for char in action:
        if char != " ":  # if it is not a space, the character is added
            final_action += char
    return final_action


# Register song


def get_min_sec():
    """
    function to receive a valid min:sec input [00:00]
    input: user(min:sec)
    output: user(error message if it applies), system[total seconds from
        input (3:15 -> 195 s)]
    1. ask for string input
    2. if the character is not a digit, print not a valid input
    3. while ':' has not been reached, min * 10 and add the digit
    4. after ':' is reached, sec * 10 and add the digit
    5. if ':' was never encountered, print not a valid format
    6. if seconds >= 60, then print seconds can't be greater than 60
    """
    msg = "duration [min:sec]: "
    while True:
        dur = cl_strinput(msg)  # duration in 00:00
        min_sec = "min"  # working with minutes, currently
        valid = True
        min = 0
        sec = 0
        dig = 0 # digit
        for char in dur:
            if char == ":":  # flips minute to second conversion
                min_sec = "sec"
            else:
                if valid_input(char, int) == False:
                    invalid_option(
                        "\033[Ktype in format 00:00 "
                        "using positive digits".upper()
                    )
                    valid = False
                    break
                dig = int(char)
                match min_sec:
                    case "min":
                        min = min * 10
                        min += dig
                    case "sec":
                        sec = sec * 10
                        sec += dig
        if sec >= 60:
            invalid_option(
                "\033[Kseconds can't be greater than or equal to 60".upper()
            )
        elif valid == False:
            continue  # checks if a wrong answer was given: not a digit
        elif min_sec == "min":
            invalid_option(
                "\033[Kplease, give length in adequate format".upper()
            )
        else:
            not_invalid_option()
            break
    dur = (
        60 * min + sec
    )  # transforms minutes to seconds and adds them to the remaining seconds
    return dur  # returns the duration in seconds


def manual_select(if_file_p, if_length): # filepath, song length
    """
    function to allow user to manually submit song info
    inputs: if filepath is needed, if song lenght is needed (system),
        filepath, song length, title, artist (user)
    output: manual song info (system)
    1. if filepath and length are needed, ask for those, title and artist
    2. if length is needded, ask for length, title, and artist
    3. otherwise, ask only for title and artist
    """
    if if_file_p == True and if_length == True:
        while True:
            msg = "is the song stored in the computer? [Y]es/[N]o: "
            in_unit = cl_strinput(msg)
            match in_unit.lower():
                case "y":
                    dir = cl_strinput("type out the mp3 filepath: ")
                    dir = dir.strip('"')
                    break
                case "n":
                    dir = ""
                    break
                case _:
                    invalid_option("not a valid option")
        not_invalid_option()
        title = cl_strinput("song title: ")
        artist = cl_strinput("artist name: ")
        length = get_min_sec()
        return dir, length, title, artist
    elif if_length == True:
        title = cl_strinput("song title: ")
        artist = cl_strinput("artist name: ")
        length = get_min_sec()
        return length, title, artist
    else:
        title = cl_strinput("song title: ")
        artist = cl_strinput("artist name: ")
        return title, artist


def song_select():
    """
    function for selecting songs directly from file explorer
    inputs: filepath (user)
    outputs: song info (system), success message (user)
    1. with the tkinter library, open file explorer window where the user
       can choose only mp3 files
    2. if a file with an mp3 file path is selected, use mutagen library to
       try and get the info directly from the metdata
        a. if the operation is not successful, call manual select function,
           and ask for length, title and artist only, since a filepath has
           been provided
    3. if no filepath is given, call manual select function and askfor
       all song info
    4. return song info
    """
    print("choose a song from your files: ")
    dir = tk.askopenfilename(
        title="choose a song from your files",
        filetypes=[("MP3 Audio Files", "*.mp3")]
    )
    if dir:
        try:
            audio = mp3(dir)
            info = easyid3(dir)
            title = info.get("title")[0]
            artist = info.get("artist")[0]
            length = audio.info.length
            print(f"Is this info correct?\nTitle: {title}\nArtist: {artist}")
            msg = "[Y]es/[N]o: "
            while True:
                correct = cl_strinput(msg)
                if correct.lower() == "y":
                    break
                elif correct.lower() == "n":
                    title, artist = manual_select(
                        if_file_p=False,
                        if_length=False
                    )
                    break
                else:
                    invalid_option("not a valid option")
        except:
            print("data could not be extracted")
            length, title, artist = manual_select(
                if_file_p=False,
                if_length=True
                )
    else:
        dir, length, title, artist = manual_select(
            if_file_p=True,
            if_length=True
            )
    return [dir, length, title, artist]


def confirm_info(info):
    """
    function for printing the message to validate song info
    inputs: song info (system)
    output: song info to validate (user)
    """
    print("\n")
    print("confirm info".upper())
    seconds = str(int(info[1] % 60))
    if (len(seconds) == 1):
        seconds = '0' + seconds
    print(
        f"Title: {info[2]}\n"
        f"Artist: {info[3]}\n"
        f"Length: {int(info[1] // 60)}:{seconds}\n"
        f"Filepath: {info[0]}"
    )


def register_menu(s_list):
    """
    Function for registering songs
    input: user(song name, artist name, song duration)
    output: user(successful registration message),
       system(new entry in song matrix)
    1. ask for title
    2. ask for artist
    3. ask for duration using min_sec()
    4. store song info in temporrary list
    5. store temporary list in playlist matrix
    5. print success message
    """
    print("\nsong registration".upper())
    song_reg = False
    msg = (
        "Do you want to store the song using this info? "
        "[Y]es/[N]o, change info/[E]xit: "
        )
    while True:
        if song_reg == False:
            song = song_select()
            confirm_info(song)
        confirm = cl_strinput(msg)
        match confirm.lower():
            case "y":
                s_list.append(song)
                not_invalid_option()
                print(f"{song[2]} by {song[3]} has been registered")
                return
            case "n":
                song_reg = False
                not_invalid_option()
                print("Song registration will start over")
                input("press enter to continue\n".upper())
            case "e":
                not_invalid_option()
                return
            case _:
                song_reg = True
                invalid_option("not a valid option")


# Playlist creation


def disp_avlbl_songs(song_matrix, pl):
    """
    function to display currently registered songs and if the songs have
    been added to the playlist
    input: none from user, system(song list, and playlist to be evaluated
        if songs are in there)
    output: user(song list)
    1. check what songs are already in playlist
    2. if song is already in playlist, print {song info} (already in playlist)
    3. else, print {song info}
    """
    print("\n")
    songs_pl = []  # songs in playlist list
    for i in range(
        1, len(pl)
    ):  # starts at 1, because playlist name is stored in pos = 0
        if songs_pl.count(pl[i]) == 0:  # checks if pl[i] appears in songs_pl
            songs_pl.append(
                pl[i]
            )
    songs_pl.sort()
    j = 0 
    already = False  # if song is already in playlist
    out_range = False  # if the count variable has reached the end of the list
    for i in range(len(song_matrix)):
        if len(songs_pl) > 0:  # if there are songs in playlist
            if j >= len(songs_pl):
                j = len(songs_pl) - 1  # return variable to a safe state
                out_range = True
                already = False
            elif (songs_pl[j] == i and out_range == False):  
                already = True
                j += 1  # moves j to the next element of songs_pl
            else:
                already = False
        print(
            f"{i + 1}. {song_matrix[i][2]} by {song_matrix[i][3]} "
            f"{already * '(song already in playlist)'}"
        )


def add_song(pl, s_list):  # requires a playlist in list form
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
    song_added = False  # if user has given a valid song to add
    cont = True  # continue, if the user wants to continue
    value_error = False
    range_error = False
    c_error = False
    msg = f"type the number of the song to add to {pl[0]}: "
    msg_c = "\033[KWould you like to add another song [Y/N]? "
    while cont == True:
        if song_added == False:
            disp_avlbl_songs(s_list, pl)
        while song_added == False:
            if value_error == True:
                invalid_option(
                    "\033[Kplease, type a number".upper()
                )
                value_error = False
            elif range_error == True:
                invalid_option(
                    "\033[K"
                    "please, choose one number from the given list".upper()
                )
                range_error = False
            song = cl_strinput(msg)
            if valid_input(song, int) == True:
                song = int(song)
                range_error = not valid_range(song, 1, len(s_list), "[]") 
                if range_error == False:
                    not_invalid_option()
                    pl.append(
                        song - 1
                    )  # s is given in natural numbers, positions start at 0
                    song_added = True
            else:
                value_error = True
        if c_error == True:
            invalid_option("\033[KType either Y or N".upper())
            c_error = False
        cont_choice = cl_strinput(msg_c)  # continue value
        match cont_choice.upper():
            case "Y":
                cont = True
                song_added = False
            case "N":
                cont = False
            case _:
                c_error = True
    not_invalid_option()


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
        s_pos = pl_list[pl][i]  # song position
        print(
            f"{i}. {s_list[s_pos][2]} - {s_list[s_pos][3]}"
        )


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
        print(f"{i + 1}. {pl_list[i][0]}")


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
    if len(pl_list) == 0:
        return None
    while True:
        msg = "Which playlist: "
        pl = cl_strinput(msg)
        val_inp = valid_input(pl, int)
        if val_inp == False:
            invalid_option(
                "\033[Ktype the number of the playlist".upper()
            )
        else:
            pl = int(pl)
            val_range = valid_range(pl, 1, len(pl_list), "[]")
            if val_range == False:
                invalid_option(
                    "\033[Kselect a number from the given list".upper()
                )
            else:
                not_invalid_option()
                return pl


def choose_s(pl, s_list, pl_list, msg):
    """
    function to choose song from playlist, used for deleting songs
    and playback song selection
    input: playlist, song list, playlist list, message for input (system),
        song choice (user)
    output: valid song choice (user)
    1. display songs in playlist
    2. ask for song position
    3. check if song choice is within range of the playlist and is a number
    4. if so, return song choice
    """
    disp_pl(pl, s_list, pl_list)
    while True:
        song = cl_strinput(msg)
        val_inp = valid_input(song, int)
        if val_inp == False:
            invalid_option(
                "\033[Ktype the number of the song".upper()
            )
        else:
            song = int(song)
            val_range = valid_range(song, 1, len(pl_list[pl]), "[)")
            if val_range == False:
                invalid_option(
                    "\033[Kselect a number from the given list".upper()
                )
            else:
                not_invalid_option()
                return song


def playback_selection(pl_list, s_list):
    """
    function for choosing which playlist and which song from said playlist
    to start playback from
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
    if len(pl_list) > 0:
        pl = (
            choose_pl(pl_list) - 1
        )  # answers are given in natural numbers, positions start at 0
    else:
        print("not enough playlists")
        input("press enter to continue".upper())
        return
    if len(pl_list[pl]) > 1:
        song = choose_s(
            pl, s_list, pl_list,
            "Which song to start from [type the number]: "
        )
    else:
        print("not enough songs in playlist")
        input("press enter to continue".upper())
        return
    return song, pl


def playback(s_length):
    """
    playback function (this is not the playback menu, it is the function
    that plays back the current song)
    input: user(command, next, previous or exit), system(song length in
        seconds)
    output: user(percentage of completion, instructions)
    1. start timer
    2. check if time since timer started is greater or equal to s_length
    3. if true, exit
    4. if not, print commands
    5. update the percentage every x seconds (check p variable below)
    6. check if user has given any commands
    7. if yes, return what option the user has chosen
    8. if not, continue
    """
    start_time = (
        round(time.monotonic(), T_PRECISION) * SPEED
    )  # time.monotonic gives back time in seconds
    # it is then rounded to the established precision and multiplied by the speed
    past_time = (
        round(time.monotonic(), T_PRECISION) * SPEED - start_time
    )
    error_time_s = 0  # start time for error message (invalid input)
    error_time_c = 0  # how much time has passed since error time start
    error_bool = False  # if an invalid input has been given by the user
    command = ""  # user input
    msg = "Option: "  # the msg given to the user to ask for input
    sys.stdout.write(
        f"0.0%\nType [e] for exit, [n] for next, [p] for previous.\n{msg}"
    )
    while True:
        current_time = (
            round(time.monotonic(), T_PRECISION) * SPEED - start_time
        )  # records how many time has passed since the timer started
        if (current_time >= s_length):
            return "N"
        else:
            if error_bool == True:
                error_time_c = (
                    round(time.monotonic(), T_PRECISION)
                    * SPEED - error_time_s
                )
            if (error_time_c > 10):
                error_bool = False
                error_time_s = 0
                error_time_c = 0
                sys.stdout.write(f"\033[B\r\033[K\033[1A\r\033[{len(msg)}C")
                #to explain stdout.write, consider the following
                #{
                #0.0%
                #Type [e] for exit, [n] for next, [p] for previous.
                #Option: [Cursor is here]
                #Error message
                #}
                #\033[B moves cursor down a line
                #\r moves cursor to the start of the line
                #\033[K wipes the line from the current cursor position
                #\033[1A moves the cursor up one line
                #\r moves the cursor to the start of the line
                #\033[{len(msg)}C moves cursor to the right, after "Option: "
                #that is why msg is stored as a string, to calculate its
                # length and move to the right length units
                #this returns cursor to the original position 
            if (
                round(current_time - past_time, T_PRECISION)
                > 10 ** (-T_PRECISION)
            ):  
                past_time = current_time
                ptg = round(
                    past_time / s_length * 100, 1
                )  # calculates the completion percentage
                sys.stdout.write(f"\033[2A\r\033[K{ptg}%"
                                 f"\033[2B\r\033[{len(msg)}C")
                sys.stdout.flush()
                # flush updates the changes made by stdout.write()
            if msvcrt.kbhit():  # checks if the user has hit a key
                command = msvcrt.getche()
                command = command.decode(
                    encoding="ascii"
                )  # since the character is stored as bytes,
                #it needs to be converted to a string.
                command = (
                    command.upper()
                )  # converts command string to uppercase to facilitate match
            match command:
                case "N":
                    return "N"  # next
                case "":
                    continue
                case "P":
                    return "P"  # previous
                case "E":
                    return "E"  # exit
                case _:
                    sys.stdout.write(
                        f"\n{command} is NOT AN OPTION\033[1A"
                        f"\r\033[{len(msg)}C\033[K"
                    )
                    sys.stdout.flush()
                    error_bool = True
                    error_time_s = (
                        round(time.monotonic(), T_PRECISION) * SPEED
                    )  # start error timer
                    command = ""  # resets command


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
    option = ""
    i = start_s  # count variable 1, for the current song
    j = i + 1  # count variable 2, for the next song
    pl = pl_list[pl]  # creates a local copy of the playlist
    print("\n" * 6, end="")
    while option != "E":
        sys.stdout.write(
            "\r\033[K\033[A\r\033[K\033[A\r\033[K\033[A\r\033[K\033[A\r\033[K"
        )  # clears the past 5 lines
        sys.stdout.flush()  # applies changes if they had not been applied yet
        if (
            i > len(pl) - 1
        ):  # checks if i is bigger than list length to avoid range errors
            i = 1  # return i to the first song position
        elif (i < 1):
            # if i is lower than 1, which is the lowest position that stores
            # songs, it moves it back up to the end of the list
            i = len(pl) - 1
        if j > len(pl) - 1:  # same for j
            j = 1
        elif j < 1:
            j = len(pl) - 1
        title = s_list[pl[i]][2]  # looks for title of current song
        artist = s_list[pl[i]][3]  # looks for artist of current song
        sec = s_list[pl[i]][1]  # looks for duration of current song
        title2 = s_list[pl[j]][2]  # looks for title of next song
        artist2 = s_list[pl[j]][3]  # looks for artist of next song
        min = int(sec // 60)  # calculates minutes from the seconds
        sec = str(int(sec - min * 60))  # calculates the remaining seconds
        if (len(sec) == 1):
            sec = '0' + sec
        print(
            f"NOW PLAYING {title} BY {artist} - {min}:{sec}"
        )  # prints info of current song
        print(f"Next, {title2} by {artist2}")  # prints info of next song
        if (s_list[pl[i]][0]):
            try:  # check if address stores songs
                song = ps.playsound(
                    s_list[pl[i]][0], block=False
                )  # using playsound (ps) library, create playback object
                option = playback(
                    s_list[pl[i]][1]
                )  # saves the return value of playback()
                if (song.is_alive()):
                    song.stop()
            except:
                option = playback(s_list[pl[i]][1])
        else:
            option = playback(s_list[pl[i]][1])
        match option:
            case "N":  # moves to the next song
                i += 1
                j += 1
            case "P":  # moves to the previous song
                i -= 1
                j -= 1
    print("\n")


def del_pl_songs(pl, s_list, pl_list):
    """
    function for deleting songs in playlist
    input: playlist position in pl_list, song list,
        playlist list (system), songs to delete (user)
    output: changed playlist (system)
    1. display songs in playlist
    2. ask for a song to delete
    3. ask for confirmation
    4. remove song from playlist
    5. ask if user wants to continue deleting songs, if so, return to 1
    """
    next = True
    while next and len(pl_list[pl]) > 1:
        song_index = choose_s(
            pl, s_list, pl_list,
            "Which song to delete [type the number]: "
            )
        msg_c = (f"Delete {s_list[pl_list[pl][song_index]][2]} "
                 f"from {pl_list[pl][0]} [Y/N]: ")
        msg_cont = "Continue deleting songs? [Y/N]: "
        while True:
            confirm = cl_strinput(msg_c)
            confirm = confirm.lower()
            match confirm:
                case "y":
                    pl_list[pl].pop(song_index)
                    break
                case "n":
                    break
                case _:
                    invalid_option(
                        "choose a valid option".upper()
                    )
        not_invalid_option()
        while True:
            cont = cl_strinput(msg_cont) # continue
            cont = cont.lower()
            match cont:
                case "y":
                    next = True
                    break
                case "n":
                    next = False
                    break
                case _:
                    invalid_option(
                        "choose a valid option".upper()
                    )
        not_invalid_option()


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
        confirm = cl_strinput(
            f"Change playlist name from {pl_list[pl][0]} to "
            f"{name} [Y]es/[N]o/[R]ename: "
        )
        confirm = confirm.lower()
        match confirm:
            case "y":
                pl_list[pl][0] = name
                break
            case "n":
                break
            case "r":
                not_invalid_option()
                continue
            case _:
                invalid_option(
                    "not a valid option".upper()
                )
    not_invalid_option()


def del_pl(pl, pl_list):
    """
    function for deleting playlist from playlist list
    input: playlist to delete, playlist list (system), confirmation (user)
    output: deletion of playlist from playlist list
    1. ask user for confirmation
    2. if they really want to do it, delete playlist from playlist list
    """
    while True:
        confirm = cl_strinput(
            f"Do you really want to delete {pl_list[pl][0]}. "
            "This action cannot be undone. [Y/N]: "
        )
        confirm = confirm.lower()
        match confirm:
            case "y":
                pl_list.pop(pl)
                break
            case "n":
                break
            case _:
                invalid_option(
                    "not a valid option".upper()
                )
    not_invalid_option()


def edit_pl_menu(s_list, pl_list):
    """
    function for choosing which way to edit a playlist
    input: song list, playlist list (system), action (user)
    output: no output (unless an unvalid answer is given)
    1. display functions
    2. ask for action
    3. call the corresponding function
    """
    print("\nPlaylist editing menu".upper())
    pl = choose_pl(pl_list) - 1
    print("\n1. Delete songs")
    print("2. Add songs")
    print("3. Change name")
    print("4. Delete playlist")
    print("[e]. Return")
    msg = "Choose an option: "
    while True:
        act = cl_strinput(msg)
        act = act.lower()
        match act:
            case "1":
                if len(pl_list[pl]) > 1:
                    del_pl_songs(pl, s_list, pl_list)
                else:
                    print("not enough songs in playlist")
                    input("press enter to continue".upper())
                break
            case "2":
                if len(s_list) > 0:
                    add_song(pl_list[pl], s_list)
                else:
                    print("there are no songs to add")
                    input("press enter to continue".upper())
                break
            case "3":
                ed_pl_name(pl, pl_list)
                break
            case "4":
                del_pl(pl, pl_list)
                break
            case "e":
                break
            case _:
                invalid_option("not a valid option".upper())
    not_invalid_option()


def del_songs(s_list, pl_list):
    """
    function for deleting songs from system memory
    input: song list, playlist list (system), song to delete (user)
    output: song deleted from song list and playlists, playlists
        are also modified to account for the new song list order
    1. ask for song to delete
    2. ask for confirmation
    3. delete the song from song list
    4. delete the song from playlists
    5. shift positions stored in playlists to account for new song order
    """
    print_list = [
        ["SONGS"]
    ]  # a simulated matrix is created so choose_s() can be reused.
    for i in range(len(s_list)):
        print_list[0].append(i)
    del_s = choose_s(
        0,
        s_list,
        print_list,
        "Which song to delete "
        "[this will also delete it from any playlists]: "
    )
    del_s -= 1  # removes one to discard the position occupied by "SONGS"
    msg = "\033[KAre you sure? [Y/N]: "
    while True:
        confirm = cl_strinput(msg)
        confirm = confirm.lower()
        match confirm:
            case "y":
                s_list.pop(del_s)
                for i in range(len(pl_list)):
                    try:
                        while True:
                            pl_list[i].remove(del_s)
                            # removes instances of the deleted song one by one
                    except:
                        for j in range(1, len(pl_list[i])):  
                            # accesses playlist; 0 stores the name
                            if pl_list[i][j] > del_s:
                                pl_list[i][j] -= 1
                break
            case "n":
                break
            case _:
                invalid_option("not a valid input")
    not_invalid_option()


def edit_m_menu(s_list, pl_list):
    """
    function that serves as main (m) editing (edit) menu (menu),
    displays main options available
    input: song list, playlist list (system), action (user)
    output: no real output (unless an unvalid answer is given),
        function calls other functions
    1. display options
    2. ask for action
    3. call corresponding function
    """
    print("\n1. Edit playlists")
    print("2. Delete songs")
    msg = "Choose an option: "
    while True:
        act = cl_strinput(msg)
        act = act.lower()
        match act:
            case "1":
                not_invalid_option()
                if len(pl_list) > 0:
                    edit_pl_menu(s_list, pl_list)
                else:
                    print("not enough playlists")
                    input("press enter to continue".upper())
                break
            case "2":
                not_invalid_option()
                if len(s_list) > 0:
                    del_songs(s_list, pl_list)
                else:
                    print("not enough songs")
                    input("press enter to continue".upper())
                break
            case _:
                invalid_option("not a valid option".upper())


def main():
    """
    main program function.
    It handles menus and calls other functions to run the program loop.
    It also calls the functions to read and write files in between sessions.
    inputs: None per se
    Outputs: None per se
    """
    songs, playlists = read_file()
    while True:
        act = action_menu()
        match act:
            case "1":
                register_menu(songs)
            case "2":
                if (len(songs) > 0):
                    pl_creation(playlists, songs)
                else:
                    print("not enough songs to do that")
                    input("press enter to continue".upper())
            case "3":
                edit_m_menu(songs, playlists)
            case "4":
                if (len(playlists) > 0):
                    try:
                        song, pl = playback_selection(playlists, songs)
                        pl_playback(song, pl, playlists, songs)
                    except:
                        print(
                            "", end=""
                        )  # try block breaks when an invalid answer is given
                else:
                    print("not enough playlists")
                    input("press enter to continue".upper())
            case "e":
                break
            case _:
                print("not a valid option")
                input("press enter to continue".upper())
        print("\n", end="")
    write_file(songs, playlists)


main()
