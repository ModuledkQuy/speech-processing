# -*- coding: utf-8 -*-
import os
import cPickle
import numpy as np
from scipy.io.wavfile import read
from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")
import time

#libs to record user speech.
import pyaudio
import wave
import do_cmd

import Tkinter
import tkMessageBox
import subprocess
from subprocess import call #to execute command in linux.
from subprocess import Popen
import psutil

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2.5
WAVE_OUTPUT_FILENAME = "word_test_set/predict"

while True:
	#INIT MODELS
	#path to training data.
	modelpath = "word_models/"

	test_file = "word_test_set_links.txt"        

	#models from training.
	gmm_files = [os.path.join(modelpath,fname) for fname in 
		      os.listdir(modelpath) if fname.endswith('.gmm')]

	#Load the Gaussian models.
	models = [cPickle.load(open(fname,'r')) for fname in gmm_files]

	words = [fname.split("/")[-1].split(".gmm")[0] for fname 
		      in gmm_files]

	#print all available cmds.
	listw = ""
	for i in range(len(words)):
		listw += words[i] + " | "
	print listw
	#END INIT MODELS	

	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
		        channels=CHANNELS,
		        rate=RATE,
		        input=True,
		        frames_per_buffer=CHUNK)

	for i, word in enumerate(words):
		print(str(i + 1) + ". " + word)

	#START RECORDING
	print("* recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)

	print("* done recording")
	stream.stop_stream()
	stream.close()
	p.terminate()

	#recording for testing.
	wf = wave.open(WAVE_OUTPUT_FILENAME + ".wav", 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	#done saving audio.
	wf.close()
	#END RECORDING

	#START PREDICT BY USING GMM WITH TRAINED MODELs
	#read recorded audio files.
	sr,amplitude = read("word_test_set/predict.wav")
	#extract features.
	vector = extract_features(amplitude,sr)
	    
	log_likelihood = np.zeros(len(models)) 

	#checking with each model one by one.
	#a model is equivalent to a word.    
	for i in range(len(models)):
		gmm = models[i]      
		#compute probability of the vector under the models[i].   
		scores = np.array(gmm.score(vector))
		log_likelihood[i] = scores.sum()
	  	
	#LOG INFO
	print log_likelihood
	print np.amax(log_likelihood)
	#END LOG INFO

	print(1 + np.argmax(log_likelihood))
	spoken_word = ""
	if (np.amax(log_likelihood) < -11000):
		spoken_word = "unknown"
	else:
		winner = np.argmax(log_likelihood)
		spoken_word = words[winner]	

	print "\n----------------------------------\n"
	print "Spoken word: ", spoken_word
	print "\n----------------------------------\n"

	#PROCESS USER COMMAND
	if (spoken_word != 'unknown'):
		response = tkMessageBox.askquestion("Command", "Are you sure want to " + spoken_word)			
		if (response == 'yes'):
			do_cmd.doCommand(spoken_word)
	#END PROCESS USER COMMAND
	
	#WAIT KEY
	#Enter to continue speech.
	#q if want to finish.
	isContinueRecording = True
	print('Type q to finish speaking otherwise will continue speaking')
	while True:
		name = raw_input("Type: ")
		if (name == 'q'):
			isContinueRecording = False
		break
	#to exit recording.
	if (isContinueRecording == False):
		break



