import json
import datetime
import os
import config

"""
    Exit application
"""
def quit_all():
    exit()


def save_result_to_file(result, filename):
    try:
        if not os.path.isdir(config.base_output_path):
            os.mkdir(config.base_output_path)
        unq_filename = config.base_output_path + filename + "_" + datetime.datetime.now().strftime("%m_%d-%H_%M_%S") + ".txt"
        f = open(unq_filename, "a")
        if type(result) is list:
            for el in result:
                f.write(json.dumps(el, indent=4))
                f.write('\n')
        else:
            f.write(result)
        f.close()
    except:
        print("Something went wrong writing to file")


"""
    Prompts user the question with the choices following. Parses input and returns value or -1 if out of range.
"""
def prompt_user(question, choices):
    i = 1
    s = question + '\n'
    for c in choices:
        s += str(i) + ": " + str(c["text"]) + '\n'
        i = int(i) + 1
    try:
        val = input(s)
        i_val = int(val)
    except:
        if val == 'q' or val.lower() == 'quit':
            quit_all()
        else:
            return -1

    if i_val > i or i_val <= 0:
        return -1
    else:
        return i_val



