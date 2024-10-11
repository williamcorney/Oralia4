import sys
import sqlite3
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap,QFont
from PyQt6.QtCore import QSize, QTimer


# Database lookup function
def database_lookup(query):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(query)
    response = cursor.fetchall()
    conn.close()
    return response


# Function to generate quiz
def generate_quiz(last_correct_answer=None):
    query = "SELECT note_file_name, note_display_name, note_clef FROM notes WHERE note_clef = 'Treble'"
    rows = database_lookup(query)

    # Filter out the last correct answer to avoid repeating it
    if last_correct_answer:
        rows = [row for row in rows if row[0] != last_correct_answer]

    correct_row = random.choice(rows)
    correct_answer = {
        "answer_image": correct_row[0],
        "note_display_name": correct_row[1]
    }

    print(f"Correct Answer: {correct_row[0]}")  # Print the correct answer file name for debugging

    remaining_rows = [row for row in rows if row[1] != correct_row[1]]
    wrong_rows = random.sample(remaining_rows, 3)
    wrong_answers = {
        "wrong_answer_1": {
            "answer_image": wrong_rows[0][0],
            "note_display_name": wrong_rows[0][1]
        },
        "wrong_answer_2": {
            "answer_image": wrong_rows[1][0],
            "note_display_name": wrong_rows[1][1]
        },
        "wrong_answer_3": {
            "answer_image": wrong_rows[2][0],
            "note_display_name": wrong_rows[2][1]
        }
    }

    for key, answer in wrong_answers.items():
        print(f"Wrong Answer: {answer['answer_image']}")  # Print the wrong answer file names for debugging

    return {"correct_answer": correct_answer, "wrong_answers": wrong_answers}


class QuizWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note Identification Quiz")
        self.setGeometry(100, 100, 800, 600)

        self.last_correct_answer = None
        self.score = 0

        self.quiz_frame = QWidget(self)
        self.setCentralWidget(self.quiz_frame)

        self.layout = QVBoxLayout(self.quiz_frame)

        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        self.result_label = QLabel(self)
        self.layout.addWidget(self.result_label)

        self.score_label = QLabel(f"Score: {self.score}", self)
        self.score_label.setFont(QFont("Arial",48))
        self.layout.addWidget(self.score_label)

        self.option_buttons = []
        for _ in range(4):
            button = QPushButton(self)
            button.setFixedHeight(50)
            button.setFixedWidth(200)
            button.setStyleSheet("font-size: 18px;")
            self.layout.addWidget(button)
            self.option_buttons.append(button)

        self.load_quiz()

    def load_quiz(self):
        quiz = generate_quiz(self.last_correct_answer)
        image_path = "/Users/williamcorney/PycharmProjects/Oralia4/Images/Notes/Treble/" + quiz['correct_answer'][
            'answer_image']

        # Load and set the image
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(QSize(400, 300)))

        # Clear the result label
        self.result_label.clear()

        options = [quiz['correct_answer']['note_display_name']]
        options.extend([quiz['wrong_answers'][key]['note_display_name'] for key in quiz['wrong_answers']])
        random.shuffle(options)

        for i, option in enumerate(options):
            self.option_buttons[i].setText(option)
            # Disconnect any existing signal
            try:
                self.option_buttons[i].clicked.disconnect()
            except TypeError:
                pass
            # Connect the new signal
            self.option_buttons[i].clicked.connect(
                lambda checked, opt=option: self.check_answer(opt, quiz['correct_answer']['note_display_name']))

        # Remember the correct answer to avoid repeating it next time
        self.last_correct_answer = quiz['correct_answer']['answer_image']

    def check_answer(self, selected, correct):
        if selected == correct:
            result_image = "correct.png"
            self.score += 1
        else:
            result_image = "incorrect.png"
            self.score -= 3

        # Update the score label
        self.score_label.setText(f"Score: {self.score}")

        # Display the result image
        result_image_path = "/Users/williamcorney/PycharmProjects/Oralia4/Images/Notes/Treble/" + result_image
        result_pixmap = QPixmap(result_image_path)
        self.result_label.setPixmap(result_pixmap.scaled(QSize(200, 50)))

        # Wait for 2 seconds before loading the next quiz
        QTimer.singleShot(2000, self.load_quiz)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizWindow()
    window.show()
    sys.exit(app.exec())
