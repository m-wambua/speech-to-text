from speech_to_text.api_communication import *
import sys
filename =  sys.argv[1]
audio_url=upload(filename)
save_transcirpt(audio_url,filename)