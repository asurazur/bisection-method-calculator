# root-finding-tkinter-python
This is a root finding calculator using Bisection Method or Regula Falsi with tkinter module for GUI and Python

## 2 ways to run the program
    
    1. Run from script
        make sure to have python installed in your device (Python 3.11.1)
        pip install -r requirements
        python main.py
        
    2. Bundle the Script to exe
        Turn off you anti-virus or windows security, you can toggle it back after pyinstaller is done
        python -m venv .\venv
        .\venv\Scripts\activate.bat
        pip install -r requirements.txt
        python -m PyInstaller --add-data "assets/frame0/*;assets/frame0/" --onefile -w --icon="assets\frame0\bisection_icon.ico" main.py
        dist\main.exe

# How to Switch root finding algorithm
    Click the Circular Arrow

## There are 3 Input Fields and 1 Result Field:
        f(x) = The Function
        x_0 = First Guess
        x_1 = Second Guess
        r = Result after doing bisection method
    
## Input
        The User can input using the Buttons in GUI or through Keyboard
        
### Key Mapping 
    The mapping of Numbers, Mathematical Operations, modulo operator (%), decimal point (.) is one is to one,
    meaning when you press it using the keyboard it will put the corressponding key to the focused entry

    Return or Enter Key - Will trigger the equal button showing the result in the "r" Result Field.
    In case the inputs are invalid it will cause the "r" field to output "Invalid Input.
    The Enter key will also show the Iterations of the Bisection Method and the use will have
    the choice to export the result to a ".txt" file. 


