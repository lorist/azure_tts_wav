# speech_synthesis.py

"""
This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
export these two variables before running

usage: speech_synthesis.py [-h] [-c CSV] [-v VOICE] [-t TEXT] [-o OUTPUT_FILENAME]

optional arguments:
  -h, --help            show this help message and exit
  -c CSV, --csv CSV     csv filename. Be sure to escape commas in test. i.e. ","
  -v VOICE, --voice VOICE
                        Azure voice to generate audio. https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/SpeechServices
  -t TEXT, --text TEXT  text to record
  -o OUTPUT_FILENAME, --output_filename OUTPUT_FILENAME
                        audio filename to save
"""
import logging
import os, argparse, csv
import azure.cognitiveservices.speech as speechsdk

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def tts(output_filename, text):
    voice = args.voice
    logging.info(f'Running the Azure function for {output_filename}, {text}, {voice}')
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm)

    # The language of the voice that speaks.
    # voice = 'en-AU-WilliamNeural'

    speech_config.speech_synthesis_voice_name=voice
    logging.info(f"using voice name: {voice}")

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # result = speech_synthesizer.speak_text_async("I'm excited to try text to speech").get()
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    stream = speechsdk.AudioDataStream(speech_synthesis_result)
    stream.save_to_wav_file("./" + output_filename)

def fromCSV(csvFile):
    # pathName = './csv1.csv'
    file = open(csvFile, mode='r', encoding='utf-8-sig')
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
        if row['new_content']:
            # print(row)
            output_filename = str(row['filename'])
            newContent = str(row['new_content'])
            text = newContent.replace('"', '')
            tts(output_filename, text)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--csv', help='csv filename. Be sure to escape commas in test. i.e. ","')
parser.add_argument('-v','--voice', default='en-AU-WilliamNeural', help='Azure voice to generate audio. https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/SpeechServices')
parser.add_argument('-t', '--text', type=str, help='text to record')
parser.add_argument('-o', '--output_filename', type=str, action='store', default='', help='audio filename to save')
args = parser.parse_args()
logging.info(f'Got argumants: {args}')
if args.csv:
    logging.info(f'got csv filename: {args.csv}')
    fromCSV(args.csv)
elif args.text and args.output_filename:
    tts(output_filename=args.output_filename, text=args.text)
else:
    logging.warning('Please check the arguments..')
