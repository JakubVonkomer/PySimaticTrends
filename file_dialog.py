import tkinter as tk
from tkinter import filedialog

# otvori file dialog a vrati meno suboru
def openFileDialog():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    return file_path
