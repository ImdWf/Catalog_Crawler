# -*- coding: utf-8 -*-

import os
import json
import urllib

class Seiten(object):
	
	def __init__(self):
		self.Liste = []
	
	def __iter__(self):
		for Eintrag in self.Liste:
			yield Eintrag
			
	def __getitem__(self,x):
		return self.Liste[x]

	def add(self,daten, Exclude = []):
		i = 0
		for Eintrag in self.Liste:
			# import pdb; pdb.set_trace()
			for Wert in Eintrag.values():
				for key in daten:
					# import pdb; pdb.set_trace()
					if Wert == daten[key] and not key in Exclude:
						return i
			i += 1
		self.Liste.append(self.Element(daten))
		return len(self.Liste)-1

	def sort(self, Kriterium = 'Seitennummer'):
		return self.Liste.sort(lambda x,y: cmp(getattr(x,Kriterium),getattr(y,Kriterium)))
		
	def length(self):
		return len(self.Liste)

	def json_dump_database(self):
		for Eintrag in Liste: yield Eintrag.json_dump_database()
		
	class Element(object):
		def __init__(self, daten):
			self.download_link = ""
			self.Seitennummer = 0
			self.fill_values(daten)
			
		def __getitem__(self,x):
			return getattr(self,x)
			
		def createName(self, Dateiendung = 'jp2'):
			return "%s.%s" % (self.Seitennummer, Dateiendung)
		
		def download_files(self,path=".", Zeitungsname="", Datum=""):
			pfad_opener = urllib.URLopener()
			if not os.path.exists("%s/%s%s%s.jp2" % (path,Zeitungsname,Datum, self.Seitennummer)):
				try: pfad_opener.retrieve(self.download_link, "%s/%s%s%s" % (path,Zeitungsname,Datum, self.createName()))
				except: 
					#import pdb; pdb.set_trace()
					print 'Fehler'
					return False
				else: return True
			else:
				return True
		
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
		
		def json_dump_database(self):
			data = {}
			for i in self.__dict__:
				try:
					json.dumps(getattr(self,i))
				except:
					data2 = []
					for Element in getattr(self,i):
						data2.append(Element.json_dump_database())
					try: json.dumps(data2)
					except: pass
					else: data[i] = data2
				else:
					data[i] = getattr(self,i)
			return data

		

		
