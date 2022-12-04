import requests
from speech_to_text.configure import auth_key
import time
upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint="https://api.assemblyai.com/v2/transcript"
headers = {'authorization': auth_key,
            'content-type': 'application/json'}

def upload(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data


    upload_response = requests.post(upload_endpoint,
                            headers=headers,
                            data=read_file(filename))

    #print(response.json())
    audio_url=upload_response.json()['upload_url']
    return audio_url
def transcribe(audio_url):
    transcript_request=json={"audio_url":audio_url}
    transcript_response=requests.post(transcript_endpoint,json=transcript_request,headers=headers)

    #print(response.json())
    job_id=transcript_response.json()['id']

    return job_id

# poll
def poll(transcript_id):
    polling_endpoint= transcript_endpoint + '/' + transcript_id

    polling_response=requests.get(polling_endpoint,headers=headers)
    return polling_response.json()

    #print(polling_response.json())
def get_transcription_url(audio_url):
    transcript_id=transcribe(audio_url)
    while True:
        data=poll(transcript_id)
        #polling_response=requests.get(polling_endpoint,headers=headers)

        if data['status']=='completed':
            return data , None
        elif data['status']=='error':
            return data , data["error"]
        print("waiting 30 seconds....")
        time.sleep

#transcipt_id=transcribe(audio_url)

def save_transcirpt(audio_url,filename):
    data,error=get_transcription_url(audio_url)
    #print(job_id)


    text_filename=filename+ ".txt"

    if data:
        with open(text_filename,"w") as f:
            f.write (data['text'])

        print("Transcription is saved!!!")

    elif error:
        print("Error!",error)

    print(data)


