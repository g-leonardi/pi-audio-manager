import os
import xml.etree.ElementTree as ET

class CarlaPresetParser:
    def __init__(self, preset_path: str, output_base_dir: str):
        self.preset_path = preset_path
        self.preset_name = os.path.splitext(os.path.basename(preset_path))[0]
        self.output_dir = os.path.join(output_base_dir, self.preset_name)
        self.tree = ET.parse(preset_path)
        self.root = self.tree.getroot()

    def extract_plugins(self):
        return self.root.findall(".//Plugin")

    def extract_connections(self):
        return self.root.find("ExternalPatchbay")

    def save_plugins(self):
        os.makedirs(self.output_dir, exist_ok=True)

        plugins = self.extract_plugins()

        for i, plugin in enumerate(plugins):
            # Prova a recuperare il nome leggibile del plugin
            plugin_name_elem = plugin.find("./Info/Name")
            plugin_name = plugin_name_elem.text if plugin_name_elem is not None else f"plugin_{i}"
            filename_safe = "".join(c if c.isalnum() else "_" for c in plugin_name)

            file_path = os.path.join(self.output_dir, f"{i:02d}_{filename_safe}.xml")
            plugin_tree = ET.ElementTree(plugin)
            plugin_tree.write(file_path, encoding="utf-8", xml_declaration=True)

        print(f"Salvati {len(plugins)} plugin in: {self.output_dir}")

        self.save_connections()

    def save_connections(self):
        connections_elem = self.extract_connections()
        if connections_elem is not None:
            file_path = os.path.join(self.output_dir, "connections.xml")
            conn_tree = ET.ElementTree(connections_elem)
            conn_tree.write(file_path, encoding="utf-8", xml_declaration=True)
            print(f"Salvate le connessioni in: {file_path}")
        else:
            print("Nessun blocco ExternalPatchbay trovato: connessioni non salvate.")
