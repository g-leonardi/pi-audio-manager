import os
import xml.etree.ElementTree as ET

class CarlaPresetUpdater:
    def __init__(self, original_preset_path: str, plugins_input_dir: str, output_preset_path: str):
        self.original_preset_path = original_preset_path
        self.plugins_input_dir = plugins_input_dir
        self.output_preset_path = output_preset_path

        self.tree = ET.parse(original_preset_path)
        self.root = self.tree.getroot()

    def _get_plugin_name(self, plugin_elem):
        name_elem = plugin_elem.find("./Info/Name")
        return name_elem.text.strip() if name_elem is not None else None

    def _load_new_plugins(self):
        new_plugins = {}
        for file in os.listdir(self.plugins_input_dir):
            if file.endswith(".xml"):
                file_path = os.path.join(self.plugins_input_dir, file)
                try:
                    plugin_tree = ET.parse(file_path)
                    plugin_root = plugin_tree.getroot()
                    plugin_name = self._get_plugin_name(plugin_root)
                    if plugin_name:
                        new_plugins[plugin_name] = plugin_root
                except Exception as e:
                    print(f"Errore nel parsing di {file}: {e}")
        return new_plugins

    def update_preset(self):
        updated_count = 0
        untouched_count = 0
        new_plugins = self._load_new_plugins()
        all_plugin_elems = self.root.findall(".//Plugin")

        for i, plugin in enumerate(all_plugin_elems):
            original_name = self._get_plugin_name(plugin)
            if original_name in new_plugins:
                new_elem = new_plugins[original_name]
                parent = plugin.getparent() if hasattr(plugin, 'getparent') else plugin.find("..")
                # sostituiamo nel DOM
                self.root.find(".//Plugin[{0}]".format(i + 1)).clear()
                self.root.find(".//Plugin[{0}]".format(i + 1)).extend(new_elem)
                updated_count += 1
                print(f"Sostituito plugin: {original_name}")
            else:
                untouched_count += 1
                print(f"Plugin invariato: {original_name}")

        self.tree.write(self.output_preset_path, encoding="utf-8", xml_declaration=True)
        print(f"\nAggiornamento completato.")
        print(f"Plugin aggiornati: {updated_count}")
        print(f"Plugin invariati: {untouched_count}")
        print(f"Nuovo file salvato in: {self.output_preset_path}")
