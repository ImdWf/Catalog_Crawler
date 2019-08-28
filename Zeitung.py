# -*- coding: utf-8 -*-

import os
import json

from Ausgabe import Ausgaben

class Zeitungen(Ausgaben):
	def __init__(self):
		# self.Ausgaben = Ausgaben()
		super(Ausgaben, self).__init__()
		
	
	def add(self, daten):
		i = super(Ausgaben, self).add(daten)
		self.Liste[i].Ausgaben.add(daten)
		
	
	
	class Element(Ausgaben.Element):
		def __init__(self,daten):
			self.Ausgaben = Ausgaben()
			self.Erscheinungsort = ""
			self.Zeitungsname = ""
			self.fill_values(daten)
			
		def createName(self):
			return '%s(%s)' % (self.Zeitungsname,self.Erscheinungsort)
			
	
	
	
	
	
	# def add(self,Erscheinungsdatum):
		# i=0
		# for Ausgabe_ in self.Ausgaben:
			# if Ausgabe_.Erscheinungsdatum == Erscheinungsdatum:
				# return i
			# i=+1
		# self.Ausgaben.append(Ausgabe(Erscheinungsdatum))
		# return -1
		
	# def create_folder(self, path="."):
		# if not os.path.exists('%s/%s'%(path,self.Zeitungsname)):
			# os.makedirs('%s/%s'%(path,self.Zeitungsname))
			# return 1
		# else:
			# return 0
			
	# def anzahl(self):
		# return len(self.Ausgaben)
		
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
				# except: import pdb; pdb.set_trace()
				# else: data[i] = data2
			# else:
				# data[i] = getattr(self,i)
		# return data