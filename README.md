# Mouse Mover

Mouse movement simulator  

![alt text](https://i.imgur.com/NRVNYZA.png)  

Mouse Mover is a Python application that can be used to simulate cursor movement. This project is heavily inspired by the infamous [Mouse Jiggler](https://mouse-jiggler.en.uptodown.com/windows) application. One of the main purposes of using this application is to prevent screen saver or auto-lock in the case where you can't disable them.

## Download  
Download the executable for Windows [HERE](https://sourceforge.net/projects/python-mouse-mover/) or compile the program yourself by following the guide below.
  
  
## Dependencies Installation

To install the dependencies, navigate to the project directory and execute this command:

```bash
pip install -r requirements.txt
```

## Usage

To use Mouse  Mover, navigate to the `mousemover` directory within the project directory and execute this command:
```bash
python mousemover.py
```
| Settings | Description |
|----------|-------------|
|Enable Timer | Enable and configure the timer this application will run. Disabling this will make the application runs indefinitely. |
| Random Movement | Randomize the movement of the mouse so that it doesn't leave any pattern.
| Random Delay Interval | Randomize the interval between the movement.
| Close Button Minimize to Tray | When enabled, pressing the close button will minimize the application to system tray instead of closing it |



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/)
