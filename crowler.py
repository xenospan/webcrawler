from ScholarCrowlerFun import *

print("########################################################################")
print("########################--- Scholar Crowler ---########################")
print("######################################################################")
print()
print()

if( len(sys.argv) > 2 ):

	#print("Orismata termatikou:",sys.argv)

	#f = open(sys.argv[1], "w")  # palia ekdosi diavasmatos den ipostirize non-ascii xaraktires.
	f = codecs.open(sys.argv[1], "w", "utf-8-sig")  # "a" gia na kanei append!
	
	for i in range(2,len(sys.argv)):
		print ("Anigma arxeiou: ",sys.argv[i])

		links = ReadFile(sys.argv[i])
		MyCrowler(links,f)

		print ()
else:
	print("Prepei na doseis san orismata prwta to outFile kai meta ta configFiles...")

f.close()
sys.exit()