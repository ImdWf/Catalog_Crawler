# -*- coding: utf-8 -*-

import re
import os
import json

class Werkzeuge(object):
	
	def __init__(self):
		self.re_muster = {}
		
	def fill_re_muster(self, daten):
		for i in daten.keys():
			if 're_' in i:
				self.re_muster[i.split('_',1)[1]] = daten[i]
	
	def read_re_muster(self, x =""):
		if x: 
			return self.re_muster[x]
		else:
			return self.read_re_muster_iter()

	def read_re_muster_iter(self):
		for i in self.re_muster:
				yield [i,self.read_re_muster(i)]

	def re_auslesen(self, re_such_string, re_untersuchter_string , matches_all = True):
		if matches_all:
			re_suche = re.compile(re_such_string, flags=re.S)
		else:
			re_suche = re.compile(re_such_string)
		re_auslesen_ergebnis = re.findall(re_suche, re_untersuchter_string)
		return re_auslesen_ergebnis
	
	def html_objekt_durchsuchen(self, html_source , x = ""):
		if x:
			re_muster = self.read_re_muster(x)
			return self.re_auslesen(re_muster, html_source)[0]
		else:
			return html_objekt_durchsuchen_iter(html_source)
			
	def html_objekt_durchsuchen_iter(self, html_source):
		try:
			for re_muster in self.read_re_muster(x):
				yield {re_muster[0]:self.re_auslesen(re_muster[1], html_source)[0]}
		except: import pdb; pdb.set_trace()
	
	def Vorzeichen(self, wert):
		if wert >= 0:
			return 1
		else:
			return -1

	def datum_vergleichen(self, datum1, datum2):
		if datum1 < datum2:
			return -1
		elif datum1 > datum2:
			return 1
		else:
			return 0
			
	def datum_vergleichen_time_obj(self, datum1, datum2):
		erg = {}
		erg['Jahr'] = (datum2.tm_year - datum1.tm_year)*365
		# erg['Monat'] = (datum2.tm_mon - datum1.tm_mon)*10
		# erg['Tag'] = datum2.tm_mday - datum1.tm_mday
		erg['Tag'] = datum2.tm_yday - datum1.tm_yday
		# erg['Summe'] = erg['Jahr'] + erg['Monat'] + erg['Tag']
		erg['Summe'] = erg['Jahr'] + erg['Tag']
		return erg

	def datum_kuerzen(self,datum, laenge = 3, re_suchstring = '\w+'):
		'''datum_kuerzen(self,datum, laenge = 3, re_suchstring = '\w+')
		Verkuerzt den gesuchten String auf die vorgebene Laenge, damit die Stringkette mit time.strptime des Module time kompatibel ist'''
		Monat = self.re_auslesen(re_suchstring,datum)[0]
		if len(Monat)>laenge:
			datum = datum.replace(Monat,Monat[:laenge])
		return datum
	
	def json_dump_database(self):
		database = {}
		for i in self.__dict__:
			try:
				json.dumps(getattr(self,i))
			except:
				# import pdb; pdb.set_trace()
				data = []
				try: 
					for Element in getattr(self,i):
						data.append(Element.json_dump_database())
					database[i] = data
				except: import pdb; pdb.set_trace()
			else:
				database[i] = getattr(self,i)
		return database
		
	def load_json_dump(self,file_name="Database.json"):
		with open(file_name,'r') as infile:
			try: data = json.load(infile)
			except: import pdb; pdb.set_trace()
			infile.close()
		return data
		
	def load_obj_from_json(self, merkmal, wert):
		try:
			setattr(self,merkmal,wert)
			return True
		except:
			import pdb; pdb.set_trace()
			return False
			
	def values(self, x = ''):
		if x: 
			return getattr(self,x)
		else:
			return self.values_iter()
	
	def values_iter(self):
		for Element_ in self.__dict__:
			yield getattr(self, Element_)
	
	def fill_values(self,daten, x=''):
		if x: setattr(self,x,daten[x])
		else:
			for variable in self.__dict__:
				try: setattr(self,variable,daten[variable])
				except: u'%s im Datensatz nicht enthalten!' %variable