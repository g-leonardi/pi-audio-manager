from core.startup_manager import StartupManager
#from core.vst_manager import VSTManager
#from core.carla_parser import CarlaParser

def main():
    print("Seleziona un'opzione:")
    print("1. Avvia audio")
    print("2. Lista VST installati")
    print("3. Estrai preset da Carla")
    scelta = input(">> ")

    if scelta == "1":
        sm = StartupManager(args=["only_audio"])
        sm.run_startup_script()
    elif scelta == "2":
        #vm = VSTManager()
        #vst = vm.list_vst_plugins()
        print("Plugin trovati:", vst)
    elif scelta == "3":
        #cp = CarlaParser()
        #cp.extract_current_chain_parameters()
    else:
        print("Scelta non valida.")

if __name__ == "__main__":
    main()
