# Tristan Steiner Assignment 2 - Name and Appearance
import base64
"""
import matplotlib.pylab as plt
import numpy as np
from PIL import Image
import urllib.request as urllib
import math
import tkinter
import PySimpleGUI as simpleGUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from canvasapi import Canvas

matplotlib.use("TKAgg")

import sys
import random
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget)
from PySide2.QtCore import Slot, Qt


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.button = QPushButton("Next Try")
        self.text = QLabel("Welcome!")
        self.text.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # Connecting the signal
        self.button.clicked.connect(self.magic)

    @Slot()
    def magic(self):
        list_out = get_image_list()
        rand = random.choice(list_out)
        self.text.setText(rand['firstName'] + ' ' + rand['lastName'])


def get_list_from_canvas():
    private_token = open('private_canvas_key.txt').readline()
    canvas = Canvas("https://canvas.umd.umich.edu/", private_token)
    entries = canvas.get_course(518091).get_discussion_topic(1913607).get_topic_entries()
    list_out = []

    for e in entries:
        sep_words = str(e).split(',')
        if len(sep_words) == 3:
            sep_words[0] = sep_words[0][sep_words[0].rfind('>')+1:]
            if 'http' in sep_words[2]:
                if 'jpg' in sep_words[2]:
                    sep_words[2] = sep_words[2][sep_words[2].rfind('http'):sep_words[2].lower().rfind('jpg')+3]
                else:
                    sep_words[2] = sep_words[2][sep_words[2].rfind('http'):sep_words[2].lower().rfind('png')+3]
            list_out.append({'firstName': sep_words[0].strip(), 'lastName': sep_words[1].strip(), 'imageURL': sep_words[2].strip()})

    for i, m in enumerate(list_out, 1):
        try:
            urllib.urlopen(m['imageURL'])
        except:
            print(f"{m['firstName']} does not have a valid link")
            list_out.remove(m)
    return list_out


def get_image_list():
    list_out = []
    f = open('students_csv.txt')
    line_no = 0
    for line in f:
        sep_words = line.split(',')
        if len(sep_words) == 3:
            list_out.append({'firstName': sep_words[0].strip(), 'lastName': sep_words[1].strip(), 'imageURL': sep_words[2].strip()})
        else:
            print(f"Line {line_no} does not contain a correctly formatted string")
        line_no += 1
    f.close()
    return list_out


def sort_and_plot(ls):
    sorted_list = sorted(ls, key=lambda name: name['firstName'])
    for i, m in enumerate(sorted_list, 1):
        # plt.imread doesn't work with jpg files
        # img = plt.imread(m['imageURL'])
        # https://stackoverflow.com/questions/12020657/how-do-i-open-an-image-from-the-internet-in-pil/12020860
        img = Image.open(urllib.urlopen(m['imageURL']))

        axs = plt.subplot(len(master_list) // 5 + 1, 5, i)
        axs.set_xlabel(f"{m['firstName']} {m['lastName']}")
        axs.axes.xaxis.set_ticks([])
        axs.axes.yaxis.set_ticks([])
        plt.imshow(img)

    return


def matching_game():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())


#Referenced https://realpython.com/pysimplegui-python/#creating-a-pysimplegui-image-viewer
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


# Referenced https://realpython.com/pysimplegui-python/#creating-basic-ui-elements-in-pysimplegui for GUI
def simple_matching_game(in_list):
    end_game = False
    total = 0
    corr = 0
    while ~end_game:

        r = random.sample(in_list, 3)
        correct_name = r[0]['firstName'] + ' ' + r[0]['lastName']
        img = Image.open(urllib.urlopen(r[0]['imageURL']))
        fig = plt.figure(2)
        axs = plt.gca()
        axs.xaxis.set_ticks([])
        axs.yaxis.set_ticks([])
        plt.imshow(img)
        plt.interactive(True)
        plt.show()

        random.shuffle(r)
        choice1 = r[0]['firstName'] + ' ' + r[0]['lastName']
        choice2 = r[1]['firstName'] + ' ' + r[1]['lastName']
        choice3 = r[2]['firstName'] + ' ' + r[2]['lastName']

        # image_column = [[simpleGUI.Canvas(key="-CANVAS-")]]
        # list_column = [[simpleGUI.Text('Select one->'), simpleGUI.Listbox([choice1, choice2, choice3],
        #                                                                   size=(50, 3), key='LB')],
        #                [simpleGUI.Button('OK'), simpleGUI.Button('Cancel')]]
        # layout = [
        #     [
        #         simpleGUI.Column(image_column),
        #         simpleGUI.Column(list_column)
        #     ]
        # ]
        # fig2 = plt.figure(figsize=(5, 4), dpi=100)
        # t = np.arange(0, 3, .01)
        # fig2.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
        #
        # window = simpleGUI.Window("Image", layout)
        #
        # draw_figure(window["-CANVAS-"].TKCanvas, fig2)
        if total <= 0:
            event, values = simpleGUI.Window(f'Choose who is in the picture (Press Cancel to Stop)',
                                             [[simpleGUI.Text('Select one->'),
                                               simpleGUI.Listbox([choice1, choice2, choice3],
                                                                 size=(50, 3), key='LB')],
                                              [simpleGUI.Button('OK'), simpleGUI.Button('Cancel')]]).read(close=True)
        else:
            event, values = simpleGUI.Window(
                f'Choose who is in the picture Current Score: {round(corr / total * 100, 3)}',
                [[simpleGUI.Text('Select one->'),
                  simpleGUI.Listbox([choice1, choice2, choice3],
                                    size=(50, 3), key='LB')],
                 [simpleGUI.Button('OK'), simpleGUI.Button('Cancel')]]).read(close=True)

        if event == 'OK':
            selected_choice = values["LB"][0]
            if selected_choice == correct_name:
                simpleGUI.popup(f'You are correct!')
                corr += 1
            else:
                simpleGUI.popup(f'You are wrong!')
        if event == simpleGUI.WIN_CLOSED or event == 'Cancel':
            plt.close(2)
            break

        total += 1
    # while True:
    #     event, values = window.read()
    #     if event == "Exit" or event == simpleGUI.WIN_CLOSED:
    #         break

    return


# Main
if __name__ == '__main__':
    #master_list = get_image_list()
    master_list = get_list_from_canvas()
    sort_and_plot(master_list)

    simple_matching_game(master_list)
    #get_list_from_canvas()

    plt.interactive(False)
    plt.show()


"""


