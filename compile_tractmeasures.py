#!/usr/bin/env python3

import json
import subprocess
import pandas as pd
import numpy as np
import os, sys, argparse
import glob


"""
This python script is designed to open tsv files downloaded from the platform Brainlife and to aggregate them in a unique tsv file.
It is specifically designed to aggregate files relative to just one tag (e. g. dti tract measures).
To be effective,your files should be organized as in the next example (which as far as I know is automatically done when downoading 
from brainlife) :
proj/sub-987074
/dt-neuro-dsistudio-tractmeasures.id-5fc365d1576e194135a9fedc/
tractmeasures/dwi.nii.gz.gqi.1.25.fib.gz.Vertical_Occipital_Fasciculus_R.stat.txt

where proj is the directory of download. The file tractmeasures should contain all the tsv (txt) files for the fibers of that subject. 
The directory that contains 'tractmeasures', should also contain a json file, here called '_info.json'.

The output file is called 'tractmeasures.tsv'. To read it, just type pd.read_csv('tractmeasures.tsv', index_col = 0).
The index of this file is composed by the tract names, while the columns are the Subjects ID and the dti tractmeasures.

To obtain files relative to the single tracts, see the script "singletracts.py"
"""

def concatenateData(subject,tag, dire):

	
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
			
			os.chdir(filename)
		
			dire = os.getcwd()
			dire= os.listdir(dire)[0]
			os.chdir(dire)
		
			with open('_info.json','r') as config_f:
				config = json.load(config_f)

			
			subjects = config['meta']['subject'] 
			
			tags =  config['tags'] 
		
			dire = 'tractmeasures'
		
			if os.path.isdir(dire):
				os.chdir(dire)
				
				
				d = concatenateData(subjects,tags, os.getcwd())

				if i == 0:
					data = pd.DataFrame(columns = d.columns)

				data = pd.concat((data,d),axis = 0,ignore_index=True, sort = False)
				i += 1


			else:
				print('Subject not present',filename)

	os.chdir(firstdir)
	data.to_csv('./tractmeasures.tsv',sep='\t',index=False)

	"""
	to open: 
	pd.read_csv(---, index_col = 0)
	"""

firstdir = os.getcwd()
main(firstdir)

