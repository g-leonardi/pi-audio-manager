# core/audio_recorder.py

import os
import subprocess
import datetime

class AudioRecorder:
    def __init__(self, output_base_dir="/home/pi/Desktop/ScriptPython/audio_manager/data"):
        self.output_dir = os.path.join(output_base_dir, "recordings")
        os.makedirs(self.output_dir, exist_ok=True)

    def record_until_keypress(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_dir, f"carla_recording_{timestamp}.wav")

        print(f"Registrazione in corso... premi INVIO per fermare.")

        try:
            process = subprocess.Popen([
                "jack_capture",
                "--filename", output_file
            ])

            input(">> ")  # Attende un tasto
            process.terminate()
            process.wait()
            print(f"Registrazione salvata in: {output_file}")
        except FileNotFoundError:
            print("Errore: jack_capture non trovato. Assicurati che sia installato.")
        except Exception as e:
            print(f"Errore durante la registrazione: {e}")
