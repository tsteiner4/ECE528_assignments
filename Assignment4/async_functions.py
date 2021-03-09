import json
import datetime
import smart_open
import config
from utils import save_result_to_file, prompt_user

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""START OF ASYNC BATCH DOCUMENT FUNCTIONS"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def list_jobs_for_function(fun):
    options = []
    jobId = '0'
    time = 15
    filter = {"SubmitTimeAfter": datetime.datetime.now() - datetime.timedelta(minutes=time)}
    if fun == 0:
        response = config.comprehend.list_dominant_language_detection_jobs(Filter=filter)
        props = response["DominantLanguageDetectionJobPropertiesList"]

    elif fun == 1:
        response = config.comprehend.list_entities_detection_jobs(Filter=filter)
        props = response["EntitiesDetectionJobPropertiesList"]

    elif fun == 2:
        response = config.comprehend.list_key_phrases_detection_jobs(Filter=filter)
        props = response["KeyPhrasesDetectionJobPropertiesList"]

    elif fun == 3:
        response = config.comprehend.list_pii_entities_detection_jobs(Filter=filter)
        props = response["PiiEntitiesDetectionJobPropertiesList"]

    elif fun == 4:
        response = config.comprehend.list_sentiment_detection_jobs(Filter=filter)
        props = response["SentimentDetectionJobPropertiesList"]

    elif fun == 5:
        response = config.comprehend.list_topics_detection_jobs(Filter=filter)
        props = response["TopicsDetectionJobPropertiesList"]


    for jobs in props:
        object_text = "Job started: " + str(jobs["SubmitTime"]) + " Status: " + str(jobs["JobStatus"])
        options.append({"text": object_text, "function": ''})

    options.append({"text": "None", "function": ''})
    if len(props) == 0:
        print("No jobs to check")
        return -1
    else:
        user_input = prompt_user("Which job do you want to check?", options)
        if 1 <= user_input < len(options):
            jobId = props[user_input - 1]["JobId"]
        elif user_input == len(options):
            return -1
        else:
            print("Please enter a valid selection")
            list_jobs_for_function(fun)
    return jobId


def start_async_dominant_lang():
    response = config.comprehend.start_dominant_language_detection_job(
        InputDataConfig={
            'S3Uri': 's3://steinerdocclassifier/',
            'InputFormat': 'ONE_DOC_PER_FILE'
        },
        OutputDataConfig={
            'S3Uri': 's3://steineroutputbucket/'
        },
        DataAccessRoleArn='arn:aws:iam::236810755497:role/Comprehend_Access',
        JobName='dominant-lang'
    )
    print(json.dumps(response, sort_keys=True, indent=4))
    jobId = response['JobId']
    return jobId


def start_async_entities_detection():
    response = config.comprehend.start_entities_detection_job(
        InputDataConfig={
            'S3Uri': 's3://steinerdocclassifier/',
            'InputFormat': 'ONE_DOC_PER_FILE'
        },
        OutputDataConfig={
            'S3Uri': 's3://steineroutputbucket/'
        },
        LanguageCode="en",
        DataAccessRoleArn='arn:aws:iam::236810755497:role/Comprehend_Access',
        JobName='entities'
    )
    print(json.dumps(response, sort_keys=True, indent=4))
    jobId = response['JobId']
    return jobId


def start_async_key_phrase_detection():
    response = config.comprehend.start_key_phrases_detection_job(
        InputDataConfig={
            'S3Uri': 's3://steinerdocclassifier/',
            'InputFormat': 'ONE_DOC_PER_FILE'
        },
        OutputDataConfig={
            'S3Uri': 's3://steineroutputbucket/'
        },
        LanguageCode="en",
        DataAccessRoleArn='arn:aws:iam::236810755497:role/Comprehend_Access',
        JobName='key-phrases'
    )
    print(json.dumps(response, sort_keys=True, indent=4))
    jobId = response['JobId']
    return jobId


def start_async_pii_detection():
    response = config.comprehend.start_pii_entities_detection_job(
        InputDataConfig={
            'S3Uri': 's3://steinerdocclassifier/',
            'InputFormat': 'ONE_DOC_PER_FILE'
        },
        OutputDataConfig={
            'S3Uri': 's3://steineroutputbucket/'
        },
        LanguageCode="en",
        Mode="ONLY_REDACTION",
        RedactionConfig={
            'MaskMode': 'REPLACE_WITH_PII_ENTITY_TYPE',
            'PiiEntityTypes': ['ALL']
        },
        DataAccessRoleArn='arn:aws:iam::236810755497:role/Comprehend_Access',
        JobName='pii'
    )
    print(json.dumps(response, sort_keys=True, indent=4))
    jobId = response['JobId']
    return jobId


def start_async_sentiment_detection():
    response = config.comprehend.start_sentiment_detection_job(
        InputDataConfig={
            'S3Uri': 's3://steinerdocclassifier/',
            'InputFormat': 'ONE_DOC_PER_FILE'
        },
        OutputDataConfig={
            'S3Uri': 's3://steineroutputbucket/'
        },
        LanguageCode="en",
        DataAccessRoleArn='arn:aws:iam::236810755497:role/Comprehend_Access',
        JobName='sentiment'
    )
    print(json.dumps(response, sort_keys=True, indent=4))
    jobId = response['JobId']
    return jobId


def start_async_topics_detection():
    response = config.comprehend.start_topics_detection_job(
        InputDataConfig={
            'S3Uri': 's3://steinerdocclassifier/',
            'InputFormat': 'ONE_DOC_PER_FILE'
        },
        OutputDataConfig={
            'S3Uri': 's3://steineroutputbucket/'
        },
        DataAccessRoleArn='arn:aws:iam::236810755497:role/Comprehend_Access',
        JobName='topics'
    )
    print(json.dumps(response, sort_keys=True, indent=4))
    jobId = response['JobId']
    return jobId


def check_async_status(type):
    jobId = list_jobs_for_function(type)

    if jobId == -1:
        return -1
    status = 'FAILED'
    file_out = ""
    results = []

    if type == 0:
        job = config.comprehend.describe_dominant_language_detection_job(JobId=jobId)
        print(job)
        properties = job['DominantLanguageDetectionJobProperties']
        file_out = 'results_async_language_detection'
    elif type == 1:
        job = config.comprehend.describe_entities_detection_job(JobId=jobId)
        print(job)
        properties = job['EntitiesDetectionJobProperties']
        file_out = 'results_async_entities_detection'
    elif type == 2:
        job = config.comprehend.describe_key_phrases_detection_job(JobId=jobId)
        print(job)
        properties = job['KeyPhrasesDetectionJobProperties']
        file_out = 'results_async_key_phrases_detection'
    elif type == 3:
        job = config.comprehend.describe_pii_entities_detection_job(JobId=jobId)
        print(job)
        properties = job['PiiEntitiesDetectionJobProperties']
        file_out = 'results_async_pii_detection'
    elif type == 4:
        job = config.comprehend.describe_sentiment_detection_job(JobId=jobId)
        print(job)
        properties = job['SentimentDetectionJobProperties']
        file_out = 'results_async_sentiment_detection'
    elif type == 5:
        job = config.comprehend.describe_topics_detection_job(JobId=jobId)
        print(job)
        properties = job['TopicsDetectionJobProperties']
        file_out = 'results_async_topics_detection'
    else:
        return -1

    status = properties['JobStatus']
    if status == 'COMPLETED':
        if type == 3:  # PII doesn't follow same output format, so we just hardcode one output for now
            output_data_s3_file = properties['OutputDataConfig']['S3Uri'] + 'business/001.txt.out'

            # Load the output into a result dictionary    # Get the files.
            with smart_open.open(output_data_s3_file) as fi:
                for line in fi.readlines():
                    if line:
                        results.extend([line])
            save_result_to_file(results, file_out)
            print(results)
            return status, results
        elif type == 5:
            output_data_s3_file = properties['OutputDataConfig']['S3Uri']

            # Load the output into a result dictionary    # Get the files.
            with smart_open.open(output_data_s3_file) as fi:
                for line in fi.readlines():
                    if line:
                        results.extend([line])
            save_result_to_file(results, file_out)
            print(results)
            return status, results
        else:
            output_data_s3_file = properties['OutputDataConfig']['S3Uri']

            # Load the output into a result dictionary    # Get the files.
            with smart_open.open(output_data_s3_file) as fi:
                for line in fi.readlines():
                    if line:
                        if line.find('{') >= 0:
                            line = line[line.find('{'):]
                            results.extend([json.loads(line)])
            results = sorted(results, key=lambda i: i["File"])
            save_result_to_file(results, file_out)
            print(results)
    return status, results
