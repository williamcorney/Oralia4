import sys,mido
from PyQt6.QtWidgets import QApplication
from logic import logic


class Oralia(logic):
    def __init__(self):
        super().__init__()
        pass

app = QApplication([])
window = Oralia()
window.show()

with mido.open_input(callback=window.note_handler) as inport: app.exec()