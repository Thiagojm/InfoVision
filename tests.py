from playsound import playsound
import winsound


azul_som = "src/sounds/azul.wav"
# playsound(azul, block=True)
winsound.PlaySound(azul, winsound.SND_FILENAME)