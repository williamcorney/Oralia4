
from PyQt6.QtCore import (
    Qt, QTimer, pyqtSignal)
from gui import gui
from PyQt6.QtGui import QPixmap, QFont

import random,copy

class logic (gui):
    green_signal = pyqtSignal(int)
    red_signal = pyqtSignal(int)
    note_off_signal = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.logic_variables()
        self.green_signal.connect(self.insert_green_note)
        self.red_signal.connect(self.insert_red_note)
        self.note_off_signal.connect(self.delete_notes)

        # we can access gui elements because we are inheriting from gui
        # what we cant do is access logic from gui


    def logic_variables(self):
        self.lastnote = 0
        self.previous_scale = None
        self.theorymode = None
        self.pressed_notes = []
        self.correct_answer = None
        self.correct_key = None


    def go_button_clicked(self):
        self.get_theory_items()

    def note_handler(self,mididata):

        if self.tab_widget.currentIndex() == 1:

            match self.theorymode:


                case "Notes":

                    if mididata.type == "note_on":

                        if mididata.note % 12 == self.required_notes:
                            self.green_signal.emit(mididata.note)
                            self.go_button_clicked()
                            self.score_increase()

                        else:
                            self.red_signal.emit(mididata.note)
                            self.reset_scale()

                case "Scales":

                    if mididata.type == "note_on":
                        if mididata.note == self.required_notes[0]:
                            self.required_notes.pop(0)
                            self.green_signal.emit(mididata.note)
                            if len(self.required_notes) == 0:
                                self.go_button_clicked()
                        else:

                            self.red_signal.emit(mididata.note)
                            self.reset_scale()
                case "Triads":

                    if mididata.type == "note_on":

                        if mididata.note in self.required_notes:
                            self.green_signal.emit(mididata.note)
                            self.pressed_notes.append(mididata.note)
                            if len(self.pressed_notes) >= 3:
                                self.go_button_clicked()


                        else:
                            self.red_signal.emit(mididata.note)

                case "Sevenths":

                    if mididata.type == "note_on":
                        if mididata.note in self.required_notes:
                            self.green_signal.emit(mididata.note)
                            self.pressed_notes.append(mididata.note)
                            if len(self.pressed_notes) >= 4:
                                self.go_button_clicked()
                        else:
                            self.red_signal.emit(mididata.note)

                case "Modes":

                    if mididata.type == "note_on":
                        if mididata.note == self.required_notes[0]:
                            self.green_signal.emit(mididata.note)
                            self.required_notes.pop(0)
                            if len(self.required_notes) == 0:
                                self.go_button_clicked()
                        else:
                            self.red_signal.emit(mididata.note)
                            self.reset_scale()

                case _:
                  if mididata.type == "note_on":
                      self.red_signal.emit(mididata.note)


            if mididata.type == "note_off":
                self.note_off_signal.emit(mididata.note)
                self.pressed_notes.remove(mididata.note)
    def reset_scale(self):
        if hasattr(self, 'deepnotes') and self.deepnotes:
            self.required_notes = copy.deepcopy(self.deepnotes)
    def get_theory_items(self):

        if hasattr(self, 'theorymode'):

            match self.theorymode:

                case "Notes":

                    self.get_random_values()

                    self.required_notes = self.int

                    if self.type == "Flats":
                        self.key_label.setText(self.Theory["Enharmonic"][self.required_notes])
                    else:
                        self.key_label.setText(self.Theory["Chromatic"][self.required_notes])

                case "Scales":

                    self.get_random_values()
                    while self.current_scale == self.previous_scale:
                        self.get_random_values()
                    self.required_notes = (self.midi_note_scale_generator((self.Theory["Scales"][self.type][self.int]),
                                                                          octaves=int(self.Settings['User']['Octaves']),
                                                                          base_note=60))
                    self.deepnotes = copy.deepcopy(self.required_notes)
                    self.previous_scale = self.current_scale

                    self.key_label.setText(self.current_scale)

                    self.fingering_label.setText(str(self.Theory['Fingering'][self.int][self.current_scale]["Right"]))

                case "Triads":
                    #self.scaletypesselected = [item.text() for item in self.listselector2.selectedItems()]
                    if not self.theory2list:
                        print("You need to select a scale type")
                        return
                    if not self.theory3list:
                        print("You need to select an inversion")
                        return

                    self.get_random_values()
                    while self.current_scale == self.previous_scale:
                        self.get_random_values()
                    self.required_notes = self.midi_note_scale_generator(
                        self.Theory["Triads"][self.current_scale][self.inv],
                        octaves=1,
                        base_note=60, include_descending=False
                    )
                    self.current_scale = f"{self.current_scale} {self.inv}"
                    self.deepnotes = copy.deepcopy(self.required_notes)
                    self.previous_scale = self.current_scale
                    self.key_label.setText(self.current_scale)

                case "Sevenths":

                    if not self.theory2list:
                        print("You need to select a scale type")
                        return

                    if not self.theory3list:
                        print("You need to select an inversion")
                        return

                    self.get_random_values()
                    while self.current_scale == self.previous_scale:
                        self.get_random_values()
                    self.required_notes = self.midi_note_scale_generator(
                        self.Theory["Sevenths"][self.current_scale][self.inv],
                        octaves=1,
                        base_note=60, include_descending=False
                    )
                    self.current_scale = f"{self.current_scale} {self.inv}"
                    self.deepnotes = copy.deepcopy(self.required_notes)
                    self.previous_scale = self.current_scale
                    self.key_label.setText(self.current_scale)

                case "Modes":
                    if not self.theory_subtype_list:
                        print("You need to select a scale type")
                        return

                    self.get_random_values()
                    while self.current_scale == self.previous_scale:
                        self.get_random_values()
                    self.required_notes = (self.midi_note_scale_generator((self.Theory["Modes"][self.letter][self.type]),
                                                                          octaves=1,
                                                                          base_note=60))
                    self.deepnotes = copy.deepcopy(self.required_notes)
                    self.previous_scale = self.current_scale
                    self.key_label.setText(self.current_scale)

        else:
            pass

    def midi_note_scale_generator(self, notes, octaves=1, base_note=60, repeat_middle=False, include_descending=True):
        adjusted_notes = [note + base_note for note in notes]
        extended_notes = adjusted_notes[:]

        for octave in range(1, octaves):
            extended_notes.extend([note + 12 * octave for note in adjusted_notes[1:]])

        if include_descending:
            if repeat_middle:
                reversed_notes = extended_notes[::-1]
            else:
                reversed_notes = extended_notes[:-1][::-1]
            extended_notes.extend(reversed_notes)

        return extended_notes

    def get_random_values(self):



        match self.theorymode:
            case "Notes":

                self.type = random.choice(self.theory2list)
                self.notes = self.Theory["Notes"][self.type]
                self.int = (random.choice(self.notes))
                while self.lastnote == self.int:
                    self.int = (random.choice(self.notes))
                self.letter = (self.Theory["Chromatic"][self.int])
                self.lastnote = self.int

            case "Scales":
                self.int = random.choice([0, 2, 4, 5, 7, 9, 11])
                # self.int = random.randint(0, 11)
                self.letter = self.Theory["Enharmonic"][self.int]
                self.type = random.choice(self.theory2list)
                self.current_scale = f"{self.letter} {self.type}"

            case "Triads":

                self.int = random.randint(0, 11)
                self.letter = self.Theory["Enharmonic"][self.int]
                self.type = random.choice(self.theory2list)
                self.current_scale = f"{self.letter} {self.type}"
                self.inv = random.choice(self.theory3list)

            case "Sevenths":

                self.int = random.randint(0, 11)
                self.letter = self.Theory["Enharmonic"][self.int]
                self.type = random.choice(self.theory2list)
                self.current_scale = f"{self.letter} {self.type}"
                self.inv = random.choice(self.theory3list)

            case "Modes":

                self.int = random.randint(0, 11)
                self.letter = self.Theory["Enharmonic"][self.int]
                self.type = random.choice(self.theory2list)
                self.current_scale = f"{self.letter} {self.type}"
            case "Keys":

                # work in progress

                self.type = random.choice(self.theory_subtype_list)
                self.int = random.randint(0, 11)
                # print (self.Theory["Theory"][self.type])
                # self.letter = self.Theory["Theory"][self.type][self.int]
                key_value_pair = list(self.Theory["Theory"][self.type].items())[self.int]
                print(key_value_pair)


