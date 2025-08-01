from core.startup_manager import StartupManager
from core.vst_manager import VSTManager
from core.carla_parser import CarlaPresetParser

def main():
    while True:
        print("\nSeleziona un'opzione:")
        print("1. Avvia audio")
        print("2. Lista VST installati")
        print("3. Estrai preset da Carla")
        print("4. Il metodo di Ciccio")
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
        elif scelta.lower() == "q":
            print("Uscita dal programma. Ciao!")
            break
        else:
            print("Scelta non valida.")


if __name__ == "__main__":
    main()
