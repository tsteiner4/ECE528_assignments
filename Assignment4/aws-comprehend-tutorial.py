import boto3
import json
import pycountry
from datetime import datetime
from tabulate import tabulate
import os
from time import sleep
import smart_open

# Global for storing comprehend service pointer
comprehend = []
# Base path for storing output text files
base_output_path = './results/'

"""
    Exit application
"""
def quit_all():
    exit()

"""
    Use boto3 to start comprehend.
"""
def setup_service():
    global comprehend
    try:
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
        # Let's use Amazon S3
        s3 = boto3.resource('s3')
        # Print out bucket names
        for bucket in s3.buckets.all():
            print(bucket.name)
    except:
        print('Error setting up the boto3 service. Check your aws credentials.')


def save_result_to_file(result, filename):
    global base_output_path
    try:
        if not os.path.isdir(base_output_path):
            os.mkdir(base_output_path)
        unq_filename = base_output_path + filename + "_" + datetime.now().strftime("%m_%d-%H_%M_%S") + ".txt"
        f = open(unq_filename, "a")
        f.write(result)
        f.close()
    except:
        print("Something went wrong writing to file")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""START OF SINGLE DOCUMENT FUNCTIONS"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
    Detect the language in the given text. Input is text to detect in and output is list of languages with scores.
    Function parses output to display better info for the user.
    {
    "Languages": [
        {
            "LanguageCode": "en",
            "Score": 0.9793661236763
        }
    ]
    }
"""
def detect_language(text):
    global comprehend
    i = 1
    val = comprehend.detect_dominant_language(Text=text)
    print(val)
    if val["Languages"] is not None:
        for lang in val["Languages"]:
            name = pycountry.languages.get(alpha_2=lang["LanguageCode"]).name
            print("Language " + str(i) + ": " + name)
            print("Score: " + str(lang["Score"]) + "\n")
            i += 1
    else:
        print("No languages detected")

    return val


"""
    Detect the entities in the given text. Input is text to detect in and language to use (not needed, but helps
    performance).
    Output is list of entities with scores. Function parses output to display better info for the user.
    {
        "Entities": [
            {
                "Text": "today",
                "Score": 0.97,
                "Type": "DATE",
                "BeginOffset": 14,
                "EndOffset": 19
            },
            {
                "Text": "Seattle",
                "Score": 0.95,
                "Type": "LOCATION",
                "BeginOffset": 23,
                "EndOffset": 30
            }
        ],
        "LanguageCode": "en"
    }
"""
def detect_entities(text):
    global comprehend
    i = 0
    val = comprehend.detect_entities(Text=text, LanguageCode='en')
    print(val)
    if len(val["Entities"]) > 0:
        for e in val["Entities"]:
            text = e["Text"]
            print("Entity Text " + str(i) + ": " + text)
            print("Type: " + e["Type"])
            print("Score: " + str(e["Score"]) + "\n")
            i += 1
    else:
        print("No entities detected")
    return val


"""
    Detect the phrases in the given text. Input is text to detect in and language to use (not needed, but helps 
    performance).
    Output is list of key phrases with scores. Function parses output to display better info for the user.
    {
        "LanguageCode": "en",
        "KeyPhrases": [
            {
                "Text": "today",
                "Score": 0.89,
                "BeginOffset": 14,
                "EndOffset": 19
            },
            {
                "Text": "Seattle",
                "Score": 0.91,
                "BeginOffset": 23,
                "EndOffset": 30
            }
        ]
    }
"""
def detect_phrases(text):
    global comprehend
    val = comprehend.detect_key_phrases(Text=text, LanguageCode='en')
    i = 0
    print(val)
    if len(val["KeyPhrases"]) > 0:
        for p in val["KeyPhrases"]:
            text = p["Text"]
            print("Key Phrase " + str(i) + ": " + text)
            print("Score: " + str(p["Score"]) + "\n")
            i += 1
    else:
        print("No phrases detected")
    return val


"""
    Detect the personally identifiable information in the given text. Input is text to detect in and language to use
    (not needed, but helps performance).
    Output is list of pii with scores. Function parses output to display better info for the user.
    {
        "Entities": [
            {
                "Score": 0.9999669790267944,
                "Type": "NAME",
                "BeginOffset": 6,
                "EndOffset": 18
            },
            {
                "Score": 0.8905550241470337,
                "Type": "CREDIT_DEBIT_NUMBER",
                "BeginOffset": 69,
                "EndOffset": 88
            },
            {
                "Score": 0.9999889731407166,
                "Type": "ADDRESS",
                "BeginOffset": 103,
                "EndOffset": 138
            }
        ]
    }  
"""
def detect_pii(text):
    global comprehend
    val = comprehend.detect_pii_entities(Text=text, LanguageCode='en')
    i = 0
    print(val)
    if len(val["Entities"]) > 0:
        for p in val["KeyPhrases"]:
            text = p["Text"]
            print("Key Phrase " + str(i) + ": " + text)
            print("Type: " + p["Type"])
            print("Score: " + str(p["Score"]) + "\n")
            i += 1
    else:
        print("No personal information detected")
    return val



"""
    Detect the sentiment of the given text. Input is text to detect in and language to use (not needed, but helps 
    performance).
    Output is a sentiment table with scores. Function parses output to display better info for the user.
    {
        "SentimentScore": {
            "Mixed": 0.014585512690246105,
            "Positive": 0.31592071056365967,
            "Neutral": 0.5985543131828308,
            "Negative": 0.07093945890665054
        },
        "Sentiment": "NEUTRAL",
        "LanguageCode": "en"
    }
"""
def detect_sentiment(text):
    global comprehend
    val = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    i = 0
    print(val)
    print("Overall Sentiment: " + val["Sentiment"])
    if len(val["SentimentScore"]) > 0:
        for key in val["SentimentScore"]:
            print('{0:{width}} {1:{width}}'.format(key, str.format("{:.2%}", (val["SentimentScore"][key])), width=10))
    else:
        print("Error in sentiment detection")
    return val


"""
    Detect the syntax of the given text with a specified language (not needed, but helps performance).
    Output is list of syntax tokens with each element's part of speech identified and a score. Function displays this
    more clearly.
    {
        `"SyntaxTokens": [
            {
                "Text": "It", 
                "EndOffset": 2, 
                "BeginOffset": 0, 
                "PartOfSpeech": {
                    "Tag": "PRON", 
                    "Score": 0.8389829397201538
                }, 
                "TokenId": 1
            }, 
            {
                "Text": "is", 
                "EndOffset": 5, 
                "BeginOffset": 3, 
                "PartOfSpeech": {
                    "Tag": "AUX", 
                    "Score": 0.9189288020133972
                }, 
                "TokenId": 2
            }, 
            {
                "Text": "raining", 
                "EndOffset": 13, 
                "BeginOffset": 6, 
                "PartOfSpeech": {
                    "Tag": "VERB", 
                    "Score": 0.9977611303329468
                }, 
                "TokenId": 3
            }
        ]
    }
"""
def detect_syntax(text):
    global comprehend
    val = comprehend.detect_syntax(Text=text, LanguageCode='en')
    text_arr = []
    syn_arr = []
    score_arr = []
    print(val)
    if len(val["SyntaxTokens"]) > 0:
        for el in val["SyntaxTokens"]:
            text_arr.append(el["Text"])
            syn_arr.append(el["PartOfSpeech"]["Tag"])
            score_arr.append(el["PartOfSpeech"]["Score"])
        print(tabulate({"Text": text_arr, "Syntax": syn_arr, "Score": score_arr}, headers="keys"))
    else:
        print("Error in syntax detection")

    return val

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""START OF SYNCHRONOUS BATCH DOCUMENT FUNCTIONS"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
    Performs detect language of a list of texts synchronously. Returns Result List with the Indices and then responses
    similar to detect_dominant_language. Function prints to a file with result list for each document.
"""
def batch_detect_language(text, path_list=[]):
    global comprehend
    val = comprehend.batch_detect_dominant_language(TextList=text)
    i = 0
    if len(val["ResultList"]) > 0:
        for ind in val["ResultList"]:
            print("Document Number " + str(ind["Index"]))
            for lang in ind["Languages"]:
                name = pycountry.languages.get(alpha_2=lang["LanguageCode"]).name
                print("Language " + str(i) + ": " + name)
                print("Score: " + str(lang["Score"]) + "\n")
                i += 1
    else:
        print("No languages detected")

    fmt_val = json.dumps(val, indent=4, sort_keys=True)
    if not path_list:
        save_result_to_file(fmt_val, "results_detect_language")
    else:
        save_result_to_file(str(path_list) + "\n\n" + fmt_val, "results_detect_language")
    return val


"""
    Performs detect entities of a list of texts synchronously. Returns Result List with the Indices and then responses
    similar to detect_entities.
"""
def batch_detect_entities(text, path_list=[]):
    global comprehend
    val = comprehend.batch_detect_entities(TextList=text, LanguageCode='en')
    i = 0
    if len(val["ResultList"]) > 0:
        for ind in val["ResultList"]:
            print("Document Number " + str(ind["Index"]))
            if len(ind["Entities"]) > 0:
                for e in ind["Entities"]:
                    text = e["Text"]
                    print("Entity Text " + str(i) + ": " + text)
                    print("Type: " + e["Type"])
                    print("Score: " + str(e["Score"]) + "\n")
                    i += 1
            else:
                print("No entities")

        fmt_val = json.dumps(val, indent=4, sort_keys=True)
        if not path_list:
            save_result_to_file(fmt_val, "results_detect_entities")
        else:
            save_result_to_file(str(path_list) + "\n\n" + fmt_val, "results_detect_entities")
    else:
        print("No results found")

    return val


"""
    Performs detect phrases of a list of texts synchronously. Returns Result List with the Indices and then responses
    similar to detect_phrases.
"""
def batch_detect_phrases(text, path_list=[]):
    global comprehend
    val = comprehend.batch_detect_key_phrases(TextList=text, LanguageCode='en')
    i = 0
    if len(val["ResultList"]) > 0:
        for ind in val["ResultList"]:
            print("Document Number " + str(ind["Index"]))
            if len(ind["KeyPhrases"]) > 0:
                for p in ind["KeyPhrases"]:
                    text = p["Text"]
                    print("Key Phrase " + str(i) + ": " + text)
                    print("Score: " + str(p["Score"]) + "\n")
                    i += 1
            else:
                print("No phrases detected")

        fmt_val = json.dumps(val, indent=4, sort_keys=True)
        if not path_list:
            save_result_to_file(fmt_val, "results_detect_phrases")
        else:
            save_result_to_file(str(path_list) + "\n\n" + fmt_val, "results_detect_phrases")
    else:
        print("No results found")

    return val


"""
    Performs detect sentiment of a list of texts synchronously. Returns Result List with the Indices and then responses
    similar to detect_sentiment.
"""
def batch_detect_sentiment(text, path_list=[]):
    global comprehend
    val = comprehend.batch_detect_sentiment(TextList=text, LanguageCode='en')
    if len(val["ResultList"]) > 0:
        for ind in val["ResultList"]:
            print("Document Number " + str(ind["Index"]))
            if len(ind["SentimentScore"]) > 0:
                for key in ind["SentimentScore"]:
                    print('{0:{width}} {1:{width}}'.format(key, str.format("{:.2%}", (ind["SentimentScore"][key])),
                                                           width=10))
            else:
                print("Error in sentiment detection")

        fmt_val = json.dumps(val, indent=4, sort_keys=True)
        if not path_list:
            save_result_to_file(fmt_val, "results_detect_sentiment")
        else:
            save_result_to_file(str(path_list) + "\n\n" + fmt_val, "results_detect_sentiment")
    else:
        print("No results found")

    return val


"""
    Performs detect syntax of a list of texts synchronously. Returns Result List with the Indices and then responses
    similar to detect_syntax.
"""
def batch_detect_syntax(text, path_list=[]):
    global comprehend
    val = comprehend.batch_detect_syntax(TextList=text, LanguageCode='en')
    if len(val["ResultList"]) > 0:
        for ind in val["ResultList"]:
            print("Document Number " + str(ind["Index"]))
            text_arr = []
            syn_arr = []
            score_arr = []
            if len(ind["SyntaxTokens"]) > 0:
                for el in ind["SyntaxTokens"]:
                    text_arr.append(el["Text"])
                    syn_arr.append(el["PartOfSpeech"]["Tag"])
                    score_arr.append(el["PartOfSpeech"]["Score"])
                print(tabulate({"Text": text_arr, "Syntax": syn_arr, "Score": score_arr}, headers="keys"))
            else:
                print("No syntax detected")

        fmt_val = json.dumps(val, indent=4, sort_keys=True)
        if not path_list:
            save_result_to_file(fmt_val, "results_detect_syntax")
        else:
            save_result_to_file(str(path_list) + "\n\n" + fmt_val, "results_detect_syntax")
    else:
        print("No results found")
    return val


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""START OF ASYNC BATCH DOCUMENT FUNCTIONS"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def start_async_dominant_lang():
    global comprehend
    response = comprehend.start_dominant_language_detection_job(
        InputDataConfig={
            'S3Uri': 's3://steinerdocclassifier/',
            'InputFormat': 'ONE_DOC_PER_FILE'
        },
        OutputDataConfig={
            'S3Uri': 's3://steineroutputbucket/'
        },
        DataAccessRoleArn='arn:aws:iam::236810755497:role/Comprehend_Access',
        JobName='dominant-lang-1'
    )
    print(json.dumps(response, sort_keys=True, indent=4))
    jobId = response['JobId']
    return jobId

def check_dominant_lang(jobId):
    success = 'FAILED'
    results = []

    job = comprehend.describe_dominant_language_detection_job(JobId=jobId)
    print(job)
    status = job['DominantLanguageDetectionJobProperties']['JobStatus']
    if status == 'COMPLETED':
        output_data_s3_file = job['DominantLanguageDetectionJobProperties']['OutputDataConfig']['S3Uri']

        # Load the output into a result dictionary    # Get the files.
        with smart_open.open(output_data_s3_file) as fi:
            for line in fi.readlines():
                if line:
                    if line.find('{') >= 0:
                        line = line[line.find('{'):]
                        results.extend([json.loads(line)])
        print(results)
    return success, results

# TODO
def async_entities_detection():
    global comprehend
    response = comprehend.start_entities_detection_job(
        InputDataConfig={
            'S3Uri': 's3://steinerdocclassifier/',
            'InputFormat': 'ONE_DOC_PER_FILE'
        },
        OutputDataConfig={
            'S3Uri': 's3://steineroutputbucket/'
        },
        DataAccessRoleArn='arn:aws:iam::236810755497:role/Comprehend_Access',
        JobName='dominant-lang-1'
    )
    print(json.dumps(response, sort_keys=True, indent=4))
    jobId = response['JobId']
    job = comprehend.describe_entities_detection_job(JobId=jobId)
    waited = 0

    sleep_time = 60
    timeout = 15 * 60 / sleep_time
    print(job)
    # Wait until job is complete (takes a few mins or longer depending on data size)
    while job['DominantLanguageDetectionJobProperties']['JobStatus'] != 'COMPLETED' and \
            job['DominantLanguageDetectionJobProperties']['JobStatus'] != 'FAILED':
        sleep(sleep_time)
        waited += sleep_time
        assert waited // sleep_time < timeout
        job = comprehend.describe_entities_detection_job(JobId=jobId)
        print(job)
    if job['DominantLanguageDetectionJobProperties']['JobStatus'] == 'FAILED':
        print("Failed")
    else:
        output_data_s3_file = job['DominantLanguageDetectionJobProperties']['OutputDataConfig']['S3Uri']

        # Load the output into a result dictionary    # Get the files.
        results = []
        # with smart_open.open(output_data_s3_file, encoding='utf-8') as fi:
        for line in smart_open.open(output_data_s3_file, encoding='utf-8'):
            print(repr(line))
            # results.extend([json.loads(line) for line in fi.readlines() if line])
        # print(results)
    return

# TODO
def async_events_detection():
    global comprehend
    response = comprehend.start_events_detection_job(
        InputDataConfig={
            'S3Uri': 's3://steinerdocclassifier/',
            'InputFormat': 'ONE_DOC_PER_FILE'
        },
        OutputDataConfig={
            'S3Uri': 's3://steineroutputbucket/'
        },
        DataAccessRoleArn='arn:aws:iam::236810755497:role/Comprehend_Access',
        JobName='dominant-lang-1'
    )
    print(json.dumps(response, sort_keys=True, indent=4))
    jobId = response['JobId']
    job = comprehend.describe_events_detection_job(JobId=jobId)
    waited = 0

    sleep_time = 60
    timeout = 15 * 60 / sleep_time
    print(job)
    # Wait until job is complete (takes a few mins or longer depending on data size)
    while job['DominantLanguageDetectionJobProperties']['JobStatus'] != 'COMPLETED' and \
            job['DominantLanguageDetectionJobProperties']['JobStatus'] != 'FAILED':
        sleep(sleep_time)
        waited += sleep_time
        assert waited // sleep_time < timeout
        job = comprehend.describe_events_detection_job(JobId=jobId)
        print(job)
    if job['DominantLanguageDetectionJobProperties']['JobStatus'] == 'FAILED':
        print("Failed")
    else:
        output_data_s3_file = job['DominantLanguageDetectionJobProperties']['OutputDataConfig']['S3Uri']

        # Load the output into a result dictionary    # Get the files.
        results = []
        # with smart_open.open(output_data_s3_file, encoding='utf-8') as fi:
        for line in smart_open.open(output_data_s3_file, encoding='utf-8'):
            print(repr(line))
            # results.extend([json.loads(line) for line in fi.readlines() if line])
        # print(results)
    return

# TODO
def async_key_phrase_detction():
    global comprehend
    response = comprehend.start_key_phrases_detection_job(
        InputDataConfig={
            'S3Uri': 's3://steinerdocclassifier/',
            'InputFormat': 'ONE_DOC_PER_FILE'
        },
        OutputDataConfig={
            'S3Uri': 's3://steineroutputbucket/'
        },
        DataAccessRoleArn='arn:aws:iam::236810755497:role/Comprehend_Access',
        JobName='dominant-lang-1'
    )
    print(json.dumps(response, sort_keys=True, indent=4))
    jobId = response['JobId']
    job = comprehend.describe_key_phrases_detection_job(JobId=jobId)
    waited = 0

    sleep_time = 60
    timeout = 15 * 60 / sleep_time
    print(job)
    # Wait until job is complete (takes a few mins or longer depending on data size)
    while job['DominantLanguageDetectionJobProperties']['JobStatus'] != 'COMPLETED' and \
            job['DominantLanguageDetectionJobProperties']['JobStatus'] != 'FAILED':
        sleep(sleep_time)
        waited += sleep_time
        assert waited // sleep_time < timeout
        job = comprehend.describe_key_phrases_detection_job(JobId=jobId)
        print(job)
    if job['DominantLanguageDetectionJobProperties']['JobStatus'] == 'FAILED':
        print("Failed")
    else:
        output_data_s3_file = job['DominantLanguageDetectionJobProperties']['OutputDataConfig']['S3Uri']

        # Load the output into a result dictionary    # Get the files.
        results = []
        # with smart_open.open(output_data_s3_file, encoding='utf-8') as fi:
        for line in smart_open.open(output_data_s3_file, encoding='utf-8'):
            print(repr(line))
            # results.extend([json.loads(line) for line in fi.readlines() if line])
        # print(results)
    return


# TODO
def async_key_phrase_detction():
    global comprehend
    response = comprehend.start_key_phrases_detection_job(
        InputDataConfig={
            'S3Uri': 's3://steinerdocclassifier/',
            'InputFormat': 'ONE_DOC_PER_FILE'
        },
        OutputDataConfig={
            'S3Uri': 's3://steineroutputbucket/'
        },
        DataAccessRoleArn='arn:aws:iam::236810755497:role/Comprehend_Access',
        JobName='dominant-lang-1'
    )
    print(json.dumps(response, sort_keys=True, indent=4))
    jobId = response['JobId']
    job = comprehend.describe_key_phrases_detection_job(JobId=jobId)
    waited = 0

    sleep_time = 60
    timeout = 15 * 60 / sleep_time
    print(job)
    # Wait until job is complete (takes a few mins or longer depending on data size)
    while job['DominantLanguageDetectionJobProperties']['JobStatus'] != 'COMPLETED' and \
            job['DominantLanguageDetectionJobProperties']['JobStatus'] != 'FAILED':
        sleep(sleep_time)
        waited += sleep_time
        assert waited // sleep_time < timeout
        job = comprehend.describe_key_phrases_detection_job(JobId=jobId)
        print(job)
    if job['DominantLanguageDetectionJobProperties']['JobStatus'] == 'FAILED':
        print("Failed")
    else:
        output_data_s3_file = job['DominantLanguageDetectionJobProperties']['OutputDataConfig']['S3Uri']

        # Load the output into a result dictionary    # Get the files.
        results = []
        # with smart_open.open(output_data_s3_file, encoding='utf-8') as fi:
        for line in smart_open.open(output_data_s3_file, encoding='utf-8'):
            print(repr(line))
            # results.extend([json.loads(line) for line in fi.readlines() if line])
        # print(results)
    return


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

    return funcs


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


def test_output_read():
    # for line in smart_open.open('output.tar.gz', encoding='utf-8'):
    #     line = line[line.find('{'):]
    #     # if "" in line:
    #     #     line = line.rfind("\\x00")
    #     print(repr(line))
    results = []
    with smart_open.open('output.tar.gz') as fi:
        for line in fi.readlines():
            if line:
                if line.find('{') >= 0:
                    line = line[line.find('{'):]
                    results.extend([json.loads(line)])
    print(results)

"""
    Main text input loop for deciding when to finish and how to enter in data.
"""
def main_loop():
    finished = False
    while not finished:
        options = [{"text": "Text input", "function": text_input},
                   {"text": "Single document", "function": single_document},
                   {"text": "List of documents", "function": list_of_documents},
                   {"text": "Start Asynch Detect", "function": async_job_loop},
                   {"text": "quit", "function": quit_all}]
        resp = prompt_user("How would you like to provide the text?", options)
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
    job = start_async_dominant_lang()
    status = check_dominant_lang(job)
    while status != 'COMPLETED' or status != 'FAILED':
        sleep(60)
        status = check_dominant_lang(job)

    # test_output_read()
