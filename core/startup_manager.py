import subprocess

class StartupManager:
    def __init__(self, script_path="/home/pi/Desktop/startup_audio.sh", args=None):
        self.script_path = script_path
        self.args = args or []

    def run_startup_script(self):
        cmd = ["bash", self.script_path] + self.args
        print(f"Eseguo comando: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
