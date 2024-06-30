from tkinter import *
import time

window = Tk()

selected_number = None

def back_button_function(current_frame, previous_frame): 
    current_frame.grid_remove()
    previous_frame.grid()

def easy_command():
    #Bring the board 
    home_frame.grid_remove()
    easy_saved_games_list_frame.grid()
    back_button = Button(easy_saved_games_list_frame, text = "Back", command = lambda: back_button_function(easy_saved_games_list_frame, home_frame))
    back_button.grid(row = 0, column = 0)

    file_path = "D:\projects\sudoku\easy_games.txt"
    lines = 0

    with open(file_path, "r") as file:
        for line in file:
            lines += 1

    game_load_buttons = []
    for i in range(lines):
        game_load_button = Button(easy_saved_games_list_frame, text = "Game {0}".format(i+1), command= lambda index_num = i: load_games(index_num))
        game_load_button.grid(row = i + 1, column=0)
        game_load_buttons.append(game_load_button)

def load_games(line_number):
    easy_saved_games_list_frame.grid_remove()
    game_frame.grid()
    back_button = Button(game_frame, text = "Back", command = lambda: back_button_function(game_frame, easy_saved_games_list_frame))
    back_button.grid(row = 0, column = 0)

    solve_button = Button(game_frame, text = "Solve", command=solve_sudoku)
    solve_button.grid(row = 1, column = 2)

    print_board(game_frame)

    game_index = None

    with open("D:\projects\sudoku\easy_games.txt", "r") as file:
        games = file.readlines()
        game_index = games[line_number]

    index = 0
    for i in range(9):
        for j in range(9):
            if game_index[index] == "0":
                buttons[i][j].config(text = "")
            else:
                buttons[i][j].config(text = game_index[index])
            index += 1
        
def number_command(number):
    #select the number in number buttons
    global selected_number
    selected_number = number

buttons = [[None for a in range(9)] for b in range(9)]
number_buttons = [None for a in range(9)]

def print_board(frame):
    board_frame = Frame(frame)
    board_frame.grid(row=1, column= 0)

    global number_frame
    number_frame = Frame(frame)
    number_frame.grid(row=2, column=0)

    for i in range(9):
        for j in range(9):
            button = Button(board_frame, text="", height=1, width=2, command= lambda row = i, column = j: board_command(row, column))
            button.grid(row=i, column=j, padx=5, pady=5)
            buttons[i][j] = button

    number = 1
    for i in range(9):
        button = Button(number_frame, text=str(number), height=1, width=2, command= lambda num = number: number_command(num))
        button.grid(row=1,column=i, padx=5)
        number_buttons.append(button)
        number += 1
    
    eraser_button = Button(number_frame, text="E", height=1, width=2, command= lambda: number_command(""))
    eraser_button.grid(row = 2, column = 0, columnspan=9)

def board_command(r, c):
    # Input number into the board from the number buttons.
    buttons[r][c].config(text=str(selected_number))

    if selected_number == "":
        # Reset the background color to the default (empty string)
        buttons[r][c].config(bg="#f0f0f0")

    check_board(r, c, str(selected_number))

possible = True
game_finished = False

def check_victory():
    score = 0
    for i in range(9):
        for j in range(9):
            if buttons[i][j].cget("text") != "":
                if buttons[i][j].cget("bg") != "red":
                    score +=1
    
    if score == 81:
        return True

def check_board(r, c, n):
    #check the numbers being entered in the squares
    global number_frame

    #check columns
    for i in range(9):
        if buttons[r][i].cget("text") == str(n):
            return False
                
    for i in range(9):
        if buttons[i][c].cget("text") == str(n):
            return False
        
    #check 3X3 sections
    x = (r//3) * 3
    y = (c//3) * 3
    for i in range(x, x + 3):
        for j in range(y, y + 3):
            if buttons[i][j].cget("text") == str(n):
                return False
    
    return True
                    
    # if check_victory():
    #     winning_label = Label(number_frame, text = "You Win!!!")
    #     winning_label.grid(row=3, column=5)

def open_set_game_frame():
    home_frame.grid_remove()
    set_game_frame.grid()
    back_button = Button(set_game_frame, text = "Back", command = lambda: back_button_function(set_game_frame, home_frame))
    back_button.grid(row = 0, column = 0)
    print_board(set_game_frame)

    set_game_button_ = Button(set_game_frame, text = "Set Game", command = set_game_function)
    set_game_button_.grid(row=0, column=1)

def set_game_function():
    
    game = [""] * 81  # Initialize the game list with 81 empty strings

    for i in range(9):
        for j in range(9):
            text = buttons[i][j].cget("text")
            if text:
                game[i * 9 + j] = text
            else: 
                game[i * 9 + j] = "0"

    with open("easy_games.txt", "a") as file:
        file.write("".join(game) + "\n")
it = 0
def console(gird):
        for line in gird:
            print(line)
def solve_sudoku():
    for i in range(9):
        for j in range(9):
            text = buttons[i][j].cget("text")
            if text == "":
                for n in range(1, 10):  
                    if check_board(i, j, n):
                        buttons[i][j].config(text = str(n))
                        if solve_sudoku():
                            return True
                        buttons[i][j].config(text = "")
                return False
    return True

    

global game_frame 
easy_saved_games_list_frame = Frame(window)
game_frame = Frame(window)

home_frame = Frame(window)
home_frame.grid()

set_game_frame = Frame(window)

#game buttons 
easy_button = Button(home_frame, text = "Easy", command=easy_command)
medium_button = Button(home_frame, text = "Medium")
hard_button = Button(home_frame, text = "Hard")
very_hard_button = Button(home_frame, text = "Very Hard")
set_game_button = Button(home_frame, text = "Set Games", command=open_set_game_frame)

easy_button.grid()
medium_button.grid()
hard_button.grid()
very_hard_button.grid()
set_game_button.grid()

window.mainloop()