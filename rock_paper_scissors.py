import tkinter as tk
import random

# Colours
BG = "#101827"
CARD = "#1e293b"
TEXT = "#f8fafc"
MUTED = "#94a3b8"
BLUE = "#38bdf8"
GREEN = "#4ade80"
RED = "#fb7185"
YELLOW = "#facc15"

MOVES = {
    "Rock": "✊",
    "Paper": "✋",
    "Scissors": "✌"
}

BEATS = {
    "Rock": "Scissors",
    "Paper": "Rock",
    "Scissors": "Paper"
}


class RockPaperScissors:
    def __init__(self, window):
        self.window = window
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.round_number = 0
        self.busy = False
        self.timer = None

        window.title("🎮 Rock Paper Scissors")
        window.geometry("720x760")
        window.minsize(660, 720)
        window.configure(bg=BG)

        tk.Label(
            window,
            text="ROCK • PAPER • SCISSORS",
            font=("Segoe UI", 25, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=(22, 4))

        tk.Label(
            window,
            text="Choose your move and challenge the computer!",
            font=("Segoe UI", 11),
            bg=BG,
            fg=MUTED
        ).pack()

        # Scoreboard
        scoreboard = tk.Frame(window, bg=CARD)
        scoreboard.pack(fill="x", padx=28, pady=20)

        self.player_label = self.score_card(
            scoreboard, "YOU", BLUE
        )
        self.tie_label = self.score_card(
            scoreboard, "TIES", YELLOW
        )
        self.computer_label = self.score_card(
            scoreboard, "COMPUTER", RED
        )

        self.round_label = tk.Label(
            window,
            text="Round 1 • Ready?",
            font=("Segoe UI", 12, "bold"),
            bg=BG,
            fg=MUTED
        )
        self.round_label.pack()

        # Battle area
        arena = tk.Frame(window, bg=BG)
        arena.pack(fill="x", padx=35, pady=12)
        arena.columnconfigure(0, weight=1)
        arena.columnconfigure(1, weight=0)
        arena.columnconfigure(2, weight=1)

        self.player_hand = tk.Label(
            arena,
            text="❔",
            font=("Segoe UI Emoji", 66),
            bg=BG,
            fg=BLUE
        )
        self.player_hand.grid(row=0, column=0)

        tk.Label(
            arena,
            text="VS",
            font=("Segoe UI", 20, "bold"),
            bg=BG,
            fg=MUTED
        ).grid(row=0, column=1, padx=20)

        self.computer_hand = tk.Label(
            arena,
            text="❔",
            font=("Segoe UI Emoji", 66),
            bg=BG,
            fg=RED
        )
        self.computer_hand.grid(row=0, column=2)

        self.player_move = tk.Label(
            arena,
            text="Your move",
            font=("Segoe UI", 12),
            bg=BG,
            fg=TEXT
        )
        self.player_move.grid(row=1, column=0)

        self.computer_move = tk.Label(
            arena,
            text="Computer's move",
            font=("Segoe UI", 12),
            bg=BG,
            fg=TEXT
        )
        self.computer_move.grid(row=1, column=2)

        self.result_label = tk.Label(
            window,
            text="Make your move! 👇",
            font=("Segoe UI", 20, "bold"),
            bg=BG,
            fg=TEXT
        )
        self.result_label.pack(pady=(10, 3))

        self.explanation = tk.Label(
            window,
            text="Rock beats Scissors • Paper beats Rock • Scissors beats Paper",
            font=("Segoe UI", 10),
            bg=BG,
            fg=MUTED
        )
        self.explanation.pack(pady=(0, 15))

        # Move buttons
        buttons_frame = tk.Frame(window, bg=BG)
        buttons_frame.pack()

        self.move_buttons = []

        for move, emoji in MOVES.items():
            button = tk.Button(
                buttons_frame,
                text=f"{emoji}  {move}",
                font=("Segoe UI Emoji", 15),
                bg=CARD,
                fg=TEXT,
                activebackground=BLUE,
                activeforeground=BG,
                disabledforeground=MUTED,
                relief="flat",
                bd=0,
                width=11,
                pady=12,
                cursor="hand2",
                command=lambda selected=move: self.start_round(selected)
            )
            button.pack(side="left", padx=7)

            button.bind(
                "<Enter>",
                lambda event: self.hover(event, True)
            )
            button.bind(
                "<Leave>",
                lambda event: self.hover(event, False)
            )
            self.move_buttons.append(button)

        tk.Label(
            window,
            text="Keyboard shortcuts: R = Rock   P = Paper   S = Scissors",
            font=("Segoe UI", 10),
            bg=BG,
            fg=MUTED
        ).pack(pady=12)

        # Round history
        history_frame = tk.Frame(window, bg=CARD)
        history_frame.pack(fill="both", expand=True, padx=28, pady=(0, 12))

        tk.Label(
            history_frame,
            text="📜 ROUND HISTORY",
            font=("Segoe UI", 11, "bold"),
            bg=CARD,
            fg=TEXT,
            anchor="w"
        ).pack(fill="x", padx=14, pady=(10, 5))

        self.history = tk.Listbox(
            history_frame,
            height=4,
            font=("Segoe UI", 11),
            bg=CARD,
            fg=MUTED,
            selectbackground="#334155",
            relief="flat",
            bd=0,
            highlightthickness=0,
            activestyle="none"
        )
        self.history.pack(fill="both", expand=True, padx=14, pady=(0, 10))

        tk.Button(
            window,
            text="🔄  Reset Game",
            font=("Segoe UI", 11, "bold"),
            bg=BLUE,
            fg=BG,
            activebackground="#7dd3fc",
            relief="flat",
            padx=22,
            pady=9,
            cursor="hand2",
            command=self.reset_game
        ).pack(pady=(0, 18))

        window.bind("<KeyPress>", self.keyboard_move)

    def score_card(self, parent, title, colour):
        frame = tk.Frame(parent, bg=CARD)
        frame.pack(side="left", expand=True, fill="x", pady=12)

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 10, "bold"),
            bg=CARD,
            fg=MUTED
        ).pack()

        label = tk.Label(
            frame,
            text="0",
            font=("Segoe UI", 28, "bold"),
            bg=CARD,
            fg=colour
        )
        label.pack()
        return label

    def hover(self, event, entering):
        if str(event.widget["state"]) == "normal":
            event.widget.config(
                bg="#334155" if entering else CARD
            )

    def keyboard_move(self, event):
        shortcuts = {
            "r": "Rock",
            "p": "Paper",
            "s": "Scissors"
        }
        move = shortcuts.get(event.char.lower())
        if move:
            self.start_round(move)

    def set_buttons(self, enabled):
        for button in self.move_buttons:
            button.config(
                state="normal" if enabled else "disabled",
                bg=CARD
            )

    def start_round(self, player_choice):
        if self.busy:
            return

        self.busy = True
        self.set_buttons(False)

        self.round_label.config(
            text=f"Round {self.round_number + 1} • Get ready!"
        )
        self.player_move.config(text="Move locked!")
        self.computer_move.config(text="Getting ready...")
        self.explanation.config(text="Here we go...")
        self.countdown(player_choice, 0)

    def countdown(self, player_choice, step):
        self.timer = None

        animation = [
            ("✊", "Rock..."),
            ("✋", "Paper..."),
            ("✌", "Scissors...")
        ]

        if step < len(animation):
            emoji, message = animation[step]

            self.player_hand.config(text=emoji)
            self.computer_hand.config(text=emoji)
            self.result_label.config(text=message, fg=YELLOW)

            self.timer = self.window.after(
                450,
                self.countdown,
                player_choice,
                step + 1
            )
        else:
            self.show_result(player_choice)

    def show_result(self, player_choice):
        computer_choice = random.choice(list(MOVES))
        self.round_number += 1

        self.player_hand.config(text=MOVES[player_choice])
        self.computer_hand.config(text=MOVES[computer_choice])
        self.player_move.config(text=player_choice)
        self.computer_move.config(text=computer_choice)

        if player_choice == computer_choice:
            self.ties += 1
            message = "🤝 It's a tie!"
            colour = YELLOW
            reason = "Same move! Try again."
            outcome = "Tie"

        elif BEATS[player_choice] == computer_choice:
            self.player_score += 1
            message = "🎉 You win!"
            colour = GREEN
            reason = f"{player_choice} beats {computer_choice}!"
            outcome = "You won"

        else:
            self.computer_score += 1
            message = "🤖 Computer wins!"
            colour = RED
            reason = f"{computer_choice} beats {player_choice}!"
            outcome = "Computer won"

        self.result_label.config(text=message, fg=colour)
        self.explanation.config(text=reason)
        self.round_label.config(
            text=f"Round {self.round_number} complete • Choose again!"
        )

        self.player_label.config(text=str(self.player_score))
        self.computer_label.config(text=str(self.computer_score))
        self.tie_label.config(text=str(self.ties))

        record = (
            f"Round {self.round_number}:  "
            f"You {MOVES[player_choice]}  vs  "
            f"Computer {MOVES[computer_choice]}  —  {outcome}"
        )
        self.history.insert(0, record)
        self.history.itemconfig(0, fg=colour)

        # Keep the latest 20 rounds.
        if self.history.size() > 20:
            self.history.delete(20, tk.END)

        self.busy = False
        self.set_buttons(True)

    def reset_game(self):
        # Cancel any countdown still running.
        if self.timer is not None:
            self.window.after_cancel(self.timer)
            self.timer = None

        self.busy = False
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.round_number = 0

        for label in (
            self.player_label,
            self.computer_label,
            self.tie_label
        ):
            label.config(text="0")

        self.player_hand.config(text="❔")
        self.computer_hand.config(text="❔")
        self.player_move.config(text="Your move")
        self.computer_move.config(text="Computer's move")
        self.result_label.config(text="Make your move! 👇", fg=TEXT)
        self.explanation.config(
            text="Rock beats Scissors • Paper beats Rock • Scissors beats Paper"
        )
        self.round_label.config(text="Round 1 • Ready?")
        self.history.delete(0, tk.END)
        self.set_buttons(True)


if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissors(root)
    root.mainloop()