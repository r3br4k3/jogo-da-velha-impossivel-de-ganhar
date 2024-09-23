import tkinter as tk
from tkinter import messagebox
import random

def check_winner(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
            return True
    return False

def get_empty_cells(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

def minimax(board, depth, is_maximizing, difficulty):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if not get_empty_cells(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for (r, c) in get_empty_cells(board):
            board[r][c] = "O"
            score = minimax(board, depth + 1, False, difficulty)
            board[r][c] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for (r, c) in get_empty_cells(board):
            board[r][c] = "X"
            score = minimax(board, depth + 1, True, difficulty)
            board[r][c] = " "
            best_score = min(score, best_score)
        return best_score

def best_move(board, difficulty):
    if always_win:
        return random.choice(get_empty_cells(board))
    if difficulty == "Fácil":
        return random.choice(get_empty_cells(board))
    elif difficulty == "Médio":
        if random.random() < 0.5:
            return random.choice(get_empty_cells(board))
    best_score = -float("inf")
    move = None
    for (r, c) in get_empty_cells(board):
        board[r][c] = "O"
        score = minimax(board, 0, False, difficulty)
        board[r][c] = " "
        if score > best_score:
            best_score = score
            move = (r, c)
    return move

def on_click(row, col):
    if board[row][col] == " " and not game_over:
        board[row][col] = "X"
        buttons[row][col].config(text="X", state="disabled", disabledforeground="lightblue")
        if check_winner(board, "X"):
            messagebox.showinfo("Fim de Jogo", "Você ganhou!")
            reset_board()
            return
        if not get_empty_cells(board):
            messagebox.showinfo("Fim de Jogo", "Empate!")
            reset_board()
            return

        move = best_move(board, difficulty.get())
        if move:
            board[move[0]][move[1]] = "O"
            buttons[move[0]][move[1]].config(text="O", state="disabled", disabledforeground="lightcoral")
            if check_winner(board, "O"):
                if always_win:
                    messagebox.showinfo("Fim de Jogo", "Você ganhou!")
                else:
                    messagebox.showinfo("Fim de Jogo", "Você perdeu!")
                reset_board()
                return

def reset_board():
    global board, game_over
    board = [[" " for _ in range(3)] for _ in range(3)]
    game_over = False
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text=" ", state="normal")
    if first_player.get() == "Computador":
        move = best_move(board, difficulty.get())
        board[move[0]][move[1]] = "O"
        buttons[move[0]][move[1]].config(text="O", state="disabled", disabledforeground="lightcoral")

def check_password():
    global always_win
    if password_entry.get() == "ganhar":
        always_win = True
        messagebox.showinfo("Senha Correta", "Modo de vitória garantida ativado!")
    else:
        always_win = False
        messagebox.showerror("Senha Incorreta", "Senha incorreta. Tente novamente.")

root = tk.Tk()
root.title("Jogo da Velha")
root.configure(bg="black")

board = [[" " for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
game_over = False
always_win = False

difficulty = tk.StringVar(value="Impossível")
first_player = tk.StringVar(value="Humano")

for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(root, text=" ", width=10, height=3, font=('Helvetica', 20), bg="gray", fg="white", command=lambda r=row, c=col: on_click(r, c))
        buttons[row][col].grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

reset_button = tk.Button(root, text="Reiniciar", font=('Helvetica', 14), bg="darkgray", fg="white", command=reset_board)
reset_button.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

difficulty_label = tk.Label(root, text="Dificuldade:", font=('Helvetica', 14), bg="black", fg="white")
difficulty_label.grid(row=4, column=0, pady=10)
difficulty_menu = tk.OptionMenu(root, difficulty, "Fácil", "Médio", "Difícil", "Impossível")
difficulty_menu.config(bg="darkgray", fg="white")
difficulty_menu.grid(row=4, column=1, pady=10)

first_player_label = tk.Label(root, text="Primeiro Jogador:", font=('Helvetica', 14), bg="black", fg="white")
first_player_label.grid(row=5, column=0, pady=10)
first_player_menu = tk.OptionMenu(root, first_player, "Humano", "Computador")
first_player_menu.config(bg="darkgray", fg="white")
first_player_menu.grid(row=5, column=1, pady=10)

password_label = tk.Label(root, text="Senha:", font=('Helvetica', 14), bg="black", fg="white")
password_label.grid(row=6, column=0, pady=10)
password_entry = tk.Entry(root, font=('Helvetica', 14), show="*")
password_entry.grid(row=6, column=1, pady=10)
password_button = tk.Button(root, text="Entrar", font=('Helvetica', 14), bg="darkgray", fg="white", command=check_password)
password_button.grid(row=6, column=2, pady=10)

for i in range(3):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)

root.mainloop()
