#include <iostream>
#include <cstdlib>
#include <ctime>
#include <limits>

using namespace std;

int getValidatedInput(const string& prompt) {
    int num;
    while (true) {
        cout << prompt;
        cin >> num;
        if (cin.fail()) {
            cin.clear(); // clear error state
            cin.ignore(numeric_limits<streamsize>::max(), '\n'); // discard invalid input
            cout << "Invalid input. Please enter a number.\n";
        } else {
            return num;
        }
    }
}

int main() {
    srand(static_cast<unsigned int>(time(0)));

    int bestScore = INT_MAX;
    char playAgain;

    do {
        int minRange = getValidatedInput("Enter minimum number: ");
        int maxRange = getValidatedInput("Enter maximum number: ");

        while (maxRange <= minRange) {
            cout << "Max should be greater than min. Try again.\n";
            maxRange = getValidatedInput("Enter maximum number: ");
        }

        int secretNumber = rand() % (maxRange - minRange + 1) + minRange;

        int guessLimit = getValidatedInput("Enter max number of guesses allowed: ");
        int guessCount = 0;
        int guess;
        bool guessedCorrectly = false;

        cout << "\n--- Game Started! ---\n";

        while (guessCount < guessLimit) {
            guess = getValidatedInput("Enter your guess: ");
            guessCount++;

            if (guess == secretNumber) {
                cout << "🎉 Correct! You guessed it in " << guessCount << " attempts.\n";
                if (guessCount < bestScore) {
                    bestScore = guessCount;
                    cout << "🏆 New best score!\n";
                }
                guessedCorrectly = true;
                break;
            } else if (guess < secretNumber) {
                cout << "Too low. Try again.\n";
            } else {
                cout << "Too high. Try again.\n";
            }
        }

        if (!guessedCorrectly) {
            cout << "❌ You've run out of guesses! The correct number was: " << secretNumber << "\n";
        }

        if (bestScore != INT_MAX) {
            cout << "🔥 Best score so far: " << bestScore << " attempts.\n";
        }

        cout << "Do you want to play again? (y/n): ";
        cin >> playAgain;

    } while (playAgain == 'y' || playAgain == 'Y');

    cout << "Thanks for playing! 👋\n";
    return 0;
}
