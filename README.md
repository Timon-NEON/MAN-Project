# Web application for generating and storing crossword puzzles
The program consists of a crossword generation algorithm and a web interface.  
The project was created as a scientific work by Tymofiy Kirilenko.  
The web-application you can fing by link: [crosswordsua.pythonanywhere.com](https://crosswordsua.pythonanywhere.com/)

## Install instructions
To download, you need to have Python 3.10 installed on the device, clone the repository and create virtual environment using command in the console in the MAN-Project folder ```python -m venv venv```. Then activate virtual environment using the command ```venv\Scripts\activate.bat```, install all used libraries using command ```pip install -r requirements.txt```.  
After that, in the same folder, you need to execute the command ```python key_generation.py``` to generate your own key. You can then run the web application locally using the command ```python manage.py runserver```.  
If you encounter errors when executing the second and third commands, we advise you to replace the word *python* with *python3* and try again.

## Usage
The algorithm provides an opportunity to create crossword puzzles based on words and their descriptions and to create its images. The algorithm can be found at: */crossword/main_algorithm/CW.py*. You can use the algorithm for your purposes.
The web application allows the user to create and store crosswords on the website. 

## For feedback
[Telegram](https://t.me/Timon_NEON)
