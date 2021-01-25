# Internal Imports
import random
from datetime import datetime
import time

# External Imports
import PySimpleGUI as sg
from bitstring import BitArray
import serial
from serial.tools import list_ports


def trng3_random():
    # global thread_cap
    # sample_value = int(values["ac_bit_count"])
    # interval_value = int(values["ac_time_count"])
    blocksize = 1
    ports_avaiable = list(list_ports.comports())
    rng_com_port = None
    for temp in ports_avaiable:
        if temp[1].startswith("TrueRNG"):
            if rng_com_port == None:  # always chooses the 1st TrueRNG found
                rng_com_port = str(temp[0])
    # file_name = time.strftime(f"%Y%m%d-%H%M%S_trng_s{sample_value}_i{interval_value}")
    # file_name = f"1-SavedFiles/{file_name}"
    # while thread_cap:
    #     start_cap = time.time()
    #     with open(file_name + '.bin', "ab") as bin_file:  # save binary file
    try:
        ser = serial.Serial(port=rng_com_port, timeout=10)  # timeout set at 10 seconds in case the read fails
        if (ser.isOpen() == False):
            ser.open()
        ser.setDTR(True)
        ser.flushInput()
    except Exception:
        sg.popupmsg("Warning!", f"Port Not Usable! Do you have permissions set to read {rng_com_port}?")
        # # thread_cap = False
        # window['ac_button'].update("Start")
        # window["stat_ac"].update("        Idle", text_color="orange")
        # break
    try:
        x = ser.read(blocksize)  # read bytes from serial port
    except Exception:
        sg.popupmsg("Warning!", "Read failed!")
        # thread_cap = False
        # window['ac_button'].update("Start")
        # window["stat_ac"].update("        Idle", text_color="orange")
        # break
    # bin_file.write(x)
    ser.close()
    bin_hex = BitArray(x)  # bin to hex
    bin_ascii = bin_hex.bin  # hex to ASCII
    bin_ascii_2 = bin_ascii[0:2]
    # bin_ascii_3_count = bin_ascii_3.count('1')  # count numbers of ones in the string
    # with open(file_name + '.csv', "a+") as write_file:  # open file and append time and number of ones
    #     write_file.write(f'{strftime("%H:%M:%S", localtime())} {num_ones_array}\n')
    # end_cap = time.time()
    # print(interval_value - (end_cap - start_cap))
    # try:
    #     time.sleep(interval_value - (end_cap - start_cap))
    # except Exception:
    #     pass
    print(bin_ascii_2)
    if bin_ascii_2 == "00":
        return 0
    elif bin_ascii_2 == "01":
        return 1
    elif bin_ascii_2 == "10":
        return 2
    else:
        return 3




def main():
    events_list = ("a", "s", "d", "f")
    events_dict = {"a": "Vermelho", "s": "Amarelo", "d": "Azul", "f": "Verde", " ": "src/white.png"}
    image_dict = {"Vermelho": "src/red.png", "Amarelo": "src/yellow.png", "Azul": "src/blue.png", "Verde": "src/green.png"}
    image_list = ["Vermelho", "Amarelo", "Azul", "Verde"]
    count = 0
    doc_name = None
    act_image = None
    hit = None
    right_hits = 0
    percent = 0.0
    ongoing = False


    layout = [[sg.Text("Nome do Usuário: "), sg.Listbox(values=('Mony', "Thi"), key="user_name", default_values='Mony', size=(18, 2)),
               sg.Text("A = VERMELHO, S = AMARELO, D = AZUL, F = VERDE")],
              [sg.Radio('Pseudo-Random', "RADIO1", default=True, k="pseudo"), sg.Radio('TrueRNG3', "RADIO1", k="trng")],
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
            print(values)
            if not ongoing:
                ongoing = True
                doc_name = datetime.now().strftime(f"{values['user_name'][0]}_%Y_%m_%d-%H_%M_%S")
                if values["pseudo"]:
                    act_image = random.choice(list(image_dict.keys()))
                else:
                    act_image = image_list[trng3_random()]
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
                if values["pseudo"]:
                    act_image = random.choice(list(image_dict.keys()))
                else:
                    act_image = image_list[trng3_random()]
                # act_image = random.choice(list(image_dict.keys()))
                img_element.update(image_dict[act_image])


    window.close()

if __name__ == '__main__':
    main()