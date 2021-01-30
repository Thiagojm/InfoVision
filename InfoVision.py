# Internal Imports
import secrets
from datetime import datetime
import time
import winsound

# External Imports
import PySimpleGUI as sg
import serial
from serial.tools import list_ports


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
    bin_ascii = bin(int(x.hex(), base=16))[2:].zfill(8 * blocksize) # bin to ascii
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

def main():
    events_list = ("a", "s", "d", "f")
    events_dict = {"a": "Vermelho", "s": "Amarelo", "d": "Azul", "f": "Verde"}
    image_dict = {"Vermelho": "src/images/red.png", "Amarelo": "src/images/yellow.png", "Azul": "src/images/blue.png", "Verde": "src/images/green.png"}
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

    sg.theme('LightGreen')

    layout = [[sg.Text("Nome do Usuário: "), sg.T('Default User', key="user_name", relief="sunken", size=(10,1)), sg.B("Change User", k="user_button")],
               [sg.Radio('Pseudo-Random', "RADIO1", default=True, k="pseudo"), sg.Radio('TrueRNG3', "RADIO1", k="trng"),sg.T("   |   "),
                sg.Radio('Sound on', "RADIO2", default=True, k="sound_on"), sg.Radio('Sound off', "RADIO2", k="sound_off")],
               [sg.Text("Legenda: "), sg.Text("A = VERMELHO, S = AMARELO, D = AZUL, F = VERDE")],
              [sg.T(size=(7, 1)), sg.Image(filename="src/images/white.png", key="image")],
              [sg.Text("Você escolheu a cor: "), sg.Text("", key='text', size=(9, 1)),
               sg.Text("Número da rodada: "), sg.Text("0", key='COUNT', size=(3, 1)),
               sg.Text("Acertos: "), sg.Text(f"{right_hits} ({percent}%)", key='HITS', size=(10, 1))],
              [sg.T(size=(10, 1)), sg.Button("Start", key='START/STOP', size=(20, 1)), sg.Button("Exit", key='EXIT', size=(20, 1))]]

    window = sg.Window("InfoVision 1.0", layout,
                       return_keyboard_events=True, use_default_focus=False, location=(300, 20), icon=("src/images/tapa_olho.ico"))

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
        if event == "user_button":
            user_name = get_name()
            user_name_text.update(user_name)
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
                    window['START/STOP'].update("Stop")
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
                    window['START/STOP'].update("Start")
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
                window['START/STOP'].update("Start")
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
                    percent = round(float(right_hits * 100/ count), 2)
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
                window['START/STOP'].update("Start")
                ongoing = False

    window.close()

if __name__ == '__main__':
    main()