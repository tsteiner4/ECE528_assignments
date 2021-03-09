import pycountry
from tabulate import tabulate
import config

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
    i = 1
    val = config.comprehend.detect_dominant_language(Text=text)
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
    i = 0
    val = config.comprehend.detect_entities(Text=text, LanguageCode='en')
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
    val = config.comprehend.detect_key_phrases(Text=text, LanguageCode='en')
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
    val = config.comprehend.detect_pii_entities(Text=text, LanguageCode='en')
    i = 0
    print(val)
    if len(val["Entities"]) > 0:
        for p in val["Entities"]:
            text = text[p["BeginOffset"]:p["EndOffset"]]
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
    val = config.comprehend.detect_sentiment(Text=text, LanguageCode='en')
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
    val = config.comprehend.detect_syntax(Text=text, LanguageCode='en')
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