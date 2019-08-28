# -*- coding: utf-8 -*-
import time

from Werkzeuge import Werkzeuge
from Index import Indexseiten

class Katalog(Werkzeuge):

	def __init__(self):
		# self.Datenbank_Url = Datenbank_Url
		# self.Katalog_index_url = Index_Url
		# self.index_steuer_string = Index_Steuer_String
		# self.teiler = teiler
		self.Datenbank_Url = ""
		self.Katalog_index_Url = ""
		self.index_steuer_string = ""
		self.teiler = ""
		self.Datum_schema = ""
		self.Indexseiten = Indexseiten()
		super(Katalog, self).__init__()

	def fill(self, startwert, endwert):
		index_url = ''
		for indexwert in range(startwert, endwert):
			index_url = self.neue_index_url(indexwert)
			self.fill_index_page(self.add_index_page({'url':index_url,'Indexnummer':indexwert}))
		
		
	def add_index_page(self, data):
		return self.Indexseiten.add(data)
	
	def fill_index_page(self, identifier = -1):
		Eintraege = []
		link_liste = self.link_liste_auslesen(self.Indexseiten[identifier].values('html_source'))
		for link in self.links(link_liste):
			Eintraege.append(link)
		Daten = {'Eintraege':Eintraege,
		'erstes_Datum': self.html_objekt_durchsuchen(Eintraege[0],'Erscheinungsdatum'),
		'letztes_Datum': self.html_objekt_durchsuchen(Eintraege[-1],'Erscheinungsdatum')}
		self.Indexseiten[identifier].fill_values(Daten)


	def datum_vergleichen(self, datum1, datum2 , vz = False):
		datum = [datum1, datum2]
		erg = []
		# import pdb; pdb.set_trace()
		if self.Datum_schema:
			for date in datum:
				try: 
					# import pdb; pdb.set_trace()
					erg.append(time.strptime(self.datum_kuerzen(date), self.Datum_schema))
				except: 
					print u'%s liegt bereits im time Format vor oder das Schema %s ist nicht anwendbar'%(date,self.Datum_schema)
					if date =="":
						import pdb; pdb.set_trace()
					erg.append(date)
			if vz:
				return super(Katalog, self).datum_vergleichen(erg[0], erg[1])
			else:
				# import pdb; pdb.set_trace()
				return self.datum_vergleichen_time_obj(erg[0], erg[1])
		else:
			print u'Kein Schema angegegeben. Für eine genauere Analyse bitte das Schema angeben!'
			return super(Katalog, self).datum_vergleichen(datum[0], datum[1])

	def index_from_url(self,index_url):
		return self.re_auslesen(self.read_re_muster('Indexnummer'),index_url)[0]

	def multiplikator1(self, datum, datum_index_1, datum_index_2):
		# import pdb; pdb.set_trace()
		index_schwankung = self.datum_vergleichen(datum_index_1,datum_index_2)['Summe']/2
		return self.datum_vergleichen(datum_index_1, datum)['Summe'] + index_schwankung
		
	def multiplikator2(self, i_dat):
		erg = 0
		for i in [1,-1]:
			i_dat_schleife = int(i_dat)
			i_kat_schleife = int(self.Indexseiten.add({'Indexnummer':i_dat}))
			datum1, datum2 = self.Indexseiten[i_kat_schleife].Zeitraum()
			while self.datum_vergleichen(datum1, datum2, True) == 0:
				i_dat_schleife= i_dat_schleife + i
				url = self.neue_index_url(i_dat_schleife)
				i_kat_schleife = self.add_index_page({'url':url,'Indexnummer':i_dat_schleife})
				self.fill_index_page(i_kat_schleife)
				datum1, datum2 = self.Indexseiten[i_kat_schleife].Zeitraum()
				print i_dat_schleife
				erg+=1
		return erg
	
	
	# def suche(self, gesuchtes_datum, indexwert, Multiplikator1, Vorzeichen):
	def suche(self, gesuchtes_datum, indexwert, Vorzeichen):
		Nummer_Indexseite = self.Indexseiten.add({'url':self.neue_index_url(indexwert),'Indexnummer':indexwert})
		self.fill_index_page(Nummer_Indexseite)
		# import pdb; pdb.set_trace()
		# Multiplikator1 = self.multiplikator1(gesuchtes_datum,self.Indexseiten[Nummer_Indexseite].Zeitraum()[0],self.Indexseiten[Nummer_Indexseite].Zeitraum()[1])
		Zeitraum = self.Indexseiten[Nummer_Indexseite].Zeitraum()
		# import pdb; pdb.set_trace()
		if indexwert <= 0:  # or Schleifendauer > Multiplikator2*10
			return -1
		elif self.datum_vergleichen(gesuchtes_datum,Zeitraum[0])['Summe'] <=0 and self.datum_vergleichen(gesuchtes_datum,Zeitraum[1])['Summe'] >= 0:
			index_return = indexwert
			indexwert += (1*Vorzeichen)
			indexwert_feinsuche = self.suche(gesuchtes_datum,indexwert , Vorzeichen)
			#import pdb; pdb.set_trace()
			if indexwert_feinsuche:
				return indexwert_feinsuche
			else:
				return index_return
		else: return 0
	
	def Indexwerte_ermitteln(self, datum_start, datum_ende):
		Index_start = 0
		Index_ende = 0
		Vorzeichen = -1
		index_url = self.values('Katalog_index_Url')
		indexwert = int(self.index_from_url(index_url))
		Zeitraum = [datum_start,datum_ende]
		self.fill_index_page(self.add_index_page({'url':index_url,'Indexnummer':indexwert}))
		multiplikator2_start = self.multiplikator2(indexwert)
		for Zeit in Zeitraum:
			# Multiplikator1 = self.multiplikator1(Zeit, self.Indexseiten[i].Zeitraum()[0],self.Indexseiten[i].Zeitraum()[1])
			multiplikator1_alt = 0
			multiplikator2 = multiplikator2_start
			suchergebnis = self.suche(Zeit,indexwert, Vorzeichen)
			while not suchergebnis:
				Nummer_Indexseite = self.add_index_page({'Indexnummer':indexwert})
				Multiplikator1 = self.multiplikator1(Zeit,self.Indexseiten[Nummer_Indexseite].Zeitraum()[0],self.Indexseiten[Nummer_Indexseite].Zeitraum()[1])
				#import pdb; pdb.set_trace()
				print Multiplikator1
				if Multiplikator1:
					if multiplikator1_alt and abs(multiplikator1_alt)<abs(Multiplikator1):
						# indexwert += self.Vorzeichen(Multiplikator1)*multiplikator1_alt
						multiplikator2/=2
					indexwert += Multiplikator1*multiplikator2
					if multiplikator1_alt / Multiplikator1 == -1 and not multiplikator1_alt % Multiplikator1:
							indexwert += (1*Vorzeichen)
				else:
					indexwert +=(1*Vorzeichen)
				if indexwert <= 0:
					indexwert = 1
				print indexwert
				multiplikator1_alt = Multiplikator1
				suchergebnis = self.suche(Zeit,indexwert, Vorzeichen)
			if suchergebnis < 0:
				print "Fehler"
			if Index_start:
				Index_ende = suchergebnis
			else:
				Index_start = suchergebnis
				Vorzeichen = 1
		return Index_start, Index_ende

	def link_liste_auslesen(self, index_page_source):
		return self.re_auslesen(self.read_re_muster('link_liste'), index_page_source)

	def links(self, html_link_liste):
		#import pdb;pdb.set_trace()
		return self.re_auslesen(self.read_re_muster('Eintraege'), html_link_liste[0])
		
	

	# def neue_index_url(self,index_url_alt, neuer_wert, alter_wert):
		# '''def neue_index_url(self,index_url_alt, steuerstring, neuer_wert, alter_wert)'''
		# try: steuerstring_teile = self.index_steuer_string.split(teiler)
		# except: return False
		# return index_url_alt.replace('%s=%s'%(steuerstring_teile[0],alter_wert),'%s=%s' %(steuerstring_teile[0],neuer_wert))

	def neue_index_url(self, neuer_wert):
		'''def neue_index_url(self,index_url_alt, steuerstring, neuer_wert, alter_wert)'''
		try: steuerstring_teile = self.index_steuer_string.split(self.teiler)
		except: 
			import pdb; pdb.set_trace()
			return False
		return self.Katalog_index_Url.replace('%s'%self.index_steuer_string,'%s=%s' %(steuerstring_teile[0],neuer_wert))

	def retrieveInformationsFromUrl(self, index_url):
		return self.links_auswerten(self.link_liste_auslesen(self.html_source(index_url)))
		
