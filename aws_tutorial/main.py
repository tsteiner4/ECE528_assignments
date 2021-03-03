# This example shows a basic API call to AWS
# Load the AWS Python SDK
import boto3
# Configure Polly client *implicitly*
polly = boto3.client('polly')
# Call the Amazon Polly Web Service
result = polly.synthesize_speech(Text='Hello World!',
OutputFormat='mp3', VoiceId='Aditi')

# Save the Audio File
audio = result['AudioStream'].read()
with open("helloworld.mp3","wb") as file:
    file.write(audio)
