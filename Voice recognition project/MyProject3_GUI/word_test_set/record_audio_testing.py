import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "word_test_set/predict"

while True:
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
		        channels=CHANNELS,
		        rate=RATE,
		        input=True,
		        frames_per_buffer=CHUNK)

	print("* recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)

	print("* done recording")
	stream.stop_stream()
	stream.close()
	p.terminate()
	wf = wave.open(WAVE_OUTPUT_FILENAME + ".wav", 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
	#wait key:
	#Enter to continue recording.
	#q if want to finish.
	isContinueRecording = True
	print('Type q to finish speaking otherwise will continue speaking')
	while True:
		name = raw_input("Type: ")
		if (name == 'q'):
			isContinueRecording = False
		break
	#to exit recording
	if (isContinueRecording == False):
		break

