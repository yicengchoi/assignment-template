# assignment-template
SD5913 - Assignment template
Student name: Cai Qiqing
Student ID: 24120309G

## Concentration and Reaction Game

### Description
This is a simple Pygame-based concentration and reaction game where players must name the color of displayed words, not the words themselves. The game tests players' concentration and reaction speed.

### How to Run the Game
#### Install Required Packages
- pip install pygame  
- pip install SpeechRecognition
- pip install pyaudio
#### Adjust the speed of the words scrolling
You may change the speed of the scrolling words by modifying the value on line 37 in the code
'word_scroll_speed = 9  ### scrolling speed' # Adjust this number for faster or slower scrolling

### Gameplay
1. Start the game by clicking the "START" button.
2. A countdown will appear before the game begins.
3. Words will be displayed on the screen in different colors. You must say the color of the word aloud, not the word itself.
4. Use your microphone to speak the colors.Your score will increase with each correct answer.
5. The game lasts for a limited time. Try to achieve the highest score possible.
6. After the game ends, your final score will be displayed, and you can click the "RETURN" button to play again.
7. If you want to stop the game while playing, click the "END" button to finish the game in advance.

### Problems I met
I've found that the voice recognition feature occasionally can't keep up with the speed of the user's answers to the point where it doesn't recognise them in time for the player to gain points. The problem has not yet been resolved.
