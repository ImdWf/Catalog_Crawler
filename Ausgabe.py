# -*- coding: utf-8 -*-

import os
import json

from Seite import Seiten
#from Zeitung import Zeitung

class Ausgaben(Seiten):
	def __init__(self):
		# self.Seiten = Seiten()
		super(Ausgaben, self).__init__()
		
	
	def add(self,daten):
		i = super(Ausgaben, self).add(daten)
		self.Liste[i].Seiten.add(daten)
	
	class Element(Seiten.Element):
		def __init__(self, daten):
			self.Seiten = Seiten()
			self.Erscheinungsdatum = ""
			self.fill_values(daten)
		
		def createName(self):
			return '%s' %self.Erscheinungsdatum
		
		def download_files(self, path="."):
			if not os.path.exists('%s/%s'%(path,self.createName())):
				os.makedirs('%s/%s'%(path,self.createName()))
				return 1
			else:
				return 0
	
	# def json_dump_database(self):
		# data = {}
		# for i in self.__dict__:
			# try:
				# json.dumps(getattr(self,i))
			# except:
				# data2 = []
				# for Element in getattr(self,i):
					# data2.append(Element.json_dump_database())
				# try: json.dumps(data2)
				# except: pass
				# else: data[i] = data2
			# else:
				# data[i] = getattr(self,i)
		# return data
		
	# def add(self, download_link, Seitennummer):
		# try: self.Pages.append(Zeitungsseite(download_link,Seitennummer))
		# except: return 0
		# else: return 1