import os
import json
from rdflib import Graph, Namespace, RDF, RDFS

LV2 = Namespace("http://lv2plug.in/ns/lv2core#")
ATOM = Namespace("http://lv2plug.in/ns/ext/atom#")
UNITS = Namespace("http://lv2plug.in/ns/extensions/units#")

class VSTManager:
    plugin_filter = [
        "urn:zamaudio:ZamTube",
        "http://guitarix.sourceforge.net/plugins/gx_ultracab_#_ultracab_",
        "http://calf.sourceforge.net/plugins/Equalizer12Band",
        "http://calf.sourceforge.net/plugins/Compressor",
        "urn:dragonfly:plate",
        "http://calf.sourceforge.net/plugins/Limiter",
        "http://github.com/mikeoliphant/neural-amp-modeler-lv2"
    ]

    def __init__(self, directories=None, filter_plugins=False):
        if directories is None:
            directories = ["/usr/lib/lv2", os.path.expanduser("~/.lv2")]
        self.directories = directories
        self.filter_plugins = filter_plugins
        self.controls = {}

    def extract_plugin_controls(self, ttl_path, debug=False):
        g = Graph()
        g.parse(ttl_path, format='turtle')

        controls = {}

        for plugin in g.subjects(RDF.type, LV2.Plugin):
            plugin_name = g.value(plugin, RDFS.label)
            if plugin_name is None:
                plugin_name = str(plugin).split('#')[-1]
            plugin_name = str(plugin_name)

            if self.filter_plugins and self.plugin_filter and plugin_name not in self.plugin_filter:
                continue

            controls[plugin_name] = []

            for port in g.objects(plugin, LV2.port):
                if debug:
                    print(f"\n--- Porta: {port}")
                    for p, o in g.predicate_objects(port):
                        print(f"  {p} -> {o}")

                param_data = {}

                symbol = g.value(port, LV2.symbol)
                param_data['uri'] = str(symbol) if symbol else str(port)

                label = g.value(port, RDFS.label)
                name = g.value(port, LV2.name)
                if label:
                    param_data['name'] = str(label)
                elif name:
                    param_data['name'] = str(name)
                elif symbol:
                    param_data['name'] = str(symbol)
                else:
                    param_data['name'] = str(port).split('#')[-1]

                types = list(g.objects(port, RDF.type))
                param_data['types'] = []
                for t in types:
                    t_str = str(t)
                    if '#' in t_str:
                        param_data['types'].append(t_str.split('#')[-1])
                    elif '/' in t_str:
                        param_data['types'].append(t_str.split('/')[-1])
                    else:
                        param_data['types'].append(t_str)

                min_val = g.value(port, LV2.minimum)
                max_val = g.value(port, LV2.maximum)
                default_val = g.value(port, LV2.default)

                try:
                    param_data['min'] = float(min_val) if min_val else None
                except:
                    param_data['min'] = None

                try:
                    param_data['max'] = float(max_val) if max_val else None
                except:
                    param_data['max'] = None

                try:
                    param_data['default'] = float(default_val) if default_val else None
                except:
                    param_data['default'] = None

                unit = g.value(port, UNITS.unit)
                param_data['unit'] = str(unit) if unit else None

                atom_path = g.value(port, ATOM.path)
                if atom_path is not None:
                    param_data['atom_path'] = str(atom_path)

                controls[plugin_name].append(param_data)

        return controls

    def find_ttl_files(self):
        ttl_files = []
        for directory in self.directories:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.ttl'):
                        ttl_files.append(os.path.join(root, file))
        return ttl_files

    def list_vst_plugins(self, debug=False):
        self.controls = {}
        ttl_files = self.find_ttl_files()
        if debug:
            print(f"Trovati {len(ttl_files)} file .ttl nelle directory {self.directories}")

        for ttl_file in ttl_files:
            if debug:
                print(f"Parsing {ttl_file}...")
            controls = self.extract_plugin_controls(ttl_file, debug=debug)
            for k, v in controls.items():
                if k in self.controls:
                    self.controls[k].extend(v)
                else:
                    self.controls[k] = v

        return self.controls

    def save_controls_json(self, filename="plugin_controls.json"):
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)  # crea la cartella se non c'è
        filepath = os.path.join(data_dir, filename)
        with open(filepath, "w") as f:
            json.dump(self.controls, f, indent=2)
        print(f"File JSON scritto in: {os.path.abspath(filepath)}")
