from time import sleep
from guizero import PushButton, App, Text
from kobukidriver import Kobuki

def stop():
    kobuki_instance.play_button_sound()
    kobuki_instance.move(0,0,0)

def forward():
    kobuki_instance.play_button_sound()
    kobuki_instance.move(255,255,0)

def right():
    kobuki_instance.play_button_sound()
    kobuki_instance.move(-255,255,0)

def left():
    kobuki_instance.play_button_sound()
    kobuki_instance.move(255,-255,0)

def reverse():
    kobuki_instance.play_button_sound()
    kobuki_instance.move(-255,-255,0)

if __name__ == '__main__':    
    kobuki_instance=Kobuki()
    app = App(title="GUI Development", layout="grid")
    message = Text(app, text="NAVIGATOR By HDK", grid=[1,0])

    button1 = PushButton(app, command=forward, grid = [1,1], text="forward", width=10,height=3)
    button2 = PushButton(app, command=reverse, grid = [1,3], text="reverse", width=10,height=3)
    button3 = PushButton(app, command=right, grid=[2,2], text = "right", width=10,height=3)
    button4 = PushButton(app, command=left, grid=[0,2], text="left", width=10, height=3)
    button4 = PushButton(app, command=stop, grid=[1,2] , text="stop", width=10, height=3)


    app.display()


x