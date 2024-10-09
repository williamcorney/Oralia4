import sys,mido,pickle,random,copy
from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QWidget,
    QMainWindow, QPushButton, QTabWidget, QLabel, QListWidget,
    QGraphicsView,QGraphicsScene,QGraphicsPixmapItem,
    QAbstractItemView,QButtonGroup,QRadioButton)
from PyQt6.QtGui import (
    QPixmap, QFont)

from PyQt6.QtCore import (
    Qt, QTimer, pyqtSignal)
class gui(QMainWindow):



    def __init__(self):
        super().__init__()
        self.setup_variables()
        self.gui_tabs()

        self.setWindowTitle('Piano Training')

    def setup_variables(self):
        self.tabs = {}
        self.widgets = {}
        self.pixmap_item = {}
        with open('theory.pkl', 'rb') as file: self.Theory = pickle.load(file)
        with open('settings.pkl', 'rb') as file: self.Settings = pickle.load(file)

    def insert_green_note(self, note):
        if self.tab_widget.currentIndex() == 1:
            self.xcord = self.Theory["NoteCoordinates"][note % 12] + ((note // 12) - 4) * 239
            self.pixmap_item[note] = QGraphicsPixmapItem(
                QPixmap("./Images/key_" + "green" + self.Theory["NoteFilenames"][note % 12]))
            self.pixmap_item[note].setPos(self.xcord, 0)
            # Remove item from its current scene before adding it to the new one
            current_scene = self.pixmap_item[note].scene()
            if current_scene:
                current_scene.removeItem(self.pixmap_item[note])
            self.tabs["Practical"].Scene.addItem(self.pixmap_item[note])

    def insert_red_note(self, note):
        if self.tab_widget.currentIndex() == 1:
            self.xcord = self.Theory["NoteCoordinates"][note % 12] + ((note // 12) - 4) * 239
            self.pixmap_item[note] = QGraphicsPixmapItem(
                QPixmap("./Images/key_" + "red" + self.Theory["NoteFilenames"][note % 12]))
            self.pixmap_item[note].setPos(self.xcord, 0)
            # Remove item from its current scene before adding it to the new one
            current_scene = self.pixmap_item[note].scene()
            if current_scene:
                current_scene.removeItem(self.pixmap_item[note])
            self.tabs["Practical"].Scene.addItem(self.pixmap_item[note])

    def delete_notes(self, note):
        if self.tab_widget.currentIndex() == 1:
            try:
                # Ensure item is removed from its scene
                if self.pixmap_item[note].scene():
                    self.pixmap_item[note].scene().removeItem(self.pixmap_item[note])
            except:
                pass

    def reset_scene(self):
        self.tabs["Practical"].Scene.clear()
        self.tabs["Practical"].BackgroundPixmap = QPixmap(
            "/Users/williamcorney/PycharmProjects/Oralia2/Images/keys.png")
        self.tabs["Practical"].BackgroundItem = QGraphicsPixmapItem(self.tabs["Practical"].BackgroundPixmap)
        self.tabs["Practical"].Scene.addItem(self.tabs["Practical"].BackgroundItem)

    def gui_tabs(self):
        #Create the QTabwidget
        self.tab_widget = QTabWidget()

        self.tabs["Home"] = QWidget()
        self.tabs["Practical"] = QWidget()
        self.tabs["Theory"] = QWidget()
        self.tabs["Settings"] = QWidget()
        #Add tabs to to tab_widget
        self.tab_widget.addTab(self.tabs["Home"], "Home")
        self.tab_widget.addTab(self.tabs["Practical"], "Practical")
        self.tab_widget.addTab(self.tabs["Theory"], "Theory")
        self.tab_widget.addTab(self.tabs["Settings"], "Settings")
        self.setCentralWidget(self.tab_widget)

        self.tabs["Home"].setLayout(QVBoxLayout())
        self.tabs["Practical"].setLayout(QVBoxLayout())
        self.tabs["Theory"].setLayout(QVBoxLayout())
        self.tabs["Settings"].setLayout(QVBoxLayout())


        self.tab_widget.currentChanged.connect(self.reset_scene)

        self.tabs["Practical"].horizontal = QHBoxLayout()

        self.widgets['theory1'] = QListWidget()
        self.widgets['theory2'] = QListWidget()
        self.widgets['theory3'] = QListWidget()

        self.tabs["Practical"].layout().addLayout(self.tabs["Practical"].horizontal)

        self.tabs["Practical"].horizontal.addWidget(self.widgets['theory1'])
        self.tabs["Practical"].horizontal.addWidget(self.widgets['theory2'])
        self.tabs["Practical"].horizontal.addWidget(self.widgets['theory3'])


        self.tabs["Practical"].Scene = QGraphicsScene()
        self.tabs["Practical"].BackgroundPixmap = QPixmap("/Users/williamcorney/PycharmProjects/Oralia2/Images/keys.png")
        self.tabs["Practical"].BackgroundItem = QGraphicsPixmapItem(self.tabs["Practical"].BackgroundPixmap)
        self.tabs["Practical"].Scene.addItem(self.tabs["Practical"].BackgroundItem)
        self.tabs["Practical"].View = QGraphicsView(self.tabs["Practical"].Scene)
        self.tabs["Practical"].View.setFixedSize( self.tabs["Practical"].BackgroundPixmap.size())
        self.tabs["Practical"].View.setSceneRect(0, 0, self.tabs["Practical"].BackgroundPixmap.width(),self.tabs["Practical"].BackgroundPixmap.height())
        self.tabs["Practical"].View.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tabs["Practical"].View.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tabs["Practical"].layout().addWidget(self.tabs["Practical"].View)
        self.tabs["Practical"].horizontal.vertical = QVBoxLayout()
        self.tabs["Practical"].horizontal.addLayout(self.tabs["Practical"].horizontal.vertical, 2)
        self.widgets['key_label'] = QLabel("C Major")
        self.widgets['key_label'].setFont(QFont("Arial", 32))
        self.widgets['inversion_label'] = QLabel("B")
        self.widgets['fingering_label'] = QLabel("1,2,3,1,2,3,4,5")
        self.widgets['score_label'] = QLabel("Score :")
        self.widgets['score_value'] = QLabel("0")
        self.widgets['go_button'] = QPushButton("Go")
        self.tabs["Practical"].horizontal.vertical.addWidget(self.widgets['key_label'])
        self.tabs["Practical"].horizontal.vertical.addWidget(self.widgets['inversion_label'])
        self.tabs["Practical"].horizontal.vertical.addWidget(self.widgets['fingering_label'])
        self.tabs["Practical"].horizontal.vertical.addWidget(self.widgets['score_label'])
        self.tabs["Practical"].horizontal.vertical.addWidget(self.widgets['score_value'])
        self.tabs["Practical"].horizontal.vertical.addWidget(self.widgets['go_button'])
        self.widgets['theory1'].addItems(["Notes", "Scales", "Triads", "Sevenths", "Modes"])
        self.widgets['theory1'].clicked.connect(self.theory1_clicked)
        self.widgets['theory2'].clicked.connect(self.theory2_clicked)
        self.widgets['theory3'].clicked.connect(self.theory3_clicked)
        self.widgets['theory2'].setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.widgets['theory3'].setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        self.widgets['theory4'] = QListWidget()
        self.widgets['theory4'].clicked.connect(self.set_question_bank)
        self.widgets['theory5'] = QListWidget()
        self.tabs["Theory"].horizontal1 = QHBoxLayout()
        self.tabs["Theory"].horizontal2 = QHBoxLayout()
        self.tabs["Theory"].horizontal1.addWidget(self.widgets['theory4'])
        self.tabs["Theory"].horizontal1.addWidget(self.widgets['theory5'])
        self.widgets['theory4'].addItems(['Note Identification', "Key Identification", "Key Signature Identification"])
        self.tabs["Theory"].layout().addLayout(self.tabs["Theory"].horizontal1)
        self.tabs["Theory"].layout().addLayout(self.tabs["Theory"].horizontal2)

        self.widgets['radiobuttons'] = QButtonGroup()
        self.widgets['A'] = QRadioButton("A")
        self.widgets['B']= QRadioButton("B")
        self.widgets['C'] = QRadioButton("C")
        self.widgets['D'] = QRadioButton("D")
        self.radio_buttons = [self.widgets['A'],self.widgets['B'],self.widgets['C'],self.widgets['D']]

        for radio_button in self.radio_buttons:
            self.widgets['radiobuttons'].addButton(radio_button)
            radio_button.clicked.connect(self.check_answer)
        self.widgets['question_label'] = QLabel("ABC")
        self.widgets['question_image'] = QLabel("Image")
        self.widgets['key_label'] = QLabel("C Major")
        self.widgets['key_label'].setFont(QFont("Arial", 32))
        self.widgets['inversion_label'] = QLabel("B")
        self.widgets['fingering_label'] = QLabel("1,2,3,1,2,3,4,5")
        self.widgets['score_label'] = QLabel("Score :")
        self.widgets['score_value'] = QLabel("0")
        self.widgets['go_button'] = QPushButton("Go")
        self.tabs["Theory"].horizontal1.vertical = QVBoxLayout()
        self.tabs["Theory"].horizontal1.addLayout(self.tabs["Theory"].horizontal1.vertical)
        self.tabs["Theory"].horizontal2.vertical = QVBoxLayout()
        self.tabs["Theory"].horizontal2.addLayout(self.tabs["Theory"].horizontal2.vertical)

        self.tabs["Theory"].horizontal2.addWidget(self.widgets['question_label'])
        self.tabs["Theory"].horizontal1.vertical.addWidget(self.widgets['key_label'])
        self.tabs["Theory"].horizontal1.vertical.addWidget(self.widgets['inversion_label'])
        self.tabs["Theory"].horizontal1.vertical.addWidget(self.widgets['fingering_label'])
        self.tabs["Theory"].horizontal1.vertical.addWidget(self.widgets['score_label'])
        self.tabs["Theory"].horizontal1.vertical.addWidget(self.widgets['score_value'])
        self.tabs["Theory"].horizontal1.vertical.addWidget(self.widgets['go_button'])
        self.widgets["go_button"].clicked.connect(self.generate_question)

        self.tabs["Theory"].horizontal2.layout().addWidget(self.widgets['question_label'])



        self.tabs["Theory"].layout().addWidget(self.widgets['A'])
        self.tabs["Theory"].layout().addWidget(self.widgets['B'])
        self.tabs["Theory"].layout().addWidget(self.widgets['C'])
        self.tabs["Theory"].layout().addWidget(self.widgets['D'])




    def theory1_clicked(self):
        self.widgets['theory2'].clear()
        self.widgets['theory3'].clear()
        self.theorymode = (self.widgets['theory1'].selectedItems()[0].text())

        match self.theorymode:
            case "Notes":
                self.theory2.addItems(["Naturals", "Sharps", "Flats"])
            case "Scales":
                self.theory2.addItems(["Major", "Minor", "Melodic Minor", "Harmonic Minor"])
            case "Triads":
                self.theory2.addItems(["Major", "Minor"])
            case "Sevenths":
                self.theory2.addItems(["Maj7", "Min7", "7", "Dim7", "m7f5"])
            case "Modes":
                self.theory2.addItems(
                    ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"])

    def theory2_clicked(self):

        match self.theorymode:
            case "Notes":
                self.theory2list = ([item.text() for item in self.theory2.selectedItems()])

            case "Scales":
                self.theory2list = ([item.text() for item in self.theory2.selectedItems()])

            case "Triads":
                self.theory2list = ([item.text() for item in self.theory2.selectedItems()])
                self.theory3.clear()
                self.theory3.addItems(["Root", "First", "Second"])
            case "Sevenths":
                self.theory2list = ([item.text() for item in self.theory2.selectedItems()])
                self.theory3.clear()
                self.theory3.addItems(["Root", "First", "Second", "Third"])

    def theory3_clicked(self):

        match self.theorymode:
            case "Notes":
                self.theory3list = ([item.text() for item in self.theory3.selectedItems()])

            case "Scales":
                self.theory3list = ([item.text() for item in self.theory3.selectedItems()])
            case "Triads":
                self.theory3list = ([item.text() for item in self.theory3.selectedItems()])
            case "Sevenths":
                self.theory3list = ([item.text() for item in self.theory3.selectedItems()])

    def set_question_bank(self):

        if self.widgets['theory4'].currentItem().text() == "Key Identification":
            self.questions = self.Theory['Theory']['Major']

    def generate_question(self, questions, image_flag=False):
        if hasattr(self, 'questions'):
            # Select a random key and its accidentals as the correct answer
            self.correct_key = random.choice(list(self.questions.keys()))
            self.correct_answer = self.questions[self.correct_key]

            if image_flag:
                # Set the question image
                pixmap_path = f"./images/{self.correct_key}.png"  # Adjust extension as needed
                self.widgets['question_image'].setPixmap(QPixmap(pixmap_path))

            # Select three other keys as distractors, ensuring they're unique
            other_keys = random.sample([k for k in self.questions.keys() if k != self.correct_key], 3)

            # Combine the correct answer with the distractors and shuffle
            options = [(self.correct_key, self.correct_answer)] + [(k, self.questions[k]) for k in other_keys]
            random.shuffle(options)

            # Update the UI with the new question and options
            self.widgets['question_label'].setText(f"{self.correct_key} Major")
            self.widgets['question_label'].setFont(QFont('Arial', 36))

            for i, (key, value) in enumerate(options):
                answer = ", ".join(value) if value else "None"
                self.radio_buttons[i].setText(answer)

            # Clear any previous selection
            self.widgets['radiobuttons'].setExclusive(False)
            for radio_button in self.radio_buttons:
                radio_button.setChecked(False)
            self.widgets['radiobuttons'].setExclusive(True)
        else:
            print("You haven't selected a valid bank of questions.")

    def check_answer(self):
        selected_button = self.widgets['radiobuttons'].checkedButton()
        if not selected_button:
            print("No answer selected!")  # Replace with any other feedback mechanism
            return

        selected_value = selected_button.text()
        correct_value = ", ".join(self.correct_answer) if self.correct_answer else "None"

        if selected_value == correct_value:
            self.generate_question(self.questions)  # Automatically proceed to next question if correct
            print('Correct !!!!')
        else:
            print("Incorrect! Try again.")  # Replace with any other feedback mechanism

    def on_radio_button_clicked(self):
        # Handle radio button clicked event
        selected_button = self.widgets['radiobuttons'].checkedButton()
        if selected_button:
            print(f"Selected option: {selected_button.text()}")
