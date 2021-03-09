import json
import pycountry
from tabulate import tabulate
import config
from utils import save_result_to_file

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""START OF SYNCHRONOUS BATCH DOCUMENT FUNCTIONS"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
    Performs detect language of a list of texts synchronously. Returns Result List with the Indices and then responses
    similar to detect_dominant_language. Function prints to a file with result list for each document.
"""
def batch_detect_language(text, path_list=[]):
    val = config.comprehend.batch_detect_dominant_language(TextList=text)
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
    val = config.comprehend.batch_detect_entities(TextList=text, LanguageCode='en')
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
    val = config.comprehend.batch_detect_key_phrases(TextList=text, LanguageCode='en')
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
    val = config.comprehend.batch_detect_sentiment(TextList=text, LanguageCode='en')
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
    val = config.comprehend.batch_detect_syntax(TextList=text, LanguageCode='en')
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
