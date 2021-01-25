# Internal Imports
import random
from datetime import datetime
import time

# External Imports
import PySimpleGUI as sg

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


layout = [[sg.Text("Nome do Usuário: "), sg.Listbox(values=('Mony', "Thi"), key="user_name", default_values='Mony', size=(18, 2)),
           sg.Text("a = vermelho, s = amarelo, d = azul, f = verde")],
          [sg.Image(filename="src/white.png", key="image")],
          [sg.Text("Você escolheu a cor: "), sg.Text("", size=(18, 1), key='text'),
           sg.Text("Número da rodada: "), sg.Text("0", size=(18, 1), key='COUNT'),
           sg.Text("Acertos: "), sg.Text(f"{right_hits} ({percent}%)", size=(18, 1), key='HITS')],
          [sg.Button("Start", key='START/STOP')],
          [sg.Button("Exit", key='EXIT')]]

window = sg.Window("InfoVision 1.0", layout,
                   return_keyboard_events=True, use_default_focus=False, location=(300, 20))

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
            doc_name = datetime.now().strftime(f"{values['user_name'][0]}_%Y_%m_%d-%H_%M_%S")
            act_image = random.choice(list(image_dict.keys()))
            time.sleep(3)
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
        if ongoing:
            text_elem.update(events_dict[event])
            if act_image == events_dict[event]:
                hit = True
                right_hits += 1
            else:
                hit = False
            percent = round(float(right_hits * 100 / count), 2)
            with open(f'{doc_name}.csv', 'a+') as fd:
                fd.write(f"{count}, {act_image}, {events_dict[event]}, {hit}, {percent}\n")
            percent = round(float(right_hits * 100/ count), 2)
            percent_element.update(f"{right_hits} ({percent}%)")
            count += 1
            count_element.update(count)
            act_image = random.choice(list(image_dict.keys()))
            img_element.update(image_dict[act_image])


window.close()