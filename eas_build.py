import os
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

PROJECT_DIR= r"C:\xampp\htdocs\WebAppWrapperExpo"
EAS_CLI = r"C:\Users\LENOVO\AppData\Roaming\npm\eas.cmd"


def run_build():
    if "EXPO_TOKEN" not in os.environ:
        messagebox.showerror(
            "Missing Token",
            "EXPO_TOKEN is not set in Environment Variables"
        )
        return

    build_button.config(state=tk.DISABLED)
    log_area.delete(1.0, tk.END)
    log("Starting EAS build...\n")

    os.chdir(PROJECT_DIR)

    command = [
        EAS_CLI,
        "build",
        "--platform", "android",
        "--profile", "production",
        "--non-interactive"
    ]

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            log(line)

        process.wait()

        if process.returncode == 0:
            log("\n✅ Build completed successfully!\n")
            messagebox.showinfo("Success", "Build completed successfully!")
        else:
            log(f"\n❌ Build failed (code {process.returncode})\n")
            messagebox.showerror("Build Failed", "Check logs for details.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    build_button.config(state=tk.NORMAL)


def start_build():
    threading.Thread(target=run_build, daemon=True).start()


def log(message):
    log_area.insert(tk.END, message)
    log_area.see(tk.END)


root = tk.Tk()
root.title("Mobile App Builder/Installer")
root.geometry("820x500")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Mobile App Builder/Installer",
    font=("Segoe UI", 16, "bold")
)
title.pack(pady=10)

build_button = tk.Button(
    root,
    text="🚀 Build Android App",
    font=("Segoe UI", 12),
    width=25,
    height=2,
    command=start_build
)
build_button.pack(pady=10)

log_area = scrolledtext.ScrolledText(
    root,
    width=100,
    height=20,
    font=("Consolas", 10)
)
log_area.pack(padx=10, pady=10)

root.mainloop()
