#!/usr/bin/env python3
"""
Lightweight Mobile App Builder Client
Connects to central server for building Android apps
Designed for POS computers with limited resources
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import requests
import websocket
import json
import threading
import time
import webbrowser
from datetime import datetime
import os
import sys

# Configuration
DEFAULT_SERVER_URL = "http://localhost:3000"  # Will be updated to ngrok URL
CONFIG_FILE = "client_config.json"

class MobileAppBuilderClient:
    def __init__(self):
        self.server_url = self.load_config()
        self.current_build_id = None
        self.ws = None
        self.setup_gui()
        self.check_server_connection()
    
    def load_config(self):
        """Load server configuration"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return config.get('server_url', DEFAULT_SERVER_URL)
        except:
            pass
        return DEFAULT_SERVER_URL
    
    def save_config(self):
        """Save server configuration"""
        try:
            config = {'server_url': self.server_url}
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
        except:
            pass
    
    def setup_gui(self):
        """Create the GUI interface"""
        self.root = tk.Tk()
        self.root.title("Mobile App Builder/Installer")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Main frame with blue header
        self.header_frame = tk.Frame(self.root, bg='#3498db', height=100)
        self.header_frame.pack(fill='x', padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        # Header title
        title_label = tk.Label(
            self.header_frame, 
            text="Mobile App Builder/Installer", 
            font=('Arial', 16, 'bold'),
            fg='white', 
            bg='#3498db'
        )
        title_label.pack(pady=20)
        
        # Configuration frame
        config_frame = tk.LabelFrame(
            self.root, 
            text="App Configuration", 
            font=('Arial', 10, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50',
            padx=10,
            pady=10
        )
        config_frame.pack(fill='x', padx=20, pady=10)
        
        # App URL
        tk.Label(
            config_frame, 
            text="App URL:", 
            font=('Arial', 9),
            bg='#ecf0f1'
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        self.url_entry = tk.Entry(
            config_frame, 
            font=('Arial', 9),
            width=80
        )
        self.url_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=(10, 0))
        self.url_entry.insert(0, "http://192.168.1.226/NEWKIOSK")\n        
        # App Name\n        tk.Label(\n            config_frame, \n            text=\"App Name:\", \n            font=('Arial', 9),\n            bg='#ecf0f1'\n        ).grid(row=1, column=0, sticky='w', pady=5)\n        \n        self.name_entry = tk.Entry(\n            config_frame, \n            font=('Arial', 9),\n            width=80\n        )\n        self.name_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=(10, 0))\n        self.name_entry.insert(0, \"My POS app\")\n        \n        config_frame.grid_columnconfigure(1, weight=1)\n        \n        # Action buttons frame\n        button_frame = tk.Frame(self.root, bg='#2c3e50')\n        button_frame.pack(fill='x', padx=20, pady=10)\n        \n        # Save Configuration button\n        self.save_btn = tk.Button(\n            button_frame,\n            text=\"💾 Save Configuration\",\n            font=('Arial', 10, 'bold'),\n            bg='#27ae60',\n            fg='white',\n            padx=20,\n            pady=10,\n            command=self.save_configuration\n        )\n        self.save_btn.pack(side='left', padx=5)\n        \n        # Build Android App button\n        self.build_btn = tk.Button(\n            button_frame,\n            text=\"📱 Build Android App\",\n            font=('Arial', 10, 'bold'),\n            bg='#3498db',\n            fg='white',\n            padx=20,\n            pady=10,\n            command=self.build_android_app\n        )\n        self.build_btn.pack(side='left', padx=5)\n        \n        # Retry Build button (initially hidden)\n        self.retry_btn = tk.Button(\n            button_frame,\n            text=\"🔄 Retry Build\",\n            font=('Arial', 10, 'bold'),\n            bg='#f39c12',\n            fg='white',\n            padx=20,\n            pady=10,\n            command=self.retry_build\n        )\n        \n        # Server Settings button\n        self.settings_btn = tk.Button(\n            button_frame,\n            text=\"⚙️ Server Settings\",\n            font=('Arial', 10, 'bold'),\n            bg='#95a5a6',\n            fg='white',\n            padx=20,\n            pady=10,\n            command=self.show_settings\n        )\n        self.settings_btn.pack(side='right', padx=5)\n        \n        # Server status\n        self.status_label = tk.Label(\n            self.root,\n            text=\"Server Status: Checking...\",\n            font=('Arial', 9),\n            bg='#2c3e50',\n            fg='#95a5a6'\n        )\n        self.status_label.pack(anchor='e', padx=20, pady=(0, 5))\n        \n        # Build Logs frame\n        logs_frame = tk.Frame(self.root, bg='#2c3e50')\n        logs_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))\n        \n        tk.Label(\n            logs_frame,\n            text=\"Build Logs:\",\n            font=('Arial', 10, 'bold'),\n            bg='#2c3e50',\n            fg='white'\n        ).pack(anchor='w', pady=(0, 5))\n        \n        # Log display\n        self.log_text = scrolledtext.ScrolledText(\n            logs_frame,\n            font=('Consolas', 9),\n            bg='#2c3e50',\n            fg='#ecf0f1',\n            insertbackground='white',\n            height=20\n        )\n        self.log_text.pack(fill='both', expand=True)\n        \n        # Progress bar\n        self.progress = ttk.Progressbar(\n            self.root,\n            mode='determinate',\n            length=300\n        )\n        self.progress.pack(fill='x', padx=20, pady=(10, 20))\n        \n    def check_server_connection(self):\n        \"\"\"Check if server is accessible\"\"\"\n        try:\n            response = requests.get(f\"{self.server_url}/api/status\", timeout=5)\n            if response.status_code == 200:\n                self.status_label.config(\n                    text=\"Server Status: ✅ Connected\",\n                    fg='#27ae60'\n                )\n                self.build_btn.config(state='normal')\n            else:\n                raise Exception(\"Server returned error status\")\n        except Exception as e:\n            self.status_label.config(\n                text=\"Server Status: ❌ Disconnected\",\n                fg='#e74c3c'\n            )\n            self.build_btn.config(state='disabled')\n            self.log(f\"Server connection failed: {str(e)}\", \"error\")\n    \n    def log(self, message, level=\"info\"):\n        \"\"\"Add message to log display\"\"\"\n        timestamp = datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")\n        \n        # Color coding\n        color = {\n            \"info\": \"#ecf0f1\",\n            \"success\": \"#27ae60\", \n            \"error\": \"#e74c3c\",\n            \"warning\": \"#f39c12\"\n        }.get(level, \"#ecf0f1\")\n        \n        self.log_text.config(state='normal')\n        self.log_text.insert('end', f\"[{timestamp}] {message}\\n\")\n        self.log_text.config(state='disabled')\n        self.log_text.see('end')\n        \n        # Update GUI\n        self.root.update_idletasks()\n    \n    def save_configuration(self):\n        \"\"\"Save current configuration to server\"\"\"\n        app_url = self.url_entry.get().strip()\n        app_name = self.name_entry.get().strip()\n        \n        if not app_url or not app_name:\n            messagebox.showerror(\"Error\", \"Please fill in both App URL and App Name\")\n            return\n        \n        self.log(\"💾 Saving configuration...\")\n        messagebox.showinfo(\"Success\", \"Configuration saved!\")\n    \n    def build_android_app(self):\n        \"\"\"Start the Android app build process\"\"\"\n        app_url = self.url_entry.get().strip()\n        app_name = self.name_entry.get().strip()\n        \n        if not app_url or not app_name:\n            messagebox.showerror(\"Error\", \"Please fill in both App URL and App Name\")\n            return\n        \n        # Disable build button during build\n        self.build_btn.config(state='disabled')\n        self.retry_btn.pack_forget()\n        self.progress['value'] = 0\n        \n        # Clear previous logs\n        self.log_text.config(state='normal')\n        self.log_text.delete(1.0, 'end')\n        self.log_text.config(state='disabled')\n        \n        self.log(\"🚀 Starting Android app build...\", \"info\")\n        self.log(f\"📱 App Name: {app_name}\")\n        self.log(f\"🌐 App URL: {app_url}\")\n        \n        # Start build in separate thread\n        threading.Thread(\n            target=self.request_build,\n            args=(app_url, app_name),\n            daemon=True\n        ).start()\n    \n    def request_build(self, app_url, app_name):\n        \"\"\"Request build from server\"\"\"\n        try:\n            # Send build request\n            self.log(\"📡 Sending build request to server...\")\n            \n            response = requests.post(\n                f\"{self.server_url}/api/build\",\n                json={\n                    \"app_url\": app_url,\n                    \"app_name\": app_name,\n                    \"client_id\": \"pos_client\"\n                },\n                timeout=30\n            )\n            \n            if response.status_code == 200:\n                build_data = response.json()\n                self.current_build_id = build_data['build_id']\n                \n                self.log(f\"✅ Build request accepted. Build ID: {self.current_build_id}\")\n                \n                # Start WebSocket connection for real-time logs\n                self.connect_websocket()\n                \n                # Start polling for status updates\n                self.poll_build_status()\n                \n            else:\n                self.log(f\"❌ Build request failed: {response.text}\", \"error\")\n                self.build_finished(False)\n                \n        except Exception as e:\n            self.log(f\"❌ Failed to start build: {str(e)}\", \"error\")\n            self.build_finished(False)\n    \n    def connect_websocket(self):\n        \"\"\"Connect to WebSocket for real-time logs\"\"\"\n        try:\n            ws_url = self.server_url.replace('http', 'ws')\n            ws_url = f\"{ws_url}/api/build/{self.current_build_id}/logs/ws\"\n            \n            def on_message(ws, message):\n                try:\n                    log_data = json.loads(message)\n                    timestamp = log_data.get('timestamp', '')\n                    level = log_data.get('level', 'info')\n                    msg = log_data.get('message', '')\n                    \n                    self.root.after(0, lambda: self.log(msg, level))\n                except:\n                    pass\n            \n            def on_error(ws, error):\n                self.root.after(0, lambda: self.log(f\"WebSocket error: {error}\", \"warning\"))\n            \n            def on_close(ws, close_status_code, close_msg):\n                self.root.after(0, lambda: self.log(\"Log stream disconnected\", \"info\"))\n            \n            self.ws = websocket.WebSocketApp(\n                ws_url,\n                on_message=on_message,\n                on_error=on_error,\n                on_close=on_close\n            )\n            \n            # Run WebSocket in separate thread\n            threading.Thread(\n                target=self.ws.run_forever,\n                daemon=True\n            ).start()\n            \n        except Exception as e:\n            self.log(f\"Failed to connect WebSocket: {str(e)}\", \"warning\")\n    \n    def poll_build_status(self):\n        \"\"\"Poll server for build status updates\"\"\"\n        def check_status():\n            try:\n                response = requests.get(\n                    f\"{self.server_url}/api/build/{self.current_build_id}/status\",\n                    timeout=10\n                )\n                \n                if response.status_code == 200:\n                    status_data = response.json()\n                    status = status_data.get('status')\n                    progress = status_data.get('progress', 0)\n                    \n                    # Update progress bar\n                    self.progress['value'] = progress\n                    \n                    if status == 'building':\n                        # Continue polling\n                        self.root.after(3000, check_status)\n                    elif status == 'success':\n                        self.log(\"🎉 Build completed successfully!\", \"success\")\n                        self.handle_build_success(status_data)\n                        self.build_finished(True)\n                    elif status == 'error':\n                        error_msg = status_data.get('message', 'Unknown error')\n                        self.log(f\"❌ Build failed: {error_msg}\", \"error\")\n                        self.build_finished(False)\n                    else:\n                        # Continue polling for pending status\n                        self.root.after(2000, check_status)\n                else:\n                    self.log(\"Failed to get build status\", \"warning\")\n                    self.root.after(5000, check_status)\n                    \n            except Exception as e:\n                self.log(f\"Status check failed: {str(e)}\", \"warning\")\n                self.root.after(5000, check_status)\n        \n        # Start status checking\n        self.root.after(1000, check_status)\n    \n    def handle_build_success(self, status_data):\n        \"\"\"Handle successful build completion\"\"\"\n        apk_url = status_data.get('apk_url')\n        \n        if apk_url:\n            self.log(f\"📦 APK Download URL: {apk_url}\")\n            \n            # Show download dialog\n            result = messagebox.askyesno(\n                \"Build Complete!\", \n                \"Your Android app has been built successfully!\\n\\n\" +\n                \"Would you like to open the download link?\"\n            )\n            \n            if result:\n                try:\n                    webbrowser.open(apk_url)\n                except:\n                    self.log(\"Failed to open browser. Please copy the URL manually.\", \"warning\")\n        else:\n            self.log(\"Build completed but download URL not available\", \"warning\")\n    \n    def build_finished(self, success):\n        \"\"\"Re-enable UI after build completion\"\"\"\n        self.build_btn.config(state='normal')\n        \n        if not success:\n            self.retry_btn.pack(side='left', padx=5, after=self.build_btn)\n        \n        if self.ws:\n            self.ws.close()\n            self.ws = None\n    \n    def retry_build(self):\n        \"\"\"Retry the last build\"\"\"\n        self.build_android_app()\n    \n    def show_settings(self):\n        \"\"\"Show server settings dialog\"\"\"\n        settings_window = tk.Toplevel(self.root)\n        settings_window.title(\"Server Settings\")\n        settings_window.geometry(\"400x200\")\n        settings_window.configure(bg='#ecf0f1')\n        \n        # Server URL setting\n        tk.Label(\n            settings_window,\n            text=\"Server URL:\",\n            font=('Arial', 10),\n            bg='#ecf0f1'\n        ).pack(pady=(20, 5))\n        \n        url_entry = tk.Entry(\n            settings_window,\n            font=('Arial', 10),\n            width=50\n        )\n        url_entry.pack(pady=5)\n        url_entry.insert(0, self.server_url)\n        \n        # Buttons\n        button_frame = tk.Frame(settings_window, bg='#ecf0f1')\n        button_frame.pack(pady=20)\n        \n        def save_settings():\n            self.server_url = url_entry.get().strip()\n            self.save_config()\n            self.check_server_connection()\n            settings_window.destroy()\n            messagebox.showinfo(\"Settings\", \"Server settings saved!\")\n        \n        tk.Button(\n            button_frame,\n            text=\"Save\",\n            command=save_settings,\n            bg='#27ae60',\n            fg='white',\n            padx=20\n        ).pack(side='left', padx=5)\n        \n        tk.Button(\n            button_frame,\n            text=\"Cancel\",\n            command=settings_window.destroy,\n            bg='#95a5a6',\n            fg='white',\n            padx=20\n        ).pack(side='left', padx=5)\n    \n    def run(self):\n        \"\"\"Start the application\"\"\"\n        self.root.protocol(\"WM_DELETE_WINDOW\", self.on_closing)\n        self.root.mainloop()\n    \n    def on_closing(self):\n        \"\"\"Handle application closing\"\"\"\n        if self.ws:\n            self.ws.close()\n        self.root.destroy()\n\ndef main():\n    \"\"\"Main entry point\"\"\"\n    try:\n        # Enable high DPI support on Windows\n        if sys.platform.startswith('win'):\n            import ctypes\n            ctypes.windll.shcore.SetProcessDpiAwareness(1)\n    except:\n        pass\n    \n    app = MobileAppBuilderClient()\n    app.run()\n\nif __name__ == \"__main__\":\n    main()