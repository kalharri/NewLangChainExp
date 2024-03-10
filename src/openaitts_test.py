from RealtimeTTS import TextToAudioStream, OpenAIEngine
import os
from dotenv import load_dotenv
import threading  # Import threading for synchronization


# declare app's required API keys
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Define a callback function that will be called when playback is done
def on_playback_finished():
    playback_finished.set()  # Set the event to signal that playback is finished

def dummy_generator():
    yield "Hey guys! "
    yield "These here are "
    yield "realtime spoken words "
    yield "based on openai "
    yield "tts text synthesis."

engine = OpenAIEngine(model="tts-1", voice="nova")
stream = TextToAudioStream(engine, on_audio_stream_stop=on_playback_finished)
stream.feed(dummy_generator())

# Create an event to signal when playback is finished
playback_finished = threading.Event()

print ("Synthesizing...")
# stream.play()
stream.play_async(fast_sentence_fragment =True)

# Wait for the playback to finish
playback_finished.wait()  # This will block until the event is set by on_playback_finished