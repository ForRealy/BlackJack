import tkinter as tk
from tkinter import ttk, messagebox, Canvas
import random
import sys
import os
from PIL import Image, ImageDraw, ImageFont, ImageTk
import json
import customtkinter as ctk
from pytablericons import TablerIcons, OutlineIcon
from datetime import datetime


class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg="#1a1a2e")

        # Set CustomTkinter appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Language settings
        self.current_language = "en"
        self.translations = {
            "en": {
                "title": "Blackjack",
                "dealer_hand": "Dealer's Hand",
                "player_hand": "Your Hand",
                "money": "Money: $",
                "bet_amount": "Bet Amount",
                "deal": "Deal",
                "hit": "Hit",
                "stand": "Stand",
                "invalid_bet": "Invalid bet amount!",
                "enter_valid_bet": "Please enter a valid bet amount!",
                "dealer_wins": "Dealer wins!",
                "player_wins": "You win!",
                "push": "Push!",
                "dealer_bust": "Dealer busts!",
                "player_bust": "Player busts!",
                "game_in_progress": "Game is in progress. Cannot reset money.",
                "enter_name": "Please enter a name.",
                "name_submitted": "Name submitted successfully!",
                "reset_warning": "⚠️ Reset will end current game!",
                "confirm_reset": "Confirm Reset",
                "cancel": "Cancel",
                "money_reset": "💰 Money Reset!",
                "reset_cancelled": "Reset cancelled"
            },
            "es": {
                "title": "Blackjack",
                "dealer_hand": "Mano del Crupier",
                "player_hand": "Tu Mano",
                "money": "Dinero: $",
                "bet_amount": "Cantidad a Apostar",
                "deal": "Repartir",
                "hit": "Pedir",
                "stand": "Plantarse",
                "invalid_bet": "¡Apuesta inválida!",
                "enter_valid_bet": "¡Por favor, ingrese una apuesta válida!",
                "dealer_wins": "¡Gana el Crupier!",
                "player_wins": "¡Tú ganas!",
                "push": "¡Empate!",
                "dealer_bust": "¡El Crupier se pasó!",
                "player_bust": "¡Te pasaste!",
                "game_in_progress": "El juego está en progreso. No se puede reiniciar el dinero.",
                "enter_name": "Por favor, ingrese un nombre.",
                "name_submitted": "Nombre enviado exitosamente!",
                "reset_warning": "⚠️ ¡El reinicio terminará la partida actual!",
                "confirm_reset": "Confirmar Reinicio",
                "cancel": "Cancelar",
                "money_reset": "💰 ¡Dinero Reiniciado!",
                "reset_cancelled": "Reinicio cancelado"
            },
            "pt": {
                "title": "Blackjack",
                "dealer_hand": "Mão do Dealer",
                "player_hand": "Sua Mão",
                "money": "Dinheiro: $",
                "bet_amount": "Valor da Aposta",
                "deal": "Distribuir",
                "hit": "Pedir",
                "stand": "Parar",
                "invalid_bet": "Aposta inválida!",
                "enter_valid_bet": "Por favor, insira uma aposta válida!",
                "dealer_wins": "Dealer vence!",
                "player_wins": "Você vence!",
                "push": "Empate!",
                "dealer_bust": "Dealer estourou!",
                "player_bust": "Você estourou!",
                "game_in_progress": "O jogo está em progresso. Não é possível reiniciar o dinheiro.",
                "enter_name": "Por favor, insira um nome.",
                "name_submitted": "Nome enviado com sucesso!",
                "reset_warning": "⚠️ A reinicialização encerrará o jogo atual!",
                "confirm_reset": "Confirmar Reinício",
                "cancel": "Cancelar",
                "money_reset": "💰 Dinheiro Reiniciado!",
                "reset_cancelled": "Reinício cancelado"
            }
        }

        # Get the application data directory
        if getattr(sys, 'frozen', False):
            # If running as executable
            app_data_dir = os.path.join(os.environ['APPDATA'], 'BlackjackGame')
        else:
            # If running as script
            app_data_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create the directory if it doesn't exist
        os.makedirs(app_data_dir, exist_ok=True)
        
        # Set the leaderboard file path
        self.leaderboard_file = os.path.join(app_data_dir, "leaderboard.json")

        # Initialize game variables
        self.deck = []
        self.dealer_hand = []
        self.player_hand = []
        self.game_in_progress = False
        self.bet_amount = 0
        self.player_money = 1000

        # Leaderboard data
        self.leaderboard_data = self.load_leaderboard()
        self.current_player = None

        # Create icons
        self.create_icons()

        # Configure root grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create main content frame
        self.content_frame = ctk.CTkFrame(self.root, fg_color="#1a1a2e")
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Configure content frame grid weights
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=2)
        self.content_frame.grid_columnconfigure(2, weight=1)

        # Top frame
        self.top_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e")
        self.top_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 20))

        self.title_label = ctk.CTkLabel(
            self.top_frame,
            text=self.translations[self.current_language]["title"],
            font=("Arial", 36, "bold"),
            text_color="#e94560"
        )
        self.title_label.pack(side=tk.LEFT, padx=(0, 20))

        # Settings
        self.settings_frame = ctk.CTkFrame(self.top_frame, fg_color="#1a1a2e")
        self.settings_frame.pack(side=tk.RIGHT)

        self.language_button = ctk.CTkButton(
            self.settings_frame,
            text="",
            command=self.show_language_menu,
            fg_color="#0f3460",
            hover_color="#1a1a2e",
            width=40,
            height=40,
            corner_radius=20,
            cursor="hand2",
            image=self.language_icon
        )
        self.language_button.pack(side=tk.LEFT, padx=5)

        # Left frame: Leaderboard
        self.left_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e")
        self.left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        self.leaderboard_label = ctk.CTkLabel(
            self.left_frame,
            text="🏆 TOP 5",
            font=("Courier", 18, "bold"),  # monospace for alignment
            text_color="#e94560"
        )
        self.leaderboard_label.pack(pady=(10, 5))

        self.name_frame = ctk.CTkFrame(self.left_frame, fg_color="#0f3460")
        self.name_frame.pack(fill=tk.X, padx=5, pady=5)

        self.name_label = ctk.CTkLabel(
            self.name_frame,
            text="Name:",
            font=("Arial", 14, "bold"),
            text_color="#ffffff"
        )
        self.name_label.pack(pady=2)

        self.name_entry = ctk.CTkEntry(
            self.name_frame,
            width=140,
            font=("Arial", 14),
            justify="center"
        )
        self.name_entry.pack(pady=2)

        self.submit_name_button = ctk.CTkButton(
            self.name_frame,
            text="Submit",
            command=self.submit_name,
            fg_color="#e94560",
            hover_color="#c1121f",
            width=70,
            height=25,
            corner_radius=12,
            cursor="hand2",
            font=("Arial", 14, "bold")
        )
        self.submit_name_button.pack(pady=2)

        self.leaderboard_frame = ctk.CTkFrame(
            self.left_frame,
            fg_color="#0f3460",
            width=240  # widened for better money alignment
        )
        self.leaderboard_frame.pack(padx=5, pady=5, fill=tk.X)

        self.leaderboard_container = ctk.CTkFrame(
            self.leaderboard_frame,
            fg_color="#0f3460"
        )
        self.leaderboard_container.pack(fill=tk.X, pady=5)

        self.leaderboard_labels = []
        for i in range(5):
            label = ctk.CTkLabel(
                self.leaderboard_container,
                text="",
                font=("Courier", 14, "bold"),  # monospace font
                text_color="#ffffff",
                width=220,  # match container
                anchor="w"
            )
            label.pack(pady=2)
            self.leaderboard_labels.append(label)

        self.update_leaderboard_display()

        # Center frame: Game board
        self.center_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e")
        self.center_frame.grid(row=1, column=1, sticky="nsew", padx=10)

        # Dealer section
        self.dealer_frame = ctk.CTkFrame(self.center_frame, fg_color="#0f3460", height=200)
        self.dealer_frame.pack(fill=tk.X, pady=(0, 10))

        self.dealer_label = ctk.CTkLabel(
            self.dealer_frame,
            text=self.translations[self.current_language]["dealer_hand"],
            font=("Arial", 16, "bold"),
            text_color="#ffffff"
        )
        self.dealer_label.pack(pady=5)

        self.dealer_canvas = Canvas(
            self.dealer_frame,
            bg="#0f3460",
            highlightthickness=0
        )
        self.dealer_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Player section
        self.player_frame = ctk.CTkFrame(self.center_frame, fg_color="#0f3460", height=200)
        self.player_frame.pack(fill=tk.X, pady=(0, 10))

        self.player_label = ctk.CTkLabel(
            self.player_frame,
            text=self.translations[self.current_language]["player_hand"],
            font=("Arial", 16, "bold"),
            text_color="#ffffff"
        )
        self.player_label.pack(pady=5)

        self.player_canvas = Canvas(
            self.player_frame,
            bg="#0f3460",
            highlightthickness=0
        )
        self.player_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Status section
        self.status_frame = ctk.CTkFrame(self.center_frame, fg_color="#0f3460", height=50)
        self.status_frame.pack(fill=tk.X)

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=("Arial", 16, "bold"),
            text_color="#ffffff"
        )
        self.status_label.pack(pady=5)

        # Right frame: Controls
        self.right_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a2e")
        self.right_frame.grid(row=1, column=2, sticky="nsew", padx=(10, 0))
        
        # Configure right frame grid
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=0)  # Stats frame
        self.right_frame.grid_rowconfigure(1, weight=0)  # Bet frame
        self.right_frame.grid_rowconfigure(2, weight=0)  # Button frame
        self.right_frame.grid_rowconfigure(3, weight=0)  # Reset confirm frame
        self.right_frame.grid_rowconfigure(4, weight=1)  # Spacer

        # Stats frame
        self.stats_frame = ctk.CTkFrame(self.right_frame, fg_color="#0f3460")
        self.stats_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.money_label = ctk.CTkLabel(
            self.stats_frame,
            text=f"{self.translations[self.current_language]['money']}{self.player_money}",
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        self.money_label.pack(pady=10)

        # Betting controls
        self.bet_frame = ctk.CTkFrame(self.right_frame, fg_color="#0f3460")
        self.bet_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        self.bet_label = ctk.CTkLabel(
            self.bet_frame,
            text=self.translations[self.current_language]["bet_amount"],
            font=("Arial", 14, "bold"),
            text_color="#ffffff"
        )
        self.bet_label.pack(pady=5)

        self.bet_entry = ctk.CTkEntry(
            self.bet_frame,
            width=140,  # match name entry
            font=("Arial", 14),
            justify="center"
        )
        self.bet_entry.pack(pady=5)
        self.bet_entry.insert(0, "100")

        # Buttons
        self.button_frame = ctk.CTkFrame(self.right_frame, fg_color="#0f3460")
        self.button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        self.deal_button = ctk.CTkButton(
            self.button_frame,
            text=self.translations[self.current_language]["deal"],
            command=self.deal_cards,
            fg_color="#e94560",
            hover_color="#c1121f",
            width=120,
            height=40,
            corner_radius=20,
            cursor="hand2",
            font=("Arial", 16, "bold")
        )
        self.deal_button.pack(pady=5)

        self.hit_button = ctk.CTkButton(
            self.button_frame,
            text=self.translations[self.current_language]["hit"],
            command=self.hit,
            state="disabled",
            fg_color="#e94560",
            hover_color="#c1121f",
            width=120,
            height=40,
            corner_radius=20,
            cursor="hand2",
            font=("Arial", 16, "bold")
        )
        self.hit_button.pack(pady=5)

        self.stand_button = ctk.CTkButton(
            self.button_frame,
            text=self.translations[self.current_language]["stand"],
            command=self.stand,
            state="disabled",
            fg_color="#e94560",
            hover_color="#c1121f",
            width=120,
            height=40,
            corner_radius=20,
            cursor="hand2",
            font=("Arial", 16, "bold")
        )
        self.stand_button.pack(pady=5)

        self.reset_money_button = ctk.CTkButton(
            self.button_frame,
            text="",
            command=self.reset_money,
            fg_color="#0f3460",
            hover_color="#1a1a2e",
            width=40,
            height=40,
            corner_radius=20,
            cursor="hand2",
            image=self.reset_icon
        )
        self.reset_money_button.pack(pady=5)

        # Reset confirmation frame (initially hidden)
        self.reset_confirm_frame = ctk.CTkFrame(
            self.right_frame, 
            fg_color="#0f3460",
            width=140  # Fixed width
        )
        self.reset_confirm_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        self.reset_confirm_frame.grid_propagate(False)  # Prevent frame from shrinking
        self.reset_confirm_frame.grid_remove()  # Hide by default
        
        self.reset_warning_label = ctk.CTkLabel(
            self.reset_confirm_frame,
            text=self.translations[self.current_language]["reset_warning"],
            font=("Arial", 14, "bold"),
            text_color="#ff9900",
            justify="center"
        )
        self.reset_warning_label.pack(pady=5)
        
        self.reset_confirm_button = ctk.CTkButton(
            self.reset_confirm_frame,
            text=self.translations[self.current_language]["confirm_reset"],
            command=self.confirm_reset,
            fg_color="#e94560",
            hover_color="#c1121f",
            width=120,
            height=30,
            corner_radius=15,
            cursor="hand2",
            font=("Arial", 14, "bold")
        )
        self.reset_confirm_button.pack(pady=5)
        
        self.reset_cancel_button = ctk.CTkButton(
            self.reset_confirm_frame,
            text=self.translations[self.current_language]["cancel"],
            command=self.cancel_reset,
            fg_color="#1a1a2e",
            hover_color="#0f3460",
            width=120,
            height=30,
            corner_radius=15,
            cursor="hand2",
            font=("Arial", 14, "bold")
        )
        self.reset_cancel_button.pack(pady=5)

        # Initialize deck
        self.initialize_deck()

    def create_icons(self):
        """Create icons using Tabler Icons"""
        # Reset money icon (rotate icon)
        reset_icon = TablerIcons.load(
            OutlineIcon.ROTATE,
            size=32,
            color='#e94560',
            stroke_width=2.0
        )
        self.reset_icon = ctk.CTkImage(
            light_image=reset_icon,
            dark_image=reset_icon,
            size=(32, 32)
        )

        # Language icon (globe icon)
        lang_icon = TablerIcons.load(
            OutlineIcon.WORLD,
            size=32,
            color='#e94560',
            stroke_width=2.0
        )
        self.language_icon = ctk.CTkImage(
            light_image=lang_icon,
            dark_image=lang_icon,
            size=(32, 32)
        )

    def initialize_deck(self):
        """Initialize a new deck of cards"""
        suits = ["♠", "♥", "♦", "♣"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.deck = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self.deck)

    def draw_card(self, canvas, card, x, y, width, height):
        """Draw a card on the canvas"""
        # Draw card background with shadow
        canvas.create_rectangle(
            x + 2, y + 2,
            x + width + 2, y + height + 2,
            fill="#000000",
            outline=""
        )
        
        # Draw card background
        canvas.create_rectangle(
            x, y,
            x + width, y + height,
            fill="#ffffff",
            outline="#e94560",
            width=2
        )

        # Get card value and suit
        value, suit = card

        # Set color based on suit
        color = "#e94560" if suit in ["♥", "♦"] else "#1a1a2e"

        # Draw value and suit in top-left
        canvas.create_text(
            x + 15, y + 15,
            text=str(value),
            fill=color,
            font=("Arial", 20, "bold"),
            anchor="nw"
        )
        canvas.create_text(
            x + 15, y + 40,
            text=suit,
            fill=color,
            font=("Arial", 20, "bold"),
            anchor="nw"
        )

        # Draw value and suit in bottom-right
        canvas.create_text(
            x + width - 15, y + height - 15,
            text=str(value),
            fill=color,
            font=("Arial", 20, "bold"),
            anchor="se"
        )
        canvas.create_text(
            x + width - 15, y + height - 40,
            text=suit,
            fill=color,
            font=("Arial", 20, "bold"),
            anchor="se"
        )

    def update_card_display(self):
        """Update the display of cards on the canvas with enhanced styling"""
        # Clear existing cards
        self.player_canvas.delete("all")
        self.dealer_canvas.delete("all")

        # Get canvas dimensions
        player_width = self.player_canvas.winfo_width()
        dealer_width = self.dealer_canvas.winfo_width()
        
        # Calculate positions for cards with side-by-side layout
        if self.game_in_progress and len(self.dealer_hand) >= 2 and len(self.player_hand) >= 2:
            # For dealer's cards
            dealer_x1 = dealer_width * 0.3  # First card position
            dealer_x2 = dealer_width * 0.7  # Second card position
            self.draw_card(self.dealer_canvas, self.dealer_hand[0], dealer_x1, 125, 100, 140)
            self.draw_card(self.dealer_canvas, self.dealer_hand[1], dealer_x2, 125, 100, 140)
            
            # For player's cards
            player_x1 = player_width * 0.3  # First card position
            player_x2 = player_width * 0.7  # Second card position
            self.draw_card(self.player_canvas, self.player_hand[0], player_x1, 125, 100, 140)
            self.draw_card(self.player_canvas, self.player_hand[1], player_x2, 125, 100, 140)
        else:
            # Show all cards side by side
            dealer_cards = len(self.dealer_hand)
            player_cards = len(self.player_hand)
            
            # Calculate spacing for dealer's cards
            if dealer_cards > 0:
                dealer_spacing = dealer_width / (dealer_cards + 1)
                for i, card in enumerate(self.dealer_hand):
                    x_pos = dealer_spacing * (i + 1)
                    self.draw_card(self.dealer_canvas, card, x_pos, 125, 100, 140)
            
            # Calculate spacing for player's cards
            if player_cards > 0:
                player_spacing = player_width / (player_cards + 1)
                for i, card in enumerate(self.player_hand):
                    x_pos = player_spacing * (i + 1)
                    self.draw_card(self.player_canvas, card, x_pos, 125, 100, 140)

        # Update status label with hand values and enhanced styling
        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        
        status_text = f"Player: {player_value} | Dealer: {dealer_value if not self.game_in_progress else '?'}"
        if player_value > 21:
            status_text = f"Player: {player_value} (BUST!) | Dealer: {dealer_value if not self.game_in_progress else '?'}"
        
        self.status_label.configure(
            text=status_text,
            fg="#e94560" if player_value > 21 else "#ffffff"
        )

    def calculate_hand_value(self, hand):
        """Calculate the value of a hand"""
        value = 0
        aces = 0
        
        for card in hand:
            rank = card[0]
            if rank in ["J", "Q", "K"]:
                value += 10
            elif rank == "A":
                aces += 1
            else:
                value += int(rank)
        
        # Add aces
        for _ in range(aces):
            if value + 11 <= 21:
                value += 11
            else:
                value += 1
        
        return value

    def deal_cards(self):
        """Deal initial cards to player and dealer"""
        try:
            bet = int(self.bet_entry.get())
            if bet <= 0 or bet > self.player_money:
                messagebox.showerror(
                    "Error",
                    self.translations[self.current_language]["invalid_bet"]
                )
                return
        except ValueError:
            messagebox.showerror(
                "Error",
                self.translations[self.current_language]["enter_valid_bet"]
            )
            return

        # Clear previous feedback
        self.status_label.configure(text="")

        self.bet_amount = bet
        self.game_in_progress = True
        self.deck = []
        self.dealer_hand = []
        self.player_hand = []
        self.initialize_deck()
        random.shuffle(self.deck)

        # Deal initial cards
        self.player_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())
        self.player_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())

        # Update display
        self.update_display()

        # Update button states
        self.bet_entry.configure(state="disabled")
        self.deal_button.configure(state="disabled")
        self.hit_button.configure(state="normal")
        self.stand_button.configure(state="normal")

        # Check for blackjack
        if self.calculate_hand_value(self.player_hand) == 21:
            self.stand()

    def hit(self):
        """Player takes another card"""
        if not self.game_in_progress:
            return

        self.player_hand.append(self.deck.pop())
        self.update_display()

        # Check for bust
        if self.calculate_hand_value(self.player_hand) > 21:
            self.end_round()

    def stand(self):
        """Player stands, dealer plays"""
        if not self.game_in_progress:
            return

        # Dealer draws until 17 or higher
        while self.calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
            self.update_display()
            self.root.update()  # Update the display after each card

        self.end_round()

    def end_round(self):
        """End the current round and determine the winner"""
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        player_value = self.calculate_hand_value(self.player_hand)
        
        # Update status label with appropriate color and message
        if player_value > 21:
            self.status_label.configure(
                text=f"💥 {self.translations[self.current_language]['player_bust']}",
                text_color="#ff0000"
            )
            self.player_money -= self.bet_amount
        elif dealer_value > 21:
            self.status_label.configure(
                text=f"🎉 {self.translations[self.current_language]['dealer_bust']}",
                text_color="#00ff00"
            )
            self.player_money += self.bet_amount
        elif dealer_value > player_value:
            self.status_label.configure(
                text=f"😢 {self.translations[self.current_language]['dealer_wins']}",
                text_color="#ff0000"
            )
            self.player_money -= self.bet_amount
        elif player_value > dealer_value:
            self.status_label.configure(
                text=f"🎉 {self.translations[self.current_language]['player_wins']}",
                text_color="#00ff00"
            )
            self.player_money += self.bet_amount
        else:
            self.status_label.configure(
                text=f"🤝 {self.translations[self.current_language]['push']}",
                text_color="#ffff00"
            )

        # Update money display
        self.money_label.configure(
            text=f"{self.translations[self.current_language]['money']}{self.player_money}"
        )

        # Update leaderboard if player has a name
        if self.current_player:
            self.update_player_score()

        # Reset game state
        self.game_in_progress = False
        self.deal_button.configure(state="normal")
        self.hit_button.configure(state="disabled")
        self.stand_button.configure(state="disabled")
        self.bet_entry.configure(state="normal")

    def update_display(self):
        # Clear canvases
        self.dealer_canvas.delete("all")
        self.player_canvas.delete("all")

        # Draw dealer's cards
        dealer_x = 10
        for card in self.dealer_hand:
            self.draw_card(self.dealer_canvas, card, dealer_x, 10, 80, 120)
            dealer_x += 90

        # Draw player's cards
        player_x = 10
        for card in self.player_hand:
            self.draw_card(self.player_canvas, card, player_x, 10, 80, 120)
            player_x += 90

        # Update status text
        if self.game_in_progress:
            dealer_text = f"{self.translations[self.current_language]['dealer_hand']}: {self.calculate_hand_value(self.dealer_hand)}"
            player_text = f"{self.translations[self.current_language]['player_hand']}: {self.calculate_hand_value(self.player_hand)}"
            self.status_label.configure(text=f"{dealer_text}\n{player_text}")
        else:
            self.status_label.configure(text="")

    def reset_money(self):
        """Reset player's money to initial amount"""
        # Show confirmation frame
        self.reset_confirm_frame.grid()

    def confirm_reset(self):
        """Confirm and execute money reset"""
        self.player_money = 1000
        self.money_label.configure(
            text=f"{self.translations[self.current_language]['money']}{self.player_money}"
        )
        
        # Reset game state if in progress
        if self.game_in_progress:
            self.game_in_progress = False
            self.deal_button.configure(state="normal")
            self.hit_button.configure(state="disabled")
            self.stand_button.configure(state="disabled")
            self.bet_entry.configure(state="normal")
            self.dealer_hand = []
            self.player_hand = []
            self.update_display()
        
        # Show feedback
        self.status_label.configure(
            text=self.translations[self.current_language]["money_reset"],
            text_color="#00ff00"
        )
        
        # Update leaderboard if player has a name
        if self.current_player:
            self.update_player_score()
        
        # Hide confirmation frame
        self.reset_confirm_frame.grid_remove()

    def cancel_reset(self):
        """Cancel money reset"""
        self.reset_confirm_frame.grid_remove()
        self.status_label.configure(
            text=self.translations[self.current_language]["reset_cancelled"],
            text_color="#ff9900"
        )

    def show_language_menu(self):
        """Show language selection menu"""
        self.language_menu = tk.Menu(self.root, tearoff=0, bg="#1a1a2e", fg="#ffffff", 
                                   activebackground="#e94560", activeforeground="#ffffff", 
                                   font=("Arial", 10))
        self.language_menu.add_command(label="English", command=lambda: self.change_language("en"))
        self.language_menu.add_command(label="Español", command=lambda: self.change_language("es"))
        self.language_menu.add_command(label="Português", command=lambda: self.change_language("pt"))
        self.language_menu.post(self.language_button.winfo_rootx(), 
                              self.language_button.winfo_rooty() + self.language_button.winfo_height())

    def change_language(self, lang):
        """Change the game language"""
        self.current_language = lang
        self.title_label.configure(text=self.translations[lang]["title"])
        self.dealer_label.configure(text=self.translations[lang]["dealer_hand"])
        self.player_label.configure(text=self.translations[lang]["player_hand"])
        self.money_label.configure(text=f"{self.translations[lang]['money']}{self.player_money}")
        self.bet_label.configure(text=self.translations[lang]["bet_amount"])
        self.deal_button.configure(text=self.translations[lang]["deal"])
        self.hit_button.configure(text=self.translations[lang]["hit"])
        self.stand_button.configure(text=self.translations[lang]["stand"])
        self.update_display()

    def update_language(self):
        """Update all text elements with current language"""
        self.title_label.configure(text="BLACKJACK")
        self.dealer_label.configure(text="Dealer's Hand")
        self.player_label.configure(text="Player's Hand")
        self.status_label.configure(text="Welcome to Blackjack!")
        self.bet_label.configure(text="Bet Amount:")
        self.deal_button.configure(text="Deal")
        self.hit_button.configure(text="Hit")
        self.stand_button.configure(text="Stand")
        self.money_label.configure(text=f"Money: ${self.player_money}")

    def load_leaderboard(self):
        """Load leaderboard data from file"""
        try:
            if os.path.exists(self.leaderboard_file):
                with open(self.leaderboard_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading leaderboard: {e}")
            return {}

    def save_leaderboard(self):
        """Save leaderboard data to file"""
        try:
            with open(self.leaderboard_file, 'w') as f:
                json.dump(self.leaderboard_data, f)
        except Exception as e:
            print(f"Error saving leaderboard: {e}")

    def update_leaderboard_display(self):
        """Update the leaderboard display with current scores"""
        # Sort players by money in descending order
        sorted_players = sorted(
            self.leaderboard_data.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Display top 5 players with better spacing and colors
        for i, (name, money) in enumerate(sorted_players[:5]):
            # Truncate long names
            display_name = name[:10] + "..." if len(name) > 10 else name
            
            # Color coding and medals for top 3
            if i == 0:
                color = "#FFD700"  # Gold for 1st place
                medal = "🥇"
            elif i == 1:
                color = "#C0C0C0"  # Silver for 2nd place
                medal = "🥈"
            elif i == 2:
                color = "#CD7F32"  # Bronze for 3rd place
                medal = "🥉"
            else:
                color = "#ffffff"  # White for others
                medal = f"{i+1}."
            
            # Format with name and money on the same line, money right-aligned
            entry = f"{medal} {display_name:<15}${money:>12}"
            self.leaderboard_labels[i].configure(text=entry, text_color=color)
        
        # Clear remaining labels if less than 5 players
        for i in range(len(sorted_players), 5):
            self.leaderboard_labels[i].configure(text="")

    def update_player_score(self):
        """Update player's score in the leaderboard"""
        if not self.current_player:
            return

        # Update or add player score
        self.leaderboard_data[self.current_player] = self.player_money
        
        # Keep only top 5 players
        sorted_players = sorted(
            self.leaderboard_data.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        # Convert back to dictionary
        self.leaderboard_data = dict(sorted_players)
        
        # Save and update display
        self.save_leaderboard()
        self.update_leaderboard_display()

    def submit_name(self):
        """Submit player name for leaderboard"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning(
                "Warning",
                self.translations[self.current_language]["enter_name"]
            )
            return

        self.current_player = name
        self.update_player_score()
        
        # Clear the entry and disable it
        self.name_entry.delete(0, tk.END)
        self.name_entry.configure(state="disabled")
        self.submit_name_button.configure(state="disabled")
        
        # Show feedback
        self.status_label.configure(
            text=f"✅ {self.translations[self.current_language]['name_submitted']}",
            text_color="#00ff00"
        )


if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()
