🎯 Number Guessing Game (Tkinter GUI)

A fun and interactive Number Guessing Game built with Python (Tkinter).
Players try to guess a randomly generated number within a set number of attempts. The game includes hints, stats tracking, hall of fame records, streaks, and a stylish modern UI.

✨ Features

🎮 Custom Game Setup – choose your own minimum, maximum, and number of attempts.

🎲 Interactive Game Arena – enter guesses, get real-time hints, and feedback with emojis.

📊 Game Statistics – track games played, games won, win rate, best score, average attempts, and streaks.

🏅 Hall of Fame – see your best scores by difficulty levels (Easy, Medium, Hard, Expert).

🔄 Recent Activity Log – displays the last 5 game outcomes.

💾 Persistent Data – saves best scores and game history using JSON files.

🎨 Modern UI – gradient background, styled buttons, colorful cards, emojis for engagement.

📷 Screenshots (Optional if you want to add)

(Add screenshots of the UI here if possible)

🚀 How to Run
1. Clone the repository:
git clone https://github.com/yourusername/number-guessing-game.git
cd number-guessing-game

2. Install Python (if not already installed):

Make sure you have Python 3.8+ installed.

3. Run the game:
python number_guessing_game.py

📂 Project Structure
number-guessing-game/
│── number_guessing_game.py   # Main game code
│── best_scores.json          # Stores best scores
│── game_history.json         # Stores game history
│── README.md                 # Project documentation

🕹️ How to Play

Enter your minimum number, maximum number, and maximum attempts in the setup panel.

Click 🚀 START NEW GAME.

Enter your guess in the input field and press Enter or click 🎯 MAKE GUESS.

Get feedback:

📈 Too Low → Guess higher

📉 Too High → Guess lower

🎉 Correct → You win!

Track your stats and achievements in the Statistics and Hall of Fame sections.

✅ Requirements

Python 3.8+

Tkinter (comes pre-installed with Python)

🏗️ Future Improvements

Add multiplayer mode 🎭

Difficulty presets (Easy, Medium, Hard)

Save user profiles