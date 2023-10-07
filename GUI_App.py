import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import subprocess

class FlaskApiGui(tk.Tk):
    def api_request(self, endpoint):
        try:
            response = requests.get(f"http://127.0.0.1:5000{endpoint}")
            if response.status_code == 200:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.INSERT, response.json())
            else:
                messagebox.showerror("Error", f"API returned {response.status_code}: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def __init__(self):
        super().__init__()

        self.title("Flask API GUI")
        self.geometry("600x400")

        # Create buttons for each API function
        self.create_button("Get All Network Devices", self.get_network_devices)
        self.create_button("Get Health Status", self.get_health_status)
        self.create_button("Get Physical Topology", self.get_physical_topology)
        self.create_button("Get All Discoveries", self.get_discoveries)
        self.create_button("Get All Health Issues", self.get_health_issues)

        # Scrolled text widget to display API responses
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=70, height=10)
        self.text_area.grid(column=0, row=6, padx=10, pady=10, columnspan=2)

    def create_button(self, text, command):
        btn = tk.Button(self, text=text, command=command)
        btn.grid(padx=10, pady=5, sticky=tk.W+tk.E)

    def get_network_devices(self):
        self.api_request("/network-device")

    def get_health_status(self):
        self.api_request("/assurance/health")

    def get_physical_topology(self):
        self.api_request("/topology/physical-topology")

    def get_discoveries(self):
        self.api_request("/discovery")

    def get_health_issues(self):
        self.api_request("/assurance/health-issues")


if __name__ == '__main__':
    flask_process = subprocess.Popen(["python", "app.py"])
    app = FlaskApiGui()
    app.mainloop()
    flask_process.terminate()