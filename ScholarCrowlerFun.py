from bs4 import BeautifulSoup
import requests
from selenium import webdriver  #use selenium
import time
import sys
import random as r
import json
import codecs
from read import *

def MyCrowler(configFile,outFile):

	SEARCH_LINK = configFile[0] # ioannidis

	try:
		NUM_OF_COLLECTED_DATA = int(configFile[1])
	except:
		NUM_OF_COLLECTED_DATA = 100 

	try:
		CLICK_MORE_BUTTON = int(configFile[2])
	except:
		CLICK_MORE_BUTTON = 10

	try:
		PRINT_HTML = int(configFile[3])  
	except:
		PRINT_HTML = 0  #1:true 0:false

	LAB = configFile[4]
	LAB_LINK = configFile[5]
	LAB_SHORT_NAME = configFile[6]

	print ("Parametroi configFile: ",configFile)

	"""
	# Paradigma xriseis metavlitwn #
	SEARCH_LINK = 'https://scholar.google.com/citations?hl=el&user=MIfpzUQAAAAJ' # ioannidis
	NUM_OF_COLLECTED_DATA = 1000 # 100
	CLICK_MORE_BUTTON = 5  # 10
	PRINT_HTML = 0  #1:true 0:false
	LAB = "Εργαστήριο Διαχείρισης Δεδομένων, Πληροφορίας και Γνώσης"
	LAB_LINK = "http://www.madgik.di.uoa.gr"
	LAB_SHORT_NAME = "MADGIK"
	"""
	#print("%%%%%%%%%%%%%%%%%--- Scholar Crowler ---%%%%%%%%%%%%%%%%%")
	#print

	data = {}
	driver = webdriver.Chrome('C:\\Users\\p1a2n\\AppData\\Local\\Programs\\Python\\Python37-32\\drivers\\chromedriver.exe')

	#driver.get('https://scholar.google.com/citations?hl=el&user=IaPXgqsAAAAJ')  # roussou
	#driver.get('https://scholar.google.com/citations?hl=el&user=MIfpzUQAAAAJ')  #ioanidis
	#driver.get('https://scholar.google.com/citations?user=9Q8pE2YAAAAJ&hl=el&oi=ao')   #liges dimosiefseis

	driver.get(SEARCH_LINK)
	time.sleep(2+r.random())

	author = driver.find_elements_by_id('gsc_prf_in') # Pernei to author's name gia to json arxeio.
	#print (author[0].text)
	author = author[0].text
	#author = ''.join([x for x in author if ord(x) < 127])
	data[ author ] = []

	#outFile.write('###\n')
	#outFile.write('%s\n' % author)
	#outFile.write('%s\n' % SEARCH_LINK)
	#outFile.write('###\n')
	#outFile.write('\n')
	#####################################################################################################
	#####################################################################################################
	#####################################################################################################
	outFile.write('\n#\n') #xaraktiras diaxorismoy, voithaei sto parse argotera.
	more = CLICK_MORE_BUTTON
	for i in range(more):
		submit_button=driver.find_element_by_id('gsc_bpf_more')
		submit_button.click()
		time.sleep(0.5+r.random())


	time.sleep(1+r.random())

	res = driver.execute_script("return document.documentElement.outerHTML") # Travaei olo to html apo ton browser

	#####################################################################################################

	soup = BeautifulSoup(res, 'lxml')

	papersList = soup.find_all('a', {'class':'gsc_a_at'}) # Pare ta onomata twn apotelesmatwn.
	years = soup.find_all('span', {'class':'gsc_a_h gsc_a_hc gs_ibl'}) # Pare tis xronologies dimosieysis twn apotelesmatwn.

	lol = 1
	#print (papersList[lol+2].text)   # ---$---> enalaktiki pigi gia ton titlo kai thn xronologia dimosiefsis.
	#print (years[lol].text)

	#for i in range(len(papersList)):
		#print(papersList[i].text)
		#print(years[i].text)
		#print ('\n')

	#print (len(papersList))
	 
	#####################################################################################################
	#####################################################################################################
	#####################################################################################################

	id_count = 1   # To id arxizei apo 1
	links = driver.find_elements_by_class_name('gsc_a_at')
	#print("Anigma ",len(links)," links...")
	print('[')
	outFile.write('[\n')
	#times = len(links)
	times = NUM_OF_COLLECTED_DATA
	for i in range( times ):
		try:
			links[i].click() # Anigei ta apotelesmata dimosiefsewn pou vgazei to Scholar.
		except:
			break; # Otan teliosoyn ta apotelesmata kane break apo to for loop.

		time.sleep( 2+r.random() )

		res = driver.execute_script("return document.documentElement.outerHTML")
		soup = BeautifulSoup(res, 'lxml')

		print('{')
		outFile.write('{\n')
		if(PRINT_HTML == 1):
			try:
				html = soup.select('form#gsc_vcd_form')[0]
				#html = ''.join([x for x in html if ord(x) < 127])
				print("\'html\': \'",html,"\',")
				outFile.write("\'html\': \'%s\',\n" % html)
			except:
				html = soup.select('form#gsc_vcd_form')[0].encode('utf8')
				print("\'html\': \'",html,"\',")
				outFile.write("\'html\': \'%s\',\n" % html)

		try:
			link = soup.select('div.gsc_vcd_title_ggi a')[0].get('href')
			#link = ''.join([x for x in link if ord(x) < 127])
			print('\"link\": \"',link,'\",')
			outFile.write('\"link\": \"%s\",\n' % sanitiseData(link))
		except:
			print('\"link\": \"Link unavailable.\",')
			outFile.write('\"link\": \"Link unavailable.\",\n')

		try:
			title = soup.select('a.gsc_vcd_title_link')[0].text
			#title = ''.join([x for x in title if ord(x) < 127])
			print('\"title\": \"',title,'\",')
			outFile.write('\"title\": \"%s\",\n' % sanitiseData(title))
		except:
			try:
				print('\"title\": \"',papersList[i].text,'\",') # Enalaktikos tropos na parw ton titlo.
				outFile.write('\"title\": \"%s\",\n' % sanitiseData(papersList[i].text))
			except:
				print('\"title\": \"TitleLink unavailable.\",') # Minima lathous.
				outFile.write('\"title\": \"TitleLink unavailable.\",\n')

		print('\"year\": \"',years[i].text,'\",')  # Ftiaksimo enos pediou mono me to etos dimosiefsis kai oxi tin pliri imerominia.
		outFile.write('\"year\": \"%s\",\n' % sanitiseData(years[i].text))

		print('\"lab\": \"',LAB,'\",')  # Ftiaksimo enos pediou mono me to etos dimosiefsis kai oxi tin pliri imerominia.
		outFile.write('\"lab\": \"%s\",\n' % sanitiseData(LAB))

		print('\"labLink\": \"',LAB_LINK,'\",')  # Ftiaksimo enos pediou mono me to etos dimosiefsis kai oxi tin pliri imerominia.
		outFile.write('\"labLink\": \"%s\",\n' % sanitiseData(LAB_LINK))

		print('\"labShortName\": \"',LAB_SHORT_NAME,'\",')  # Ftiaksimo enos pediou mono me to etos dimosiefsis kai oxi tin pliri imerominia.
		outFile.write('\"labShortName\": \"%s\",\n' % sanitiseData(LAB_SHORT_NAME))


		n = len(soup.select('div.gsc_vcd_field'))
		fields = []
		values = []
		for line in range(n):

			fields.append( soup.select('div.gsc_vcd_field')[line].text )
			if(fields[line] ==  "ʼρθρα στον Μελετητή" ):
				fields[line] = "Aρθρα στον Μελετητή"

			if(fields[line] == "Σύνολο παραθέσεων"):
				values.append( soup.select('div.gsc_vcd_value > div > a')[0].text )
			else:
				values.append( soup.select('div.gsc_vcd_value')[line].text )


		
		for k in range(n):
			try:
				#fields[k]  = ''.join([x for x in fields[k]  if ord(x) < 127])
				#values[k]  = ''.join([x for x in values[k]  if ord(x) < 127])
				if(fields[k] == "Περιγραφή"):
					print('\"',fields[k],'\": \"',values[k],'\",')
					outFile.write('\"%s\": \"%s\",\n' % (sanitiseData(fields[k]), sanitiseData2(values[k])) )
				else:
					print('\"',fields[k],'\": \"',values[k],'\",')
					outFile.write('\"%s\": \"%s\",\n' % (sanitiseData(fields[k]), sanitiseData(values[k])) )
			except:
				if(fields[k] == "Περιγραφή"):
					print('\"',fields[k],'\": \"',values[k].encode('utf8'),'\",')
					outFile.write('\"%s\": \"%s\",\n' %(sanitiseData(fields[k]), sanitiseData2(values[k].encode('utf8'))) )
				else:
					print('\"',fields[k],'\": \"',values[k].encode('utf8'),'\",')
					outFile.write('\"%s\": \"%s\",\n' %(sanitiseData(fields[k]), sanitiseData(values[k].encode('utf8'))) )


		print('\"dit_author\": \"',author,'\",')
		outFile.write('\"dit_author\": \"%s\",\n' % sanitiseData(author))

		print('\"data_from\": \"',SEARCH_LINK,'\",')
		outFile.write('\"data_from\": \"%s\",\n' % sanitiseData(SEARCH_LINK))

		print('\"local_id\": \"',id_count,'\"')
		outFile.write('\"local_id\": \"%s\"\n' % id_count)
		id_count = id_count + 1
		
		if( times < len(years) ):
			loops = times
		else:
			loops = len(years)

		if (i == (loops-1) ): # An einai h teleftea epanalipsi...years
			print('}') # min valeis koma
			outFile.write('}\n')
		else:
			print('},')
			outFile.write('},\n')
			
		print()
		outFile.write('\n')

		try:
			# Klisimo tou parathiorou
			exit_ = driver.find_elements_by_id('gs_md_cita-d-x')
			exit_[0].click() # pataei to 'X' apo to pop-up parathiro pou emfanozete gia na girisei stin basiki selida.
			time.sleep(0.5+r.random())  
		except:
			time.sleep(r.random())

	print(']')
	outFile.write(']\n')

	driver.quit()
	#sys.exit()








