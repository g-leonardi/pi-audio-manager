from core.startup_manager import StartupManager
from core.vst_manager import VSTManager
from core.carla_parser import CarlaPresetParser
from core.audio_recorder import AudioRecorder
from core.carla_preset_updater import CarlaPresetUpdater


def main():
    while True:
        print("\nSeleziona un'opzione:")
        print("1. Avvia audio")
        print("2. Lista VST installati")
        print("3. Estrai preset da Carla")
        print("4. Il metodo di Ciccio")
        print("5. Registra audio dal preset attuale")	
        print("6. Modifica il preset di carla seguendo chatGPT")
        print("q. Esci")
        scelta = input(">> ")

        if scelta == "1":
            print("Eseguo: Avvia audio...")
            sm = StartupManager(args=["only_audio"])
            sm.run_startup_script()
            print("Completato: Avvio audio terminato.")
        elif scelta == "2":
            print("Eseguo: Lista VST installati...")
            vm = VSTManager()	
            controls = vm.list_vst_plugins(debug=True)
            vm.save_controls_json()
            print("Plugin trovati:", list(controls.keys()))
            print("Completato: Lista VST mostrata.")
        elif scelta == "3":
            print("Eseguo: Estrai preset da Carla...")
            parser = CarlaPresetParser("/home/pi/test.carxp", "/home/pi/Desktop/ScriptPython/audio_manager/data")
            parser.save_plugins()
            print("Completato: Estrazione preset terminata.")
        elif scelta == "5":
            print("Eseguo: Registrazione da Carla...")
            recorder = AudioRecorder()
            recorder.record_until_keypress()
            print("Completato: Registrazione terminata.")
        elif scelta == "6":
            print("Eseguo: Aggiorna preset Carla con plugin da cartella...")
            original = "/home/pi/carlaNAM.carxp"
            plugin_folder = "/home/pi/Desktop/ScriptPython/audio_manager/my_updated_plugins"
            output = "/home/pi/Desktop/ScriptPython/audio_manager/data/test_updated.carxp"
            updater = CarlaPresetUpdater(original, plugin_folder, output)
            updater.update_preset()
            print("Completato: Aggiornamento preset.")

        elif scelta.lower() == "q":
            print("Uscita dal programma. Ciao!")
            break
        else:
            print("Scelta non valida.")


if __name__ == "__main__":
    main()
