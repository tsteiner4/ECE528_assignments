# Tristan Steiner Assignment 2 - Name and Appearance
import matplotlib.pylab as plt
import random
from PIL import Image
import urllib.request as urllib

import PySimpleGUI as simpleGUI

from canvasapi import Canvas
import re


def parse_entry(entry):
    valid = False
    dic = {}
    # if '<' in str(entry):
    temp = str(entry)

    entry = re.sub('<.*?>', '', temp)
    sep_words = str(entry).split(',')
    if len(sep_words) == 3 and len(sep_words[0].split(' ')) < 4:
        if 'http' in sep_words[2]:
            if 'jpg' in sep_words[2]:
                sep_words[2] = sep_words[2][sep_words[2].rfind('http'):sep_words[2].lower().rfind('jpg') + 3]
            else:
                sep_words[2] = sep_words[2][sep_words[2].rfind('http'):sep_words[2].lower().rfind('png') + 3]
        valid = True
        dic = {'firstName': sep_words[0].strip(), 'lastName': sep_words[1].strip(), 'imageURL': sep_words[2].strip()}
    return valid, dic

"""
This function uses the Canvas API (thanks to Daniel for the recommendation) to read from the discussion list and get the
list of student names and links. It also attempts to open the URLs and removes any bad references. Some people replied 
to other comments with their response, so we have to search down an extra level.
"""
def get_list_from_canvas():
    # you will need to create a txt file with your token for canvas, I will not release my key to the internet.
    private_token = open('Assignment2/private_canvas_key.txt').readline()
    canvas = Canvas("https://canvas.umd.umich.edu/", private_token)
    entries = canvas.get_course(518091).get_discussion_topic(1913607).get_topic_entries()

    list_out = []

    for e in entries:
        # get the replies for the entry - index may not exist if no replies
        replies = e.get_replies()
        for r in replies:
            valid, dic = parse_entry(r)
            if valid:
                list_out.append(dic)

        valid, dic = parse_entry(e)
        if valid:
            list_out.append(dic)

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
    sorted_list = sorted(ls, key=lambda name: name['lastName'])
    for i, m in enumerate(sorted_list, 1):
        #img = plt.imread(m['imageURL'], m['imageURL'][-3:])
        # https://stackoverflow.com/questions/12020657/how-do-i-open-an-image-from-the-internet-in-pil/12020860
        # can also use this for opening the image
        img = Image.open(urllib.urlopen(m['imageURL']))

        axs = plt.subplot(len(master_list) // 6 + 1, 6, i)
        axs.set_xlabel(f"{m['firstName']} {m['lastName']}")
        axs.axes.xaxis.set_ticks([])
        axs.axes.yaxis.set_ticks([])
        plt.tight_layout()
        plt.imshow(img)

    return


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
    return


# Main
if __name__ == '__main__':
    #master_list = get_image_list() replaced by canvas API
    master_list = get_list_from_canvas()
    sort_and_plot(master_list)

    simple_matching_game(master_list)

    plt.interactive(False)
    plt.show()





