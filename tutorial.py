import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):   #we need stdscr because we need access to stuff in order to write on the screen
    stdscr.clear()
    stdscr.addstr(0,40,"~~~~~ Welcome to the Speed Typing Test! ~~~~~")
    stdscr.addstr(1,3,"\nPress any key to begin!:)\n")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1,0, f"Words per Minute: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color)   #overlaid on top of my current text


def load_from_file():
    with open("text.txt", "r") as f:
        lines = f.readlines()
    return random.choice(lines).strip()  #strip is for getting rid of backslash at the end of each line


def wpm_test(stdscr):
    target_text = load_from_file()
    current_text = []
    wpm=0
    start_time = time.time()
    stdscr.nodelay(True)  #do not delay waiting for a user to hit a key

    while True:
        time_elapsed = max(time.time() - start_time, 1) #max and 1 is for avoidind division by zero, if it is zero it will give us 1
        wpm = round((len(current_text) / (time_elapsed / 60))/5)  #equation for wpm

        stdscr.clear()
        display_text(stdscr, target_text, current_text,wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:  #convert te list into a string, you can put something between "_" and it will be displayed l-i-k-e-t-h-i-s
            stdscr.nodelay(False)   #wait for the user to hit a key
            break

        try:
            key = stdscr.getkey()  #if the user doesn't enter a key this line throws an exception
        except:
            continue

        if ord(key) == 27:  # if the user hits escape we exit, 27 is the ordinal value of escape (ASCII code)
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):  #different representations for backspace on different operating systems
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)





def main(stdscr):

    #COLORS
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   #pair 1, text green background black
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   #another pair
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)   #another pair

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)

        stdscr.addstr(2,0, "You completed the teeeeest! Congrats! Press esc to exit and anything else to play again...")
        key = stdscr.getkey()
        if ord(key) == 27:
            break

'''
    stdscr.clear()

    #CURSES EXAMPLES
    #stdscr.addstr("Hello world", curses.color_pair(2)) #reference the pair
    #stdscr.addstr(1,0,"Hello world!")  #start one line down and to the right, if you put something with 1,5 before, the second one will overwrite and we will use this


    stdscr.refresh()

    #TO GET THE KEY THAT THE USER TYPED IN
    key=stdscr.getkey()
    print(key)
'''


wrapper(main)
