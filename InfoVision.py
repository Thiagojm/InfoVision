# Internal Imports
import secrets
from datetime import datetime
import time
import winsound
import os

# External Imports
import PySimpleGUI as sg
import serial
from serial.tools import list_ports

# Global Variables
azul_som = "src/sounds/azul.wav"
amarelo_som = "src/sounds/amarelo.wav"
vermelho_som = "src/sounds/vermelho.wav"
verde_som = "src/sounds/verde.wav"


def trng3_random():
    blocksize = 1
    ports_avaiable = list(list_ports.comports())
    rng_com_port = None
    for temp in ports_avaiable:
        if temp[1].startswith("TrueRNG"):
            if rng_com_port == None:  # always chooses the 1st TrueRNG found
                rng_com_port = str(temp[0])
    try:
        ser = serial.Serial(port=rng_com_port, timeout=10)  # timeout set at 10 seconds in case the read fails
        if (ser.isOpen() == False):
            ser.open()
        ser.setDTR(True)
        ser.flushInput()
    except Exception:
        return
    try:
        x = ser.read(blocksize)  # read bytes from serial port
    except Exception:
        return
    ser.close()
    bin_ascii = bin(int(x.hex(), base=16))[2:].zfill(8 * blocksize)  # bin to ascii
    bin_ascii_2 = bin_ascii[0:2]
    if bin_ascii_2 == "00":
        return "Vermelho"
    elif bin_ascii_2 == "01":
        return "Amarelo"
    elif bin_ascii_2 == "10":
        return "Azul"
    else:
        return "Verde"


def get_name():
    user_name = sg.popup_get_text("Nome do Usuário")
    return user_name


def play_color_sound(act_image):
    if act_image == "Vermelho":
        winsound.PlaySound(vermelho_som, winsound.SND_FILENAME)
    elif act_image == "Amarelo":
        winsound.PlaySound(amarelo_som, winsound.SND_FILENAME)
    elif act_image == "Azul":
        winsound.PlaySound(azul_som, winsound.SND_FILENAME)
    elif act_image == "Verde":
        winsound.PlaySound(verde_som, winsound.SND_FILENAME)
    else:
        return


def open_folder():
    script_path = os.getcwd()
    path = f"{script_path}/1- Saved Files/"
    path = os.path.realpath(path)
    os.startfile(path)


def main():
    events_list = ["a", "s", "d", "f", "A", "S", "D", "F"]
    events_dict = {"a": "Amarelo", "s": "Azul", "d": "Verde", "f": "Vermelho", "A": "Amarelo", "S": "Azul",
                   "D": "Verde", "F": "Vermelho"}
    image_dict = {"Vermelho": "src/images/red.png", "Amarelo": "src/images/yellow.png", "Azul": "src/images/blue.png",
                  "Verde": "src/images/green.png"}
    count = 0
    doc_name = None
    save_folder = "1- Saved Files/"
    act_image = None
    hit = None
    right_hits = 0
    percent = 0.0
    ongoing = False
    user_name = "Default"
    # Beep config
    frequency = 500  # Set Frequency To 1000 Hertz
    duration = 250  # Set Duration To 250 ms
    # Font
    text_normal = "Calibri, 14"
    text_big = "Calibri, 16"

    # DarkGrey5, LightBlue6
    sg.theme('LightBlue6')

    layout = [[sg.Text("Nome do Usuário: ", font=text_big), sg.T('Default', key="user_name", relief="sunken", size=(23, 1), font=text_normal),
               sg.B("Change User", k="user_button", font=text_big)],
              [sg.Radio('Pseudo-Random', "RADIO1", default=True, k="pseudo", font=text_normal), sg.Radio('TrueRNG3', "RADIO1", k="trng", font=text_normal),
               sg.T("   |   "), sg.Radio('Sound on', "RADIO2", default=True, k="sound_on", font=text_normal),
               sg.Radio('Sound off', "RADIO2", k="sound_off", font=text_normal)],
              [sg.Text("Legenda: ", font=text_big), sg.Text("A = AMARELO, S = AZUL, D = VERDE, F = VERMELHO, ESPAÇO = OUÇA A COR", font=text_normal)],
              [sg.T(size=(24, 1)), sg.Image(filename="src/images/white.png", key="image")],
              [sg.Text("Você escolheu a cor: ", font=text_big), sg.Text("", key='text', size=(9, 1), font=text_normal), sg.Text("Número da rodada: ", font=text_big),
               sg.Text("0", key='COUNT', size=(3, 1), font=text_normal), sg.Text("Acertos: ", font=text_big),
               sg.Text(f"{right_hits} ({percent}%)", key='HITS', size=(10, 1), font=text_normal)],
              [sg.T(size=(2, 1)), sg.Button("START", key='START/STOP', size=(20, 1), font=text_big),
               sg.Button("OPEN OUTPUT FOLDER", key='OUTPUT', size=(20, 1), font=text_big), sg.Button("EXIT", key='EXIT', size=(20, 1), font=text_big)]]

    window = sg.Window("InfoVision 1.0 - by Thiago Jung", layout, return_keyboard_events=True, use_default_focus=False,
                       location=(300, 20), icon=("src/images/tapa_olho.ico"))

    # ---===--- Loop taking in user input --- #
    while True:
        event, values = window.read()
        user_name_text = window['user_name']
        text_elem = window['text']
        img_element = window["image"]
        count_element = window["COUNT"]
        percent_element = window['HITS']
        if event in ("EXIT", None):
            print(event, "exiting")
            break
        if event == "OUTPUT":
            open_folder()
        if event == "user_button":
            user_name = get_name()
            user_name_text.update(user_name)
        if event == " ":
            if ongoing:
                play_color_sound(act_image)
        if event == "START/STOP":
            if not ongoing:
                try:
                    ongoing = True
                    doc_name_time = datetime.now().strftime(f"{user_name}_%Y_%m_%d-%H_%M_%S")
                    doc_name = save_folder + doc_name_time
                    sg.popup_no_buttons("Iniciando em 3 segundos, aguarde...", auto_close_duration=3, auto_close=True,
                                        non_blocking=True, icon=("src/images/tapa_olho.ico"))
                    time.sleep(3)
                    if values["pseudo"]:
                        act_image = secrets.choice(list(image_dict.keys()))
                    else:
                        act_image = trng3_random()
                    if values["sound_on"]:
                        winsound.Beep(frequency, duration)
                    img_element.update(image_dict[act_image])
                    count = 1
                    count_element.update(count)
                    window['START/STOP'].update("STOP")
                except Exception:
                    sg.popup_ok("Warning!", "Read failed! Try using Pseudo-Random mode.",
                                icon=("src/images/tapa_olho.ico"))
                    count = 0
                    doc_name = None
                    act_image = None
                    hit = None
                    right_hits = 0
                    percent = 0.0
                    img_element.update("src/images/white.png")
                    text_elem.update(" ")
                    percent_element.update(f"{right_hits} ({percent}%)")
                    count_element.update(count)
                    window['START/STOP'].update("START")
                    ongoing = False
            else:
                count = 0
                doc_name = None
                act_image = None
                hit = None
                right_hits = 0
                percent = 0.0
                img_element.update("src/images/white.png")
                text_elem.update(" ")
                percent_element.update(f"{right_hits} ({percent}%)")
                count_element.update(count)
                window['START/STOP'].update("START")
                ongoing = False
        if event in events_list:
            try:
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
                    percent = round(float(right_hits * 100 / count), 2)
                    percent_element.update(f"{right_hits} ({percent}%)")
                    count += 1
                    count_element.update(count)
                    if values["pseudo"]:
                        act_image = secrets.choice(list(image_dict.keys()))
                    else:
                        act_image = trng3_random()
                    if values["sound_on"]:
                        winsound.Beep(frequency, duration)
                    img_element.update(image_dict[act_image])
            except Exception:
                sg.popup_ok("Warning!", "Read failed! Try using Pseudo-Random mode.", icon=("src/images/tapa_olho.ico"))
                count = 0
                doc_name = None
                act_image = None
                hit = None
                right_hits = 0
                percent = 0.0
                img_element.update("src/images/white.png")
                text_elem.update(" ")
                percent_element.update(f"{right_hits} ({percent}%)")
                count_element.update(count)
                window['START/STOP'].update("START")
                ongoing = False

    window.close()


if __name__ == '__main__':
    main()
