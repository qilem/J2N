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
	keyFile = open(keyFileName, 'r')
	key = keyFile.readlines()
	responseFile = open(responseFileName, 'r')
	response = responseFile.readlines()
	if len(key) != len(response):
		print ("length mismatch between key and submitted file")
		return 0
	correct = 0
	incorrect = 0
	keyGroupCount = 0
	keyStart = 0
	responseGroupCount = 0
	responseStart = 0
	correctGroupCount = 0
	for i in range(len(key) - 1):
		key[i] = key[i].rstrip(os.linesep)
		response[i] = response[i].rstrip(os.linesep)
		if key[i] == "":
			if response[i] == "":
				continue
			else:
				print("key string is: " + str(key[i]) + " response string is: " + str(response[i]))
				print("sentence break expected at line " + str(i))
				return 0
		keyFields = key[i].split('\t')
		if len(keyFields) != 2:
			print("format error in key at line " + str(i) + ":" + key[i])
			return 0
		keyToken = keyFields[0].strip()
		keyTag = keyFields[1]
		keyTag = keyTag.rstrip(os.linesep)
		keyTag = keyTag.strip().split('-')[0]
		responseFields = response[i].split('\t')
		responseToken = ''
		responseTag = ''
		if len(responseFields) == 2:
			responseToken = responseFields[0].strip()
			responseTag = responseFields[1]
			responseTag = responseTag.rstrip(os.linesep)
			responseTag = responseTag.strip().split('-')[0]
		if (responseToken != keyToken) or (responseTag != keyTag):
			print("Token/Tag mismatch at line " + str(i))
			print("Key string is: " + str(key[i]) + "   Response string is: " + str(response[i]))
			incorrect += 1
		else:
			correct = correct + 1
		responseEnd = responseStart != 0 and (responseTag == 'O' or responseTag == 'B')
		responseBegin = responseTag == 'B' or (responseStart == 0 and responseTag == 'I')
		keyBegin = keyTag == 'B' or (keyStart == 0 and keyTag == 'I')
		keyEnd = keyStart != 0 and (keyTag == 'O' or keyTag == 'B')
		if responseEnd:
			responseGroupCount = responseGroupCount + 1
		if keyEnd:
			keyGroupCount = keyGroupCount + 1
		if responseEnd and keyEnd and responseStart == keyStart:
			correctGroupCount = correctGroupCount + 1
		if responseBegin:
			responseStart = i
		elif responseEnd:
			responseStart = 0
		if keyBegin:
			keyStart = i
		elif keyEnd:
			keyStart = 0

	print(correct, "out of", str(correct + incorrect) + " tags correct")
	accuracy = 100.0 * correct / (correct + incorrect)
	print("  accuracy: %5.2f" % accuracy)
	print(keyGroupCount, "groups in key")
	print(responseGroupCount, "groups in response")
	print(correctGroupCount, "correct groups")
	precision = 100.0 * correctGroupCount / responseGroupCount
	recall = 100.0 * correctGroupCount / keyGroupCount
	F = (2 * precision * recall / (precision + recall)) * .10
	print("  precision: %5.2f" % precision)
	print("  recall:    %5.2f" % recall)
	print("  F1:        %5.2f" % F)
	rndf = int(round(F, 0))
	print("  rounded to: " + str(rndf))

def main(args):
	key_file = args[1]
	response_file = args[2]
	score(key_file,response_file)

if __name__ == '__main__': sys.exit(main(sys.argv))

## python score.chunk.py WSJ_24.pos-chunk response.chunk
