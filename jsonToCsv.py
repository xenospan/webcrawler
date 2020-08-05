import csv
import json
import codecs
import pandas as pd
import sys



if(len(sys.argv)<=1):
	sys.exit()

fileName = sys.argv[1]
f = codecs.open(fileName, "r", "utf-8-sig") 

strs = f.read();
x = strs.split("#"); #Diaxorizei tadiaforetika arxeia json pou yparxoun mesa sto arxeio eisodou.
lebels = []
num_of_recs = 0
for i in range(1,len(x)):                      # Gia kathe json file
	#print(x[i])

	recs = json.loads(x[i])

	#print( "Engrafes poy periexonde:", len(y) )

	for k in range(len(recs)):                  # Gia kathe engrafi
		keys = list(recs[k].keys())
		num_of_recs=num_of_recs+1
		for j in range(len(keys)):              # Gia kathe label engrafis
			if( not (keys[j] in lebels) ):
				lebels.append( keys[j] )


lebels.append( "type")
print ("lebels: ",lebels)
print ("len(lebels): ",len(lebels))
print("num_of_recs: ",num_of_recs)


#sys.exit()
count_recs = 0
d = {} # ftiakse ena dictionary keno
#d = {'col1': [1, 2], 'col2': [3, 4]}
for lebel in lebels:
	d[lebel] = [] #ftiakse tis stiles kai ta onomata tous

###########################################################################

for i in range(1,len(x)):                      # Gia kathe json file.
	recs = json.loads(x[i])
	
	for k in range(len(recs)):                 # Gia kathe engrafi.

		for leb in lebels:					   # Gia ola ta labels.
			#print(leb,"-->")
			#print( recs[k][leb] )
			try:
				d[leb].append(recs[k][leb])
			except:
				d[leb].append(" ")				# Ti xaraktira na vazei otan mia timi den yparxei. <--$ 

		# Gia kathe engafi enenkse ola ta klidia gia na breis to type tis enagrafis.
		keys = list(recs[k].keys())
		for key in keys:
			if(key == "Επιστημονικό άρθρο"):
				d["type"][count_recs] = key
				break;
			elif(key == "Διάσκεψη"):
				d["type"][count_recs] = key
				break;
			elif(key == "Βιβλίο"):
				d["type"][count_recs] = key
				break;
			elif(key == "Αριθμός αναφοράς"):
				d["type"][count_recs] = "Αναφορά"
				break;
			elif(key == "Αριθμός ευρεσιτεχνίας"):
				d["type"][count_recs] = "Ευρεσιτεχνία"
				break;
			elif(d["type"][count_recs]==" "):
				d["type"][count_recs] = "Διάφορα"


		count_recs = count_recs + 1
			
				


#print (d)

#sys.exit()

df = pd.DataFrame(data=d)
#print(df)


fileNameOut = fileName.split(".")
fileNameOut = fileNameOut[0]+".csv"
print ("Output file: ",fileNameOut)

df.to_csv(fileNameOut,sep='#')

f.close();

