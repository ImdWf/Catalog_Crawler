# -*- coding: utf-8 -*-
import urllib
from Seite import Seiten

class Indexseiten(Seiten):
	def add(self, data):
		Exclude = ['erstes_Datum','letztes_Datum']
		return super(Indexseiten, self).add(data,Exclude)
	
	def sort(self, Kriterium = 'Indexnummer'):
		super(Indexseiten, self).sort(Kriterium)
		
	class Element(Seiten.Element):
		def __init__(self, daten):
			self.Eintraege = []
			self.erstes_Datum = ""
			self.letztes_Datum = ""
			self.Indexnummer = 0
			self.url = ""
			# import pdb; pdb.set_trace()
			self.fill_values(daten)
			self.set_html_source()
		
		def set_html_source(self):
			if self.url:
				seite = urllib.urlopen(self.url)
				self.html_source = seite.read()
			else:
				self.html_source = ''
		
		def Zeitraum(self):
			return self.erstes_Datum, self.letztes_Datum
		# def set_eintraege(self, Eintraege):
			# for eintrag in Eintraege:
				# self.Eintraege.append(eintrag)
				
		# def set_erstes_Datum(self, datum):
			# self.erstes_Datum = datum
			
		# def set_letztes_Datum(self, datum):
			# self.letztes_Datum = datum
			
		# def set_Indexnummer(self, nummer):
			# self.Indexnummer = nummer
		# def get_Eintraege(self):
			# return self.Eintraege
		
		# def get_Eintraege_iter(self):
			# for eintrag in self.Eintrage:
				# yield eintrag
		
		# def get_erstes_Datum(self):
			# return self.erstes_Datum
		
		# def get_letztes_Datum(self):
			# return self.letztes_Datum
		
		# def get_Indexnummer(self):
			# return self.Indexnummer
			
		# def get_html_source(self):
			# return self.html_source
	
	