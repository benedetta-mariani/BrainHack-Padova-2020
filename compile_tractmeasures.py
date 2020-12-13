#!/usr/bin/env python3

import json
import subprocess
import pandas as pd
import numpy as np
import os, sys, argparse
import glob




def concatenateData(subject,tag, dire):

	#print('now',  os.getcwd())
	filelist2 = []
	for a,b,filelist in os.walk(dire):
		for filename in np.sort(filelist):
			if ".txt" in filename.lower() and filename != "report.txt" and "no_result" not in filename.lower():
				filelist2.append(filename)


	k = 0
	l = []
	for filename in filelist2:
		l.append(filename[27:-9])
		k += 1


	filelist3 = []
	for filename in filelist2:
		data1 = pd.read_csv(filename,sep='\t', names = ["0","1"])
		new = pd.DataFrame([np.array(data1["1"])], columns = np.asarray(data1["0"]))
		filelist3.append(new)
	

	data = pd.concat((filename for filename in filelist3),axis = 0,ignore_index=True, sort = False)

	
	
	data[''] = l
	data['subjectID'] = subject
	#data['sessionID'] = session
	data['tags'] = tag[0]

	columns = data.columns.tolist()

	columns = columns[-3:] +columns[:-3] 

	data = data[columns]

	return data

	
	
def main(firstdir):

	dirs = os.listdir(firstdir)
	i = 0
	for filename in dirs:
		os.chdir(firstdir)
		if "sub" in filename:
			#print(os.getcwd())
			os.chdir(filename)
			#print(os.getcwd())
			dire = os.getcwd()
			dire= os.listdir(dire)[0]
			os.chdir(dire)
			#print(os.getcwd())
			
			#print('Subject:',filename)
			
			#### load config ####
			with open('_info.json','r') as config_f:
				config = json.load(config_f)

			
			#### parse inputs ####
			subjects = config['meta']['subject'] 
			#sessions = config['meta']['session'] 
			
			tags =  config['tags'] 
		
			dire = 'tractmeasures'
		
			if os.path.isdir(dire):
				os.chdir(dire)
				#print(os.getcwd())
				
				#### run command to generate csv structures ####
				#print("concatenating tractmeasures")
				
				d = concatenateData(subjects,tags, os.getcwd())

				if i == 0:
					data = pd.DataFrame(columns = d.columns)

				data = pd.concat((data,d),axis = 0,ignore_index=True, sort = False)
				i += 1


			else:
				print('Subject not present',filename)
	#data.drop([0], inplace = True)
	os.chdir(firstdir)
	data.to_csv('./tractmeasures.tsv',sep='\t',index=False)

	"""
	to open: 
	pd.read_csv(---, index_col = 0)
	"""

firstdir = os.getcwd()
main(firstdir)

#if __name__ == '__main__':
#	main()
