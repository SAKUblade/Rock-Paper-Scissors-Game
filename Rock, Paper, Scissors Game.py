import random
import tkinter as tk


class RockPaperScissorsApp:
    OPTIONS = {
        "rock": "✊",
        "paper": "✋",
        "scissors": "✌",
    }
    SHAKE_SEQUENCE = ["✊", "✋", "✌", "✋", "✊", "✌"]

    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors - Cyberpunk Purple")
        self.root.geometry("1000x650")
        self.root.minsize(900, 580)

        # Aesthetic cyberpunk purple palette
        self.c = {
            "bg": "#0A0614",
            "card": "#15102A",
            "border": "#5D33A8",
            "title": "#DFA8FF",
            "text": "#F2E9FF",
            "muted": "#BDAAD8",
            "player": "#B983FF",
            "score": "#FF8CF4",
            "btn": "#2A1A4D",
            "btn_hover": "#442A7A",
            "btn_active": "#6A42B5",
            "info": "#86E8FF",
            "win": "#65FF9A",
            "lose": "#FF6F90",
            "tie": "#FFD86A",
        }

        self.root.configure(bg=self.c["bg"])

        self.player_name = ""
        self.player_score = 0
        self.computer_score = 0
        self.tie_score = 0
        self.animating = False
        self.player_icon = "?"
        self.computer_icon = "?"

        self._build_start()

    def _clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def _hover(self, button, normal, hover):
        button.bind("<Enter>", lambda _: button.config(bg=hover))
        button.bind("<Leave>", lambda _: button.config(bg=normal))

    def _build_start(self):
        self._clear()

        wrap = tk.Frame(self.root, bg=self.c["bg"])
        wrap.pack(expand=True, fill="both", padx=40, pady=35)

        card = tk.Frame(
            wrap,
            bg=self.c["card"],
            highlightthickness=1,
            highlightbackground=self.c["border"],
            padx=48,
            pady=48,
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card,
            text="CYBERPUNK RPS ARENA",
            font=("Segoe UI Semibold", 34),
            bg=self.c["card"],
            fg=self.c["title"],
        ).pack(pady=(0, 10))

        tk.Label(
            card,
            text="Enter your name to start",
            font=("Segoe UI", 14),
            bg=self.c["card"],
            fg=self.c["muted"],
        ).pack(pady=(0, 22))

        self.name_entry = tk.Entry(
            card,
            font=("Segoe UI", 16),
            width=24,
            justify="center",
            relief="flat",
            bg="#20163A",
            fg=self.c["text"],
            insertbackground=self.c["text"],
        )
        self.name_entry.pack(ipady=8, pady=(0, 20))
        self.name_entry.focus_set()

        start_btn = tk.Button(
            card,
            text="Start Game",
            font=("Segoe UI Semibold", 15),
            padx=28,
            pady=11,
            relief="flat",
            bd=0,
            cursor="hand2",
            bg="#6A42B5",
            fg="white",
            activebackground="#8758E8",
            activeforeground="white",
            command=self._start_game,
        )
        start_btn.pack()
        self._hover(start_btn, "#6A42B5", "#8758E8")

        self.root.bind("<Return>", self._start_game)

    def _start_game(self, _event=None):
        self.player_name = self.name_entry.get().strip() or "Player"
        self.player_score = 0
        self.computer_score = 0
        self.tie_score = 0
        self.root.unbind("<Return>")
        self._build_game()

    def _card(self, parent, title):
        card = tk.Frame(
            parent,
            bg=self.c["card"],
            highlightthickness=1,
            highlightbackground=self.c["border"],
            padx=22,
            pady=22,
        )
        tk.Label(
            card,
            text=title,
            font=("Segoe UI Semibold", 18),
            bg=self.c["card"],
            fg=self.c["text"],
        ).pack(pady=(0, 10))
        return card

    def _build_game(self):
        self._clear()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        shell = tk.Frame(self.root, bg=self.c["bg"], padx=26, pady=20)
        shell.grid(sticky="nsew")
        shell.grid_columnconfigure(0, weight=1)
        shell.grid_rowconfigure(1, weight=1)

        header = tk.Frame(
            shell,
            bg=self.c["card"],
            highlightthickness=1,
            highlightbackground=self.c["border"],
            padx=20,
            pady=14,
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        header.grid_columnconfigure((0, 1, 2), weight=1)

        tk.Label(
            header,
            text=f"Player: {self.player_name}",
            font=("Segoe UI Semibold", 15),
            bg=self.c["card"],
            fg=self.c["player"],
        ).grid(row=0, column=0, sticky="w")

        tk.Label(
            header,
            text="Rock Paper Scissors",
            font=("Segoe UI Semibold", 18),
            bg=self.c["card"],
            fg=self.c["title"],
        ).grid(row=0, column=1)

        self.score_lbl = tk.Label(
            header,
            text="You 0 : 0 Computer | Tie: 0",
            font=("Segoe UI Semibold", 15),
            bg=self.c["card"],
            fg=self.c["score"],
        )
        self.score_lbl.grid(row=0, column=2, sticky="e")

        body = tk.Frame(shell, bg=self.c["bg"])
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure((0, 1), weight=1)
        body.grid_rowconfigure(0, weight=1)

        self.player_card = self._card(body, self.player_name)
        self.player_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=(0, 14))

        self.computer_card = self._card(body, "Computer")
        self.computer_card.grid(row=0, column=1, sticky="nsew", padx=(12, 0), pady=(0, 14))

        self.player_hand = tk.Label(
            self.player_card, text="?", font=("Segoe UI Emoji", 82), bg=self.c["card"], fg="#D8B9FF"
        )
        self.player_hand.pack(expand=True, pady=(8, 4))

        self.player_txt = tk.Label(
            self.player_card, text="Waiting for move...", font=("Segoe UI", 13), bg=self.c["card"], fg=self.c["muted"]
        )
        self.player_txt.pack()

        self.computer_hand = tk.Label(
            self.computer_card, text="?", font=("Segoe UI Emoji", 82), bg=self.c["card"], fg="#FFBEF7"
        )
        self.computer_hand.pack(expand=True, pady=(8, 4))

        self.computer_txt = tk.Label(
            self.computer_card, text="Waiting for move...", font=("Segoe UI", 13), bg=self.c["card"], fg=self.c["muted"]
        )
        self.computer_txt.pack()

        self.result_lbl = tk.Label(
            shell,
            text="Choose your move to start!",
            font=("Segoe UI Semibold", 24),
            bg=self.c["bg"],
            fg=self.c["tie"],
        )
        self.result_lbl.grid(row=2, column=0, pady=(0, 16))

        bar = tk.Frame(shell, bg=self.c["bg"])
        bar.grid(row=3, column=0, sticky="ew")
        bar.grid_columnconfigure((0, 1, 2), weight=1)

        self.move_buttons = []
        for i, (move, icon) in enumerate(self.OPTIONS.items()):
            btn = tk.Button(
                bar,
                text=f"{icon}  {move.title()}",
                font=("Segoe UI Semibold", 16),
                relief="flat",
                bd=0,
                padx=14,
                pady=14,
                cursor="hand2",
                bg=self.c["btn"],
                fg=self.c["text"],
                activebackground=self.c["btn_active"],
                activeforeground="white",
                command=lambda m=move: self._play_round(m),
            )
            btn.grid(row=0, column=i, sticky="ew", padx=10)
            self._hover(btn, self.c["btn"], self.c["btn_hover"])
            self.move_buttons.append(btn)

    def _set_buttons(self, enabled):
        st = tk.NORMAL if enabled else tk.DISABLED
        for b in self.move_buttons:
            b.config(state=st)

    def _play_round(self, player_choice):
        if self.animating:
            return

        self.animating = True
        computer_choice = random.choice(list(self.OPTIONS.keys()))
        self.player_icon = self.OPTIONS[player_choice]
        self.computer_icon = self.OPTIONS[computer_choice]

        self.player_txt.config(text="Shaking...")
        self.computer_txt.config(text="Shaking...")
        self.result_lbl.config(text="Rock... Paper... Scissors...", fg=self.c["info"])
        self._set_buttons(False)

        self._shake(0, 12, player_choice, computer_choice)

    def _shake(self, frame, max_frames, player_choice, computer_choice):
        icon = self.SHAKE_SEQUENCE[frame % len(self.SHAKE_SEQUENCE)]
        self.player_hand.config(text=icon)
        self.computer_hand.config(text=icon)

        if frame < max_frames:
            self.root.after(90, lambda: self._shake(frame + 1, max_frames, player_choice, computer_choice))
            return

        self.player_hand.config(text=self.player_icon)
        self.computer_hand.config(text=self.computer_icon)
        self.player_txt.config(text=f"{self.player_name} chose {player_choice.title()}")
        self.computer_txt.config(text=f"Computer chose {computer_choice.title()}")

        self._resolve(player_choice, computer_choice)
        self.animating = False
        self._set_buttons(True)

    def _resolve(self, p, c):
        if p == c:
            self.tie_score += 1
            self.result_lbl.config(text="It's a Tie!", fg=self.c["tie"])
        elif (p == "rock" and c == "scissors") or (p == "paper" and c == "rock") or (p == "scissors" and c == "paper"):
            self.player_score += 1
            self.result_lbl.config(text=f"{self.player_name} Wins!", fg=self.c["win"])
        else:
            self.computer_score += 1
            self.result_lbl.config(text="Computer Wins!", fg=self.c["lose"])

        self.score_lbl.config(
            text=f"You {self.player_score} : {self.computer_score} Computer | Tie: {self.tie_score}"
        )


def main():
    root = tk.Tk()
    RockPaperScissorsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()