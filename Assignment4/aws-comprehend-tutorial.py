import boto3
from single_document_functions import *
from batch_document_functions import *
from async_functions import *
from utils import *

"""
    Exit application
"""
def quit_all():
    exit()

"""
    Use boto3 to start comprehend.
"""
def setup_service():
    try:
        config.comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
    except:
        print('Error setting up the boto3 service. Check your aws credentials.')


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


"""
    Makes a list of dictionaries to map choices to function calls
"""
def aws_function_list(type):
    funcs = []
    if type == 'text':
        funcs = [{"text": "Detect Language", "function": detect_language},
                 {"text": "Detect Entities", "function": detect_entities},
                 {"text": "Detect Key Phrases", "function": detect_phrases},
                 {"text": "Detect Personally Identifiable Information", "function": detect_pii},
                 {"text": "Detect Sentiment", "function": detect_sentiment},
                 {"text": "Detect Syntax", "function": detect_syntax},
                 {"text": "<-- Go back", "function": ''}]
    elif type == 'list':
        funcs = [{"text": "Detect Language", "function": batch_detect_language},
                 {"text": "Detect Entities", "function": batch_detect_entities},
                 {"text": "Detect Key Phrases", "function": batch_detect_phrases},
                 {"text": "Detect Sentiment", "function": batch_detect_sentiment},
                 {"text": "Detect Syntax", "function": batch_detect_syntax},
                 {"text": "<-- Go back", "function": ''}]
    elif type == 'start_async':
        funcs = [{"text": "Start Detect Language Job", "function": start_async_dominant_lang},
                 {"text": "Start Detect Entities Job", "function": start_async_entities_detection},
                 {"text": "Start Detect Key Phrases Job", "function": start_async_key_phrase_detection},
                 {"text": "Start Detect Personally Identifiable Information Job",
                  "function": start_async_pii_detection},
                 {"text": "Start Detect Sentiment Job", "function": start_async_sentiment_detection},
                 {"text": "Start Detect Topics Job", "function": start_async_topics_detection},
                 {"text": "<-- Go back", "function": ''}]
    elif type == 'check_async':
        funcs = [{"text": "Check Language Job", "function": check_async_status},
                 {"text": "Check Entities Job", "function": check_async_status},
                 {"text": "Check Key Phrases Job", "function": check_async_status},
                 {"text": "Check Personally Identifiable Info Job", "function": check_async_status},
                 {"text": "Check Sentiment Job", "function": check_async_status},
                 {"text": "Check Topics Job", "function": check_async_status},
                 {"text": "<-- Go back", "function": ''}]

    return funcs


def start_async_jobs():
    while True:
        options = aws_function_list('start_async')
        resp = prompt_user("What type of job would you like to start?", options)

        if resp >= 1:
            if options[resp - 1]["function"] != '':
                options[resp - 1]["function"]()
                cont = input("Do you want to start more jobs? (y/n): ")
                if cont.lower() == 'y' or cont.lower() == 'yes':
                    continue
                break
            else:
                return
        else:
            print("Please enter a valid selection")
            start_async_jobs()

def check_async_jobs():
    while True:
        options = aws_function_list('check_async')
        resp = prompt_user("What type of job would you like to check?", options)

        if resp >= 1:
            if options[resp - 1]["function"] != '':
                options[resp - 1]["function"](resp-1) # pass in the response to know which type to use
                cont = input("Do you want to check more jobs? (y/n): ")
                if cont.lower() == 'y' or cont.lower() == 'yes':
                    continue
                break
            else:
                return
        else:
            print("Please enter a valid selection")
            check_async_jobs()


"""
    Get the text from user input on the command line and perform desired function.
"""
def text_input():
    options = aws_function_list('text')
    resp = prompt_user("What type of processing would you like to do?", options)

    if resp >= 1:
        if options[resp - 1]["function"] != '':
            sentence = input("Enter a sentence to be analyzed: ")
            if sentence:
                options[resp - 1]["function"](sentence)
            else:
                print("Enter a valid sentence. Try again")
        else:
            return
    else:
        print("Please enter a valid selection")
        text_input()
    return


"""
    Process a document from a given path.
"""
def single_document():
    path = input("Please enter path to file: ")
    try:
        file = open(path, mode='r')
        all_text = file.read()

        file.close()

        while True:
            options = aws_function_list('text')
            print("\nFile Path: " + path)
            resp = prompt_user("What type of processing would you like to do?", options)

            if resp >= 1:
                if options[resp - 1]["function"] != '':
                    options[resp - 1]["function"](all_text)
                    cont = input("Do you want to do more processing with the same document? (y/n): ")
                    if cont.lower() == 'y' or cont.lower() == 'yes':
                        continue
                    break
                else:
                    return
            else:
                print("Please enter a valid selection")
                single_document()
    except:
        print("Path not found (or invalid). Try again")


"""
    Use text file to store list of file paths to process data from.
"""
def read_list_from_text():
    path = input("Please enter path to file: ")
    doc_list = []
    text_arr = []
    try:
        file = open(path, mode='r')
        lines = file.readlines()
        for line in lines:
            path_item = line.rstrip('\n')
            try:
                nfile = open(path_item, mode='r')
                data = nfile.read()
                doc_list.append(path_item)
                text_arr.append(data)
                nfile.close()
            except Exception as e:
                print(e)
        file.close()
        return doc_list, text_arr

    except:
        print("Path not found (or invalid). Try again")


"""
    Use loop to get list of paths for files to read text from and process.
"""
def read_list_from_loop():
    doc_list = []
    text_arr = []
    while True:
        path = input("Please enter path to a file to add to the list or q to stop: ")
        try:
            if path.lower() == 'q' or path.lower() == 'quit':
                break
            file = open(path, mode='r')
            data = file.read()
            doc_list.append(path)
            text_arr.append(data)
            file.close()
        except Exception as e:
            print("Path was not found (or invalid)")

    return doc_list, text_arr


"""
    Handler for when the user wishes to process a list of documents.
"""
def list_of_documents():
    options = [{"text": "List stored in text file", "function": read_list_from_text},
               {"text": "Enter paths in loop", "function": read_list_from_loop}]
    resp = prompt_user("How do you want to enter list of documents to process?", options)
    if resp >= 1:
        doc_list, text_arr = options[resp - 1]["function"]()
        if [] == text_arr:
            return

        options = aws_function_list('list')
        while True:
            resp = prompt_user("What type of processing would you like to do?", options)
            if resp >= 1:
                if options[resp - 1]["function"] != '':
                    options[resp - 1]["function"](text_arr, path_list=doc_list)
                else:
                    return
                cont = input("Do you want to do more processing with the same document list? (y/n): ")
                if cont.lower() == 'y' or cont.lower() == 'yes':
                    continue
                break
            else:
                print("Please enter a valid selection")
                list_of_documents()
    else:
        print("Please enter a valid selection")


def async_job_loop():
    while True:
        options = [{"text": "Start Async Batch Job using S3 Database", "function": start_async_jobs},
                   {"text": "Check status of job (save results if complete)", "function": check_async_jobs},
                   {"text": "<-- Go back", "function": ''}]
        resp = prompt_user("What do you want to do?", options)
        if resp >= 1:
            if options[resp - 1]["function"] != '':
                options[resp - 1]["function"]()
            else:
                return
        else:
            print("Please enter a valid selection")
            async_job_loop()
    return


def sync_job_loop():
    while True:
        options = [{"text": "Text input", "function": text_input},
                   {"text": "Single document", "function": single_document},
                   {"text": "List of documents", "function": list_of_documents},
                   {"text": "<-- Go back", "function": ''}]
        resp = prompt_user("How would you like to provide the text?", options)
        if resp >= 1:
            if options[resp - 1]["function"] != '':
                options[resp - 1]["function"]()
            else:
                return
        else:
            print("Please enter a valid selection")
            sync_job_loop()
    return


"""
    Main text input loop for deciding when to finish and how to enter in data.
"""
def main_loop():
    while True:
        options = [{"text": "Synchronous", "function": sync_job_loop},
                   {"text": "Asynchronous ", "function": async_job_loop},
                   {"text": "quit", "function": quit_all}]
        resp = prompt_user("Do you want to use synchronous or asynchronous functions?", options)
        if resp >= 1:
            options[resp-1]["function"]()
        else:
            print("Please enter a valid selection")
            continue

"""
    Set up aws service and start main loop
"""
if __name__ == '__main__':
    setup_service()
    # job = start_async_dominant_lang()
    # status, results = check_dominant_lang(job)
    main_loop()
    # while status != 'COMPLETED' and status != 'FAILED':
    #     sleep(60)
    #     status = check_dominant_lang(job)


