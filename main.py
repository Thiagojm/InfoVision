# Internal Imports
import sys
import random
from datetime import datetime

# External Imports
import PySimpleGUI as sg

# Recipe for getting keys, one at a time as they are released
# If want to use the space bar, then be sure and disable the "default focus"

events_list = ("a", "s", "d", "f")
events_dict = {"a": "Vermelho", "s": "Amarelo", "d": "Azul", "f": "Verde", " ": "src/white.png"}
image_dict = {"Vermelho": "src/red.png", "Amarelo": "src/yellow.png", "Azul": "src/blue.png", "Verde": "src/green.png"}
count = 0
doc_name = None
act_image = None
hit = None

layout = [[sg.Text("Press a key or scroll mouse")],
          [sg.Image(filename="src/white.png", key="image")],
          [sg.Text("Você escolheu a cor: "), sg.Text("", size=(18, 1), key='text'), sg.Text("Número de rodadas: "), sg.Text("0", size=(18, 1), key='COUNT')],
          [sg.Button("Start", key='START'), sg.Button("Stop", key='STOP')],
          [sg.Button("Exit", key='EXIT')]]

window = sg.Window("Keyboard Test", layout,
                   return_keyboard_events=True, use_default_focus=False)

# ---===--- Loop taking in user input --- #
while True:
    event, values = window.read()
    text_elem = window['text']
    img_element = window["image"]
    count_element = window["COUNT"]
    if event in ("EXIT", None):
        print(event, "exiting")
        break
    if event == "START":
        doc_name = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        img_element.update(random.choice(list(image_dict.values())))
        count = 1
        count_element.update(count)
    if event in events_list:
        #act_image = random.choice(list(image_dict.values()))
        act_image = random.choice(list(image_dict.keys()))
        img_element.update(image_dict[act_image])
        text_elem.update(events_dict[event])
        if act_image == events_dict[event]:
            hit = True
        else:
            hit = False
        print(f"{count}, {act_image}, {events_dict[event]}")
        with open(f'{doc_name}.csv', 'a+') as fd:
            fd.write(f"{count}, {act_image}, {events_dict[event]}, {hit}\n")
        count += 1
        count_element.update(count)
        print(event, "=D")


window.close()