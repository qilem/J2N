#!/usr/bin/python
#
# scorer for NLP class Spring 2016
# ver.1.0
#
# score a key file against a response file
# both should consist of lines of the form:   token \t tag
# sentences are separated by empty lines
#
import sys
import os

def score (keyFileName, responseFileName):
	hh=0
	hi=0
	#record=[415, 2900, 4469, 4574, 6790, 7052, 8410, 11954, 15224, 15437, 16732, 16757, 16815, 17731, 17930, 18322, 19409, 19970, 20069, 21109, 21353, 21388, 22316, 23016, 24258, 25131, 29122, 31168, 32141]
	keyFile = open(keyFileName, 'r')
	key = keyFile.readlines()
	responseFile = open(responseFileName, 'r')
	response = responseFile.readlines()
	if len(key) != len(response):
		print("length mismatch between key and submitted file")
		exit()
	correct = 0
	incorrect = 0
	for i in range(len(key)):
		key[i] = key[i].rstrip(os.linesep)
		response[i] = response[i].rstrip(os.linesep)
		if key[i] == "":
			if response[i] == "":
				continue
			else:
				print ("sentence break expected at line " + str(i))
				exit()
		keyFields = key[i].split('\t')
		if len(keyFields) != 2:
			print ("format error in key at line " + str(i) + ":" + key[i])
			exit()
		keyToken = keyFields[0]
		keyPos = keyFields[1]
		responseFields = response[i].split('\t')
		if len(responseFields) != 2:
			print ("format error at line " + str(i))
			exit()
		responseToken = responseFields[0]
		responsePos = responseFields[1]
		if responseToken != keyToken :
			print ("token mismatch at line " + str(i))
			exit()
		if responsePos == keyPos:
			correct = correct + 1
		else:
			incorrect = incorrect + 1

	print(hh)
	print (str(correct) + " out of " + str(correct + incorrect) + " tags correct")
	accuracy = 100.0 * correct / (correct + incorrect)
	print("  accuracy: %f" % accuracy)

def main(args):
	key_file = args[1]
	response_file = args[2]
	score(key_file,response_file)

if __name__ == '__main__': sys.exit(main(sys.argv))
