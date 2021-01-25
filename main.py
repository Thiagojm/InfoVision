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
right_hits = 0
percent = 0.0
ongoing = False


layout = [[sg.Text("Press a key or scroll mouse")],
          [sg.Image(filename="src/white.png", key="image")],
          [sg.Text("Você escolheu a cor: "), sg.Text("", size=(18, 1), key='text'),
           sg.Text("Número da rodada: "), sg.Text("0", size=(18, 1), key='COUNT'),
           sg.Text("Acertos: "), sg.Text(f"{right_hits} ({percent}%)", size=(18, 1), key='HITS')],
          [sg.Button("Start", key='START/STOP')],
          [sg.Button("Exit", key='EXIT')]]

window = sg.Window("Keyboard Test", layout,
                   return_keyboard_events=True, use_default_focus=False)

# ---===--- Loop taking in user input --- #
while True:
    event, values = window.read()
    text_elem = window['text']
    img_element = window["image"]
    count_element = window["COUNT"]
    percent_element = window['HITS']
    if event in ("EXIT", None):
        print(event, "exiting")
        break
    if event == "START/STOP":
        if not ongoing:
            ongoing = True
            doc_name = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
            act_image = random.choice(list(image_dict.keys()))
            img_element.update(image_dict[act_image])
            count = 1
            count_element.update(count)
            window['START/STOP'].update("Stop")
        else:
            count = 0
            doc_name = None
            act_image = None
            hit = None
            right_hits = 0
            percent = 0.0
            img_element.update("src/white.png")
            text_elem.update(" ")
            percent_element.update(f"{right_hits} ({percent}%)")
            count_element.update(count)
            window['START/STOP'].update("Start")
            ongoing = False
    if event in events_list:
        #act_image = random.choice(list(image_dict.values()))
        text_elem.update(events_dict[event])
        if act_image == events_dict[event]:
            hit = True
            right_hits += 1
        else:
            hit = False
        #print(f"{count}, {act_image}, {events_dict[event]}")
        with open(f'{doc_name}.csv', 'a+') as fd:
            fd.write(f"{count}, {act_image}, {events_dict[event]}, {hit}\n")
        percent = round(float(right_hits * 100/ count), 2)
        percent_element.update(f"{right_hits} ({percent}%)")
        count += 1
        count_element.update(count)
        act_image = random.choice(list(image_dict.keys()))
        img_element.update(image_dict[act_image])
        #print(event, "=D")
    # if event == "STOP":
    #     count = 0
    #     doc_name = None
    #     act_image = None
    #     hit = None
    #     right_hits = 0
    #     percent = 0.0
    #     img_element.update("src/white.png")
    #     text_elem.update(" ")
    #     percent_element.update(f"{right_hits} ({percent}%)")
    #     count_element.update(count)


window.close()