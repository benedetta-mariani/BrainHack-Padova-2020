
import pandas as pd
import numpy as np
import os

"""
This script is designed to open an aggregated file ('tractmeasures.tsv'), obtained through the script 'compile_tractmeasures.py'.
This script takes in input that file, and returns separated files, which refer to each tract, and also concatenates to them the information regarding the personality traits.
In each file there will be the information of all the subjects as regard that tract, plus information regarding personalty traits.
The output files index is the Subjects ID.
"""

def main(xlsx, out):

	"""
	xlsx: file contanining personality traits for each subject
	out: label for the output files

	NB: modify the parameters of read_csv depending on your file (e. g. sep ='...')
	"""
	cases = pd.read_csv(xlsx, sep = ",", index_col = 0)

	sub = cases.index.values
	
	df = pd.read_csv('tractmeasures.tsv',sep='\t',index_col = 0) # aggregated file

	for tract in list(set(df.index)):
		

		idxs = np.where(df.index == tract)[0]
		
		data = pd.DataFrame(df.iloc[idxs])
		data.index = data.values[:,0]
		col = data.columns[1:]
		data = data[col]

		subs = []
		for s in np.array(sub):
			if s in data.index:
				subs.append(s)
		
		cases2 = pd.DataFrame(cases.loc[subs], index = subs)
		data["tract"] = tract
		cc = [data.columns.tolist()[-1]]+ data.columns.tolist()[:-1] 
		data = data[cc]
		new = pd.DataFrame(data.loc[subs], index = subs)
		new2 = pd.concat((new,cases2),axis = 1)
		new2.to_csv("%s %s.tsv" %(tract, out), sep = '\t', index = True)

if __name__ == "__main__":
	
	dirr = input("Type y if you are in the right directory or type the directory where you want to go ")
	if dirr != "y":
		os.chdir(dirr)
	xlsx = input("Insert input file name ")
	out = input("Insert label for output files (They will be named 'Tractname label.tsv') ")
	
	main(xlsx, out)
