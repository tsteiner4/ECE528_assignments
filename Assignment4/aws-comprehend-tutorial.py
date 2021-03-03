import boto3
import json
comprehend = []


def quit_all():
    exit()


def setup_service():
    global comprehend
    try:
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
    except:
        print('Error setting up the boto3 service. Check your aws credentials.')


def detect_language(text):
    global comprehend
    print('Calling DetectDominantLanguage')
    print(json.dumps(comprehend.detect_dominant_language(Text = text), sort_keys=True, indent=4))
    print("End of DetectDominantLanguage\n")


def detect_entities(text):
    global comprehend
    print('Calling DetectEntities')
    print(json.dumps(comprehend.detect_entities(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
    print('End of DetectEntities\n')


def detect_phrases(text):
    global comprehend
    print('Calling DetectKeyPhrases')
    print(json.dumps(comprehend.detect_key_phrases(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
    print('End of DetectKeyPhrases\n')


def detect_pii(text):
    global comprehend
    print('Calling DetectPiiEntities')
    print(json.dumps(comprehend.detect_pii_entities(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
    print('End of DetectPiiEntities\n')


def detect_sentiment(text):
    global comprehend
    print('Calling DetectSentiment')
    print(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
    print('End of DetectSentiment\n')


def detect_syntax(text):
    global comprehend
    print('Calling DetectSyntax')
    print(json.dumps(comprehend.detect_syntax(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
    print('End of DetectSyntax\n')


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


def aws_function_list(type):
    funcs = []
    if type == 'text':
        funcs = [{"text": "Detect Language", "function": detect_language},
                 {"text": "Detect entities", "function": detect_entities},
                 {"text": "Detect Key Phrases", "function": detect_phrases},
                 {"text": "Detect Personally Identifiable Information", "function": detect_pii},
                 {"text": "Detect Sentiment", "function": detect_sentiment},
                 {"text": "Detect Syntax", "function": detect_syntax},
                 {"text": "<-- Go back", "function": ''}]

    return funcs

def text_input():
    options = aws_function_list('text')
    resp = prompt_user("What type of processing would you like to do?", options)

    if resp >= 1:
        if options[resp - 1]["function"] != '':
            sentence = input("Enter a sentence to be analyzed:")
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

def main_loop():
    finished = False
    while not finished:
        options = [{"text": "Text input", "function": text_input},
                   {"text": "Single document", "function": quit_all},
                   {"text": "List of documents", "function": quit_all},
                   {"text": "quit", "function": quit_all}]
        resp = prompt_user("What type of processing do you want to do?", options)
        if resp >= 1:
            options[resp-1]["function"]()
        else:
            print("Please enter a valid selection")
            continue


if __name__ == '__main__':
    setup_service()
    text = "Hi, how are you doing today? I am great!"
    text = "Hola, como estas?"
    text = "Bonjour, je m'appelle Tristan et je t'aime"
    # detect_language(text)
    main_loop()
