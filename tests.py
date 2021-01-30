import serial
from serial.tools import list_ports
from bitstring import BitArray
import time

def trng3_random():
    blocksize = 4096
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
        ta0 = time.time()
        a = bin(int(x.hex(), base=16))[2:].zfill(8 * blocksize)
        ta1 = time.time()
        print(ta1, ta0)
        tb0 = time.time()
        bin_hex = BitArray(x)  # bin to hex
        bin_ascii = bin_hex.bin  # hex to ASCII
        tb1 = time.time()
        print(tb1, tb0)
        print(f"Hex: {x}, Hex2: {x.hex()}, Int: {int(x.hex(), base=16)}, Bits: {a}, BitArray: {bin_ascii}")
        print(f"Equal?: {a == bin_ascii}")
        print(f"Metodo a total time: {ta1 - ta0}, Metodo BitArray total time: {tb1 - tb0}")
    except Exception:
        return

trng3_random()


# import winsound
# frequency = 500  # Set Frequency To 1000 Hertz
# duration = 250  # Set Duration To 250 ms
# winsound.Beep(frequency, duration)

# import secrets
#
# lista = [1, 2, 3, 4]
#
# x = secrets.choice(lista)
# print(x)