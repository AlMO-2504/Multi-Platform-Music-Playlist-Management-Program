import time
import sys
import msvcrt
"""
Playlist manager
AlMoOl

The following program is a prototype that should be able of registering songs, creating playlists, and playing back playlists
Currently, the program should work similarly to the final product, i. e., functions work with one another, but data storage is still local and editing playlists and registered songs is not an available option yet
Data storage:
Songs info is stored in a matrix, where one element is the song info. For each list of song info, the data is order in the following way:
1. filepath
2. length (in seconds)
3. title
4. author
For playlists, playlists are stored in a playlist matrix. Inside a playlist, the playlist name is always the first element; also, songs are not stored themselves, but rather, their position (in list, so position 1 is 0)in the main song list:
For example: p_list[0] = ["name", 1, 7, 5]
"""

# establishing main matrices
"""
for the final delivery, this will be stored inside the computer not the code.
however, this way of handling the main data works for the prototype.
furthermore, filepaths are not yet implemented, but a blank element will be left in their place as to facilitate later improvements
"""
s_list = [
    ['', 441, "zen ball master", "glenn powell"],
    ['', 331, "jezebel", "sade"],
    ['', 81, "green eggs and jam", "dunkey"],
    ['', 252, "georgy porgy", "toto"]
]
pl_list = [
    ["dummy", 1, 2, 0, 3]
]

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
    print("1. register song") # display menu actions
    print("2. create playlist")
    print("3. edit playlist")
    print("4. playback playlists")
    print("[e]. Type e to exit")
    action = str(input("Choose an option: ")) # convert to string
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
        dur = str(input("duration [min:sec]: ")) # duration in 00:00
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

def register_menu():
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
    title = str(input("song title: "))
    artist = str(input("artist name: "))
    duration = get_min_sec()
    directory = ' '
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

def pl_creation():
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
    pl_name = str(input("playlist name: "))
    new_pl = [pl_name]
    song_added = False # if user has given a valid song to add
    cont = True # continue, if the user wants to continue
    value_error = False # if there has been a value error
    range_error = False # if there has been a range error
    c_error = False # if the continue input is not a valid or there has been an error with it
    while (cont == True):
        while (song_added == False):
            disp_avlbl_songs(s_list, new_pl)
            if(value_error == True):
                print("please, type a number".upper())
                value_error = False
            elif(range_error == True):
                print("please, choose one number from the given list".upper())
                range_error =  False
            s = input(f"type the number of the song to add to {new_pl[0]}: ") # 0 stores pl name
            if(valid_input(s, int) == True):
                s = int(s)
                range_error = not valid_range(s, 1, len(s_list), '[]') # valid_range return False if there has been an error and true otherwise, inverting the valuable helps readability
                if(range_error == False):
                    new_pl.append(s-1) # s is given in natural numbers, positions start at 0
                    song_added = True
            else:
                value_error = True
        if(c_error == True):
            print("Type either Y or N".upper())
            c_error = False
        c = str(input("Would you like to add another song [Y/N]? ")) # continue value
        match c.upper():
            case 'Y':
                cont = True
                song_added = False
            case 'N':
                cont = False
            case _:
                c_error = True
    pl_list.append(new_pl)
    return
                
def edit_pl_menu():
    print("not available yet")
    return

def disp_pl(pl):
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

def disp_pl_list():
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

def playback_selection():
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
    disp_pl_list()
    while True:
        pl = input("Which playlist: ")
        v_inp = valid_input(pl, int)
        if(v_inp == False):
            print("type the number of the playlist".upper())
        else:
            pl = int(pl)
            v_range = valid_range(pl, 1, len(pl_list), '[]')
            if(v_range == False):
                print("select a number from the given list".upper())
            else:
                break
    pl = pl - 1 # answers are given in natural numbers, positions start at 0
    disp_pl(pl)
    while True:
        song = input("Which song to start from: ")
        v_inp = valid_input(song, int)
        if(v_inp == False):
            print("type the number of the song".upper())
        else:
            song = int(song)
            v_range = valid_range(song, 1, len(pl_list[pl]), '[)')
            if(v_range == False):
                print("select a number from the given list".upper())
            else:
                break
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

def pl_playback(start_s, pl):
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

def main():
    while True: 
        act = action_menu()
        match act:
            case '1':
                register_menu()
            case '2':
                pl_creation()
            case '3':
                edit_pl_menu()
            case '4':
                song, pl = playback_selection()
                pl_playback(song, pl)
            case 'e':
                break
            case _:
                print("not an option\n".upper())
        print("\n", end="")
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
