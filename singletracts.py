
import pandas as pd
import numpy as np




cases = pd.read_excel("Subjects.xlsx",sep = '\t', index_col = 0) # file with personality traits of subjects

sub = cases.index.values

df = pd.read_csv('tractmeasures.tsv',sep='\t',index_col = 0)

for tract in list(set(df.index)):
	idxs = np.where(df.index == tract)
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
	print(np.array_equal(new.index, cases2.index))
	new2 = pd.concat((new,cases2),axis = 1)
	new2.to_csv("%s.tsv" %tract, sep = '\t', index = True)
