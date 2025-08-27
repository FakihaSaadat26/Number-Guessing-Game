import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Number Guessing Game")
        self.root.geometry("700x800")
        self.root.resizable(False, False)
        
        # Color scheme
        self.colors = {
            'bg_primary': '#2C3E50',
            'bg_secondary': '#34495E',
            'bg_card': '#ECF0F1',
            'accent_blue': '#3498DB',
            'accent_green': '#2ECC71',
            'accent_red': '#E74C3C',
            'accent_orange': '#F39C12',
            'accent_purple': '#9B59B6',
            'text_dark': '#2C3E50',
            'text_light': '#FFFFFF',
            'success': '#27AE60',
            'warning': '#F1C40F',
            'danger': '#E74C3C'
        }
        
        # Configure root
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Game variables
        self.min_range = 1
        self.max_range = 100
        self.max_attempts = 10
        self.secret_number = 0
        self.attempts_left = 0
        self.current_attempts = 0
        self.game_active = False
        self.best_scores = self.load_best_scores()
        self.game_history = self.load_game_history()
        
        self.setup_styles()
        self.setup_ui()
        self.show_setup_frame()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', 
                       font=('Arial', 24, 'bold'),
                       foreground=self.colors['text_light'],
                       background=self.colors['bg_primary'])
        
        style.configure('Header.TLabel',
                       font=('Arial', 14, 'bold'),
                       foreground=self.colors['text_dark'],
                       background=self.colors['bg_card'])
        
        style.configure('Info.TLabel',
                       font=('Arial', 12),
                       foreground=self.colors['text_dark'],
                       background=self.colors['bg_card'])
        
        style.configure('Card.TFrame',
                       background=self.colors['bg_card'],
                       relief='raised',
                       borderwidth=2)
        
        style.configure('Primary.TButton',
                       font=('Arial', 12, 'bold'),
                       foreground=self.colors['text_light'])
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['accent_blue']),
                            ('!active', self.colors['accent_blue'])])
        
        style.configure('Success.TButton',
                       font=('Arial', 12, 'bold'),
                       foreground=self.colors['text_light'])
        
        style.map('Success.TButton',
                 background=[('active', self.colors['success']),
                            ('!active', self.colors['accent_green'])])
        
        style.configure('Danger.TButton',
                       font=('Arial', 10),
                       foreground=self.colors['text_light'])
        
        style.map('Danger.TButton',
                 background=[('active', self.colors['danger']),
                            ('!active', self.colors['accent_red'])])
    
    def setup_ui(self):
        # Main container with gradient effect
        main_canvas = tk.Canvas(self.root, bg=self.colors['bg_primary'], highlightthickness=0)
        main_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create gradient background
        self.create_gradient(main_canvas)
        
        # Scrollable frame
        main_frame = tk.Frame(main_canvas, bg=self.colors['bg_primary'])
        main_canvas.create_window(350, 0, window=main_frame, anchor='n')
        
        # Title with emoji and gradient
        title_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'], height=80)
        title_frame.pack(fill=tk.X, pady=(20, 30))
        
        title_label = tk.Label(title_frame, 
                              text="🎯 NUMBER GUESSING GAME 🎲",
                              font=('Arial', 24, 'bold'),
                              fg=self.colors['text_light'],
                              bg=self.colors['bg_primary'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="Challenge your guessing skills!",
                                 font=('Arial', 12, 'italic'),
                                 fg=self.colors['accent_orange'],
                                 bg=self.colors['bg_primary'])
        subtitle_label.pack()
        
        # Setup Card
        self.setup_card = self.create_card(main_frame, "⚙️ Game Setup", self.colors['accent_blue'])
        
        setup_content = tk.Frame(self.setup_card, bg=self.colors['bg_card'])
        setup_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Range settings with icons
        self.create_input_row(setup_content, "🔢 Minimum Number:", self.colors['accent_green'], 0)
        self.min_var = tk.StringVar(value="1")
        self.min_entry = self.create_styled_entry(setup_content, self.min_var)
        self.min_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky='w')
        
        self.create_input_row(setup_content, "🎯 Maximum Number:", self.colors['accent_red'], 1)
        self.max_var = tk.StringVar(value="100")
        self.max_entry = self.create_styled_entry(setup_content, self.max_var)
        self.max_entry.grid(row=1, column=1, padx=(10, 0), pady=5, sticky='w')
        
        self.create_input_row(setup_content, "💪 Maximum Attempts:", self.colors['accent_purple'], 2)
        self.attempts_var = tk.StringVar(value="10")
        self.attempts_entry = self.create_styled_entry(setup_content, self.attempts_var)
        self.attempts_entry.grid(row=2, column=1, padx=(10, 0), pady=5, sticky='w')
        
        # Start button
        self.start_button = tk.Button(setup_content,
                                     text="🚀 START NEW GAME",
                                     font=('Arial', 14, 'bold'),
                                     bg=self.colors['accent_green'],
                                     fg=self.colors['text_light'],
                                     relief='raised',
                                     borderwidth=3,
                                     padx=20, pady=10,
                                     command=self.start_game,
                                     cursor='hand2')
        self.start_button.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        # Game Card
        self.game_card = self.create_card(main_frame, "🎮 Game Arena", self.colors['accent_purple'])
        
        game_content = tk.Frame(self.game_card, bg=self.colors['bg_card'])
        game_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Game info with better styling
        self.info_label = tk.Label(game_content,
                                  text="🎲 Click 'START NEW GAME' to begin your adventure!",
                                  font=('Arial', 13, 'bold'),
                                  fg=self.colors['text_dark'],
                                  bg=self.colors['bg_card'],
                                  wraplength=400)
        self.info_label.pack(pady=(0, 15))
        
        # Guess input with styling
        guess_frame = tk.Frame(game_content, bg=self.colors['bg_card'])
        guess_frame.pack(pady=10)
        
        tk.Label(guess_frame, text="🤔 Your Guess:",
                font=('Arial', 12, 'bold'),
                fg=self.colors['text_dark'],
                bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=(0, 10))
        
        self.guess_var = tk.StringVar()
        self.guess_entry = tk.Entry(guess_frame,
                                   textvariable=self.guess_var,
                                   font=('Arial', 14, 'bold'),
                                   width=12,
                                   justify='center',
                                   relief='raised',
                                   borderwidth=2,
                                   bg='white',
                                   fg=self.colors['text_dark'])
        self.guess_entry.pack(side=tk.LEFT)
        self.guess_entry.bind('<Return>', lambda e: self.make_guess())
        
        # Guess button
        self.guess_button = tk.Button(game_content,
                                     text="🎯 MAKE GUESS",
                                     font=('Arial', 12, 'bold'),
                                     bg=self.colors['accent_blue'],
                                     fg=self.colors['text_light'],
                                     relief='raised',
                                     borderwidth=2,
                                     padx=20, pady=8,
                                     command=self.make_guess,
                                     state="disabled",
                                     cursor='hand2')
        self.guess_button.pack(pady=(15, 0))
        
        # Attempts display with progress-like styling
        self.attempts_frame = tk.Frame(game_content, bg=self.colors['bg_card'])
        self.attempts_frame.pack(pady=(15, 0))
        
        self.attempts_label = tk.Label(self.attempts_frame,
                                      text="",
                                      font=('Arial', 11, 'bold'),
                                      fg=self.colors['text_dark'],
                                      bg=self.colors['bg_card'])
        self.attempts_label.pack()
        
        # Progress bar for attempts
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.attempts_frame,
                                           variable=self.progress_var,
                                           maximum=100,
                                           length=300,
                                           mode='determinate')
        self.progress_bar.pack(pady=(5, 0))
        
        # Feedback with emoji and colors
        self.feedback_label = tk.Label(game_content,
                                      text="",
                                      font=('Arial', 13, 'bold'),
                                      fg=self.colors['text_dark'],
                                      bg=self.colors['bg_card'],
                                      wraplength=400)
        self.feedback_label.pack(pady=(15, 0))
        
        # Statistics Card
        self.stats_card = self.create_card(main_frame, "📊 Game Statistics", self.colors['accent_orange'])
        
        stats_content = tk.Frame(self.stats_card, bg=self.colors['bg_card'])
        stats_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Stats grid
        self.stats_frame = tk.Frame(stats_content, bg=self.colors['bg_card'])
        self.stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.create_stat_box(self.stats_frame, "🎮", "Games Played", "0", self.colors['accent_blue'], 0, 0)
        self.create_stat_box(self.stats_frame, "🏆", "Games Won", "0", self.colors['success'], 0, 1)
        self.create_stat_box(self.stats_frame, "💯", "Win Rate", "0%", self.colors['accent_purple'], 0, 2)
        self.create_stat_box(self.stats_frame, "⚡", "Best Score", "N/A", self.colors['accent_orange'], 1, 0)
        self.create_stat_box(self.stats_frame, "📈", "Avg Attempts", "N/A", self.colors['accent_red'], 1, 1)
        self.create_stat_box(self.stats_frame, "🔥", "Current Streak", "0", self.colors['accent_green'], 1, 2)
        
        # Best Scores Card
        self.scores_card = self.create_card(main_frame, "🏅 Hall of Fame", self.colors['accent_red'])
        
        scores_content = tk.Frame(self.scores_card, bg=self.colors['bg_card'])
        scores_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Scores display with better formatting
        scores_display_frame = tk.Frame(scores_content, bg=self.colors['bg_card'])
        scores_display_frame.pack(fill=tk.BOTH, expand=True)
        
        self.scores_text = tk.Text(scores_display_frame,
                                  height=10, width=70,
                                  wrap=tk.WORD,
                                  font=('Consolas', 10),
                                  bg='#F8F9FA',
                                  fg=self.colors['text_dark'],
                                  relief='sunken',
                                  borderwidth=2)
        self.scores_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scores_scrollbar = ttk.Scrollbar(scores_display_frame, orient="vertical", command=self.scores_text.yview)
        scores_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scores_text.configure(yscrollcommand=scores_scrollbar.set)
        
        # Clear scores button
        clear_button = tk.Button(scores_content,
                                text="🗑️ Clear All Records",
                                font=('Arial', 10, 'bold'),
                                bg=self.colors['danger'],
                                fg=self.colors['text_light'],
                                relief='raised',
                                borderwidth=2,
                                padx=15, pady=5,
                                command=self.clear_scores,
                                cursor='hand2')
        clear_button.pack(pady=(10, 0))
        
        self.update_all_displays()
    
    def create_gradient(self, canvas):
        # Simple gradient effect
        height = 800
        for i in range(height):
            color = self.interpolate_color('#2C3E50', '#34495E', i / height)
            canvas.create_line(0, i, 700, i, fill=color, width=1)
    
    def interpolate_color(self, color1, color2, factor):
        # Simple color interpolation
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % rgb
        
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        
        rgb = tuple(int(rgb1[i] + factor * (rgb2[i] - rgb1[i])) for i in range(3))
        return rgb_to_hex(rgb)
    
    def create_card(self, parent, title, accent_color):
        # Card container
        card_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        card_frame.pack(fill=tk.X, pady=(0, 20), padx=20)
        
        # Card header
        header = tk.Frame(card_frame, bg=accent_color, height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(header,
                              text=title,
                              font=('Arial', 14, 'bold'),
                              fg=self.colors['text_light'],
                              bg=accent_color)
        title_label.pack(expand=True)
        
        # Card body
        body = tk.Frame(card_frame, bg=self.colors['bg_card'], relief='raised', borderwidth=2)
        body.pack(fill=tk.BOTH, expand=True)
        
        return body
    
    def create_input_row(self, parent, text, color, row):
        label = tk.Label(parent,
                        text=text,
                        font=('Arial', 11, 'bold'),
                        fg=color,
                        bg=self.colors['bg_card'])
        label.grid(row=row, column=0, sticky='w', pady=5)
    
    def create_styled_entry(self, parent, textvariable):
        entry = tk.Entry(parent,
                        textvariable=textvariable,
                        font=('Arial', 11),
                        width=12,
                        relief='raised',
                        borderwidth=2,
                        bg='white')
        return entry
    
    def create_stat_box(self, parent, icon, label, value, color, row, col):
        frame = tk.Frame(parent, bg=color, relief='raised', borderwidth=2, padx=10, pady=8)
        frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        
        icon_label = tk.Label(frame, text=icon, font=('Arial', 16), bg=color, fg='white')
        icon_label.pack()
        
        label_label = tk.Label(frame, text=label, font=('Arial', 8, 'bold'), bg=color, fg='white')
        label_label.pack()
        
        value_label = tk.Label(frame, text=value, font=('Arial', 12, 'bold'), bg=color, fg='white')
        value_label.pack()
        
        # Store reference for updating
        setattr(self, f"stat_{label.lower().replace(' ', '_')}", value_label)
        
        # Configure grid weights
        parent.grid_columnconfigure(col, weight=1)
    
    def show_setup_frame(self):
        self.game_active = False
        self.guess_button.config(state="disabled", bg='gray')
        self.guess_entry.config(state="disabled")
        self.start_button.config(state="normal", bg=self.colors['accent_green'])
    
    def start_game(self):
        try:
            # Validate inputs
            min_val = int(self.min_var.get())
            max_val = int(self.max_var.get())
            max_attempts = int(self.attempts_var.get())
            
            if min_val >= max_val:
                messagebox.showerror("Invalid Range", "Minimum must be less than maximum!")
                return
            
            if max_attempts < 1:
                messagebox.showerror("Invalid Attempts", "Maximum attempts must be at least 1!")
                return
            
            # Set game parameters
            self.min_range = min_val
            self.max_range = max_val
            self.max_attempts = max_attempts
            self.attempts_left = max_attempts
            self.current_attempts = 0
            
            # Generate secret number
            self.secret_number = random.randint(self.min_range, self.max_range)
            
            # Update UI
            self.game_active = True
            self.guess_button.config(state="normal", bg=self.colors['accent_blue'])
            self.guess_entry.config(state="normal")
            self.start_button.config(state="disabled", bg='gray')
            
            # Clear previous game data
            self.guess_var.set("")
            self.feedback_label.config(text="", fg=self.colors['text_dark'])
            
            # Update info
            range_text = f"🎯 Guess a number between {self.min_range} and {self.max_range}"
            self.info_label.config(text=range_text, fg=self.colors['text_dark'])
            self.update_attempts_display()
            
            # Focus on guess entry
            self.guess_entry.focus()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for all fields!")
    
    def make_guess(self):
        if not self.game_active:
            return
        
        try:
            guess = int(self.guess_var.get())
            
            if guess < self.min_range or guess > self.max_range:
                self.feedback_label.config(
                    text=f"⚠️ Please guess between {self.min_range} and {self.max_range}!",
                    fg=self.colors['warning'])
                return
            
            self.current_attempts += 1
            self.attempts_left -= 1
            
            if guess == self.secret_number:
                # Winner!
                self.feedback_label.config(
                    text=f"🎉 AMAZING! You guessed it in {self.current_attempts} attempts! 🏆",
                    fg=self.colors['success'])
                self.save_game_result(True, self.current_attempts)
                self.end_game()
                
            elif self.attempts_left == 0:
                # Out of attempts
                self.feedback_label.config(
                    text=f"😞 Game Over! The number was {self.secret_number}. Better luck next time!",
                    fg=self.colors['danger'])
                self.save_game_result(False, self.current_attempts)
                self.end_game()
                
            else:
                # Give hint with more personality
                if guess < self.secret_number:
                    diff = self.secret_number - guess
                    if diff > 20:
                        hint = "📈 WAY too low! Think much higher! 🚀"
                    elif diff > 10:
                        hint = "📈 Too low! Go higher! ⬆️"
                    else:
                        hint = "📈 Close, but still too low! Just a bit higher! 😊"
                else:
                    diff = guess - self.secret_number
                    if diff > 20:
                        hint = "📉 WAY too high! Think much lower! 🎈"
                    elif diff > 10:
                        hint = "📉 Too high! Go lower! ⬇️"
                    else:
                        hint = "📉 Close, but still too high! Just a bit lower! 😊"
                
                self.feedback_label.config(text=hint, fg=self.colors['accent_blue'])
                self.update_attempts_display()
            
            # Clear guess entry
            self.guess_var.set("")
            
        except ValueError:
            self.feedback_label.config(text="🤔 Please enter a valid number!", fg=self.colors['warning'])
    
    def end_game(self):
        self.game_active = False
        self.guess_button.config(state="disabled", bg='gray')
        self.guess_entry.config(state="disabled")
        self.start_button.config(state="normal", bg=self.colors['accent_green'])
        self.update_all_displays()
    
    def update_attempts_display(self):
        attempts_text = f"💪 Attempts: {self.current_attempts} | Remaining: {self.attempts_left}"
        self.attempts_label.config(text=attempts_text)
        
        # Update progress bar
        progress = ((self.max_attempts - self.attempts_left) / self.max_attempts) * 100
        self.progress_var.set(progress)
    
    def save_game_result(self, won, attempts):
        # Save to game history
        game_record = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'range': f"{self.min_range}-{self.max_range}",
            'max_attempts': self.max_attempts,
            'attempts_used': attempts,
            'won': won,
            'secret_number': self.secret_number
        }
        self.game_history.append(game_record)
        
        # Save best score if won
        if won:
            range_key = f"{self.min_range}-{self.max_range}"
            attempts_key = f"{self.max_attempts}_attempts"
            
            if range_key not in self.best_scores:
                self.best_scores[range_key] = {}
            
            if attempts_key not in self.best_scores[range_key]:
                self.best_scores[range_key][attempts_key] = attempts
            else:
                if attempts < self.best_scores[range_key][attempts_key]:
                    self.best_scores[range_key][attempts_key] = attempts
        
        self.save_data()
    
    def update_all_displays(self):
        self.update_stats_display()
        self.update_scores_display()
    
    def update_stats_display(self):
        if not self.game_history:
            return
        
        total_games = len(self.game_history)
        won_games = sum(1 for game in self.game_history if game['won'])
        win_rate = (won_games / total_games * 100) if total_games > 0 else 0
        
        # Best score across all games
        best_score = min((game['attempts_used'] for game in self.game_history if game['won']), default=None)
        
        # Average attempts for won games
        won_attempts = [game['attempts_used'] for game in self.game_history if game['won']]
        avg_attempts = sum(won_attempts) / len(won_attempts) if won_attempts else 0
        
        # Current streak
        current_streak = 0
        for game in reversed(self.game_history):
            if game['won']:
                current_streak += 1
            else:
                break
        
        # Update stat boxes
        self.stat_games_played.config(text=str(total_games))
        self.stat_games_won.config(text=str(won_games))
        self.stat_win_rate.config(text=f"{win_rate:.1f}%")
        self.stat_best_score.config(text=str(best_score) if best_score else "N/A")
        self.stat_avg_attempts.config(text=f"{avg_attempts:.1f}" if avg_attempts > 0 else "N/A")
        self.stat_current_streak.config(text=str(current_streak))
    
    def update_scores_display(self):
        self.scores_text.delete(1.0, tk.END)
        
        if not self.best_scores:
            self.scores_text.insert(tk.END, "🏆 No records yet! Play some games to see your achievements!\n\n")
            self.scores_text.insert(tk.END, "🎯 Tips:\n")
            self.scores_text.insert(tk.END, "• Try different difficulty levels\n")
            self.scores_text.insert(tk.END, "• Challenge yourself with larger ranges\n")
            self.scores_text.insert(tk.END, "• See how few attempts you can win in!\n")
            return
        
        self.scores_text.insert(tk.END, "🏅 HALL OF FAME - Best Scores by Difficulty 🏅\n")
        self.scores_text.insert(tk.END, "=" * 50 + "\n\n")
        
        for range_key, attempts_dict in sorted(self.best_scores.items()):
            range_parts = range_key.split('-')
            range_size = int(range_parts[1]) - int(range_parts[0]) + 1
            
            # Determine difficulty emoji
            if range_size <= 20:
                difficulty_emoji = "🟢 EASY"
            elif range_size <= 50:
                difficulty_emoji = "🟡 MEDIUM"
            elif range_size <= 100:
                difficulty_emoji = "🟠 HARD"
            else:
                difficulty_emoji = "🔴 EXPERT"
            
            self.scores_text.insert(tk.END, f"{difficulty_emoji} Range {range_parts[0]} - {range_parts[1]} ({range_size} numbers)\n")
            self.scores_text.insert(tk.END, "-" * 40 + "\n")
            
            for attempts_key, best_score in sorted(attempts_dict.items()):
                max_attempts = attempts_key.replace('_attempts', '')
                
                # Calculate efficiency
                efficiency = (best_score / int(max_attempts)) * 100
                if efficiency <= 30:
                    efficiency_emoji = "⭐⭐⭐"
                elif efficiency <= 50:
                    efficiency_emoji = "⭐⭐"
                else:
                    efficiency_emoji = "⭐"
                
                score_text = f"  🎯 {max_attempts} max attempts: {best_score} attempts {efficiency_emoji}\n"
                self.scores_text.insert(tk.END, score_text)
            
            self.scores_text.insert(tk.END, "\n")
        
        # Recent games summary
        if self.game_history:
            self.scores_text.insert(tk.END, "\n📊 RECENT ACTIVITY\n")
            self.scores_text.insert(tk.END, "=" * 20 + "\n")
            
            recent_games = self.game_history[-5:] if len(self.game_history) >= 5 else self.game_history
            for game in reversed(recent_games):
                status = "🏆 WON" if game['won'] else "❌ LOST"
                date = game['date'].split(' ')[0]  # Just the date part
                self.scores_text.insert(tk.END, f"{status} | {game['range']} | {game['attempts_used']} attempts | {date}\n")
    
    def clear_scores(self):
        """Clear all saved scores and game history"""
        if messagebox.askyesno("Clear Records", "Are you sure you want to clear all records? This cannot be undone!"):
            self.best_scores = {}
            self.game_history = []
            self.save_data()
            self.update_all_displays()
            messagebox.showinfo("Cleared", "All records have been cleared!")
    
    def load_best_scores(self):
        """Load best scores from JSON file"""
        try:
            if os.path.exists("best_scores.json"):
                with open("best_scores.json", "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading best scores: {e}")
        return {}
    
    def load_game_history(self):
        """Load game history from JSON file"""
        try:
            if os.path.exists("game_history.json"):
                with open("game_history.json", "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading game history: {e}")
        return []
    
    def save_data(self):
        """Save both best scores and game history to JSON files"""
        try:
            with open("best_scores.json", "w") as f:
                json.dump(self.best_scores, f, indent=2)
            with open("game_history.json", "w") as f:
                json.dump(self.game_history, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
            messagebox.showerror("Save Error", f"Could not save game data: {e}")

def main():
    """Main function to run the game"""
    root = tk.Tk()
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Create the game
    game = NumberGuessingGame(root)
    
    # Handle window closing
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit the game?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the game loop
    root.mainloop()

if __name__ == "__main__":
    main()