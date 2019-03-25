import tkinter as tk
from tkinter import filedialog

# otvori file dialog a vrati meno suboru
def openFileDialog():
    root = tk.Tk()
    root.withdraw() # skryje prazdne GUI okno, resp. sa nevykresli

    file_path = filedialog.askopenfilename() # samoteny dialog
    root.destroy() # potrebne, inak zamrzne okno, treba aplikaciu zakillovat
    return file_path
