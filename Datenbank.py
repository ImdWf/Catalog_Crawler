# -*- coding: utf-8 -*-

import json
import time
		
from Katalog import Katalog
from Werkzeuge import Werkzeuge

from Zeitung import Zeitungen

class Zeitungsdatenbank(Katalog):
# class Zeitungsdatenbank(object):

	# def __init__(self, Startwert, Endwert, Schema=""):
	def __init__(self):
		self.Zeitungen = Zeitungen()
		# self.Katalog = Katalog()
		self.startwert_date = 0
		self.endwert_date = 0
		self.startwert = 0
		self.endwert = 0
		
		#self.re_startwert="\d+"
		super(Zeitungsdatenbank, self).__init__()
		print u"Die Datenbank wurde initialisiert."
		print u"Um die Suche nach Daten zu starten, rufen Sie die Datenbank auf und übergeben Sie einen Start und einen Endwert"
		print u"Z.B. Name der Datenbank ist die Variable db"
		print u"Starten der Suche mit db(Startwert, Endwert)"

	def addZeitungen(self,daten):
		for data in daten: self.Zeitungen.add(data)

	def save(self, name="Database.json"):
		try:
			database = self.json_dump_database()
		except:
			import pdb; pdb.set_trace()
			return 0
		else:
			with open(name,'w') as outfile:
				json.dump(database,outfile)
			return outfile.close()
	
	def load_Zeitungs_obj_from_json(self,data):
		for Zeitung_ in data:
			ort = Zeitung_['Erscheinungsort']
			name = Zeitung_['Zeitungsname']
			for Ausgabe in Zeitung_['Ausgaben']:
				datum = Ausgabe['Erscheinungsdatum']
				for Seite_obj in Ausgabe['Seiten']:
					adresse = Seite_obj['download_link']
					Seite = Seite_obj['Seitennummer']
					yield {"Erscheinungsort":ort,"Erscheinungsdatum":datum,"Zeitungsname":name,"download_link":adresse, 'Seitennummer':Seite}
					
	
	def load(self, name="Database.json"):
		werte = self.load_json_dump(name)
		for i in self.__dict__:
			if i == 'Zeitungen':
				try:
					self.addZeitungen(self.load_Zeitungs_obj_from_json(werte['Zeitungen']))
				except:
					import pdb; pdb.set_trace()
			elif i == 'Indexseiten':
				for j in werte[i]:
					self.add_index_page(j)
			else:
				try: self.load_obj_from_json(i,werte[i])
				except: print "%s konnte im Datensatz nicht gefunden werden" % i
		self.startwert_date = self.Indexseiten[self.Indexseiten.add({'Indexnummer':self.startwert})].letztes_Datum
		self.startwert_date = time.strptime(self.datum_kuerzen(self.startwert_date),self.Datum_schema)
		self.endwert_date = self.Indexseiten[self.Indexseiten.add({'Indexnummer':self.endwert})].erstes_Datum
		self.endwert_date = time.strptime(self.datum_kuerzen(self.endwert_date),self.Datum_schema)
		return True
			
	def download_files(self):
		Gesamtzahl_Zeitungen = self.Zeitungen.length()
		Gesamtzahl_Elemente = sum((self.summary()))
		i = 0
		j = 0
		k = 0
		
		for Zeitung in self.Zeitungen:
			m=0
			i+=1
			Zeitung.download_files()
			Anzahl_Ausgaben = Zeitung.Ausgaben.length()
			for Ausgabe in Zeitung.Ausgaben:
				l= 0
				j+=1
				m+=1
				Ausgabe.download_files(path='./%s/'%Zeitung.createName())
				Anzahl_Seiten = Ausgabe.Seiten.length()
				for Seite in Ausgabe.Seiten:
					l+=1
					k+=1
					print u"Lade Seite %s der %s. Ausgabe von Zeitung Nummer %s." % (l,m,i)
					print u"Gesamtfortschritt %s Prozent, %s Elemente verbleiben" %(sum((i,j,k))*100/Gesamtzahl_Elemente,Gesamtzahl_Elemente-sum((i,j,k)))
					if not(Seite.download_files(path='./%s/%s'%(Zeitung.createName(),Ausgabe.createName()))):
						print u"Fehler beim Herunterladen von Seite %s der %s. Ausgabe der Zeitung %s" % (l,m,Zeitung['Zeitungsname'])
					
	def datum_oder_index(self, Startwert, Endwert):
		if self.Datum_schema:
			try: 
				self.endwert_date = time.strptime(Endwert,self.Datum_schema)
			except:
				import pdb; pdb.set_trace()
				self.endwert = 0
				print u'There is something wrong with Endwert'
			try: self.startwert_date = time.strptime(Startwert,self.Datum_schema)
			except:
				self.startwert = 0
				print u'There is something wrong with Startwert'
			if self.startwert_date and self.endwert_date:
				self.startwert, self.endwert = self.Indexwerte_ermitteln(self.startwert_date, self.endwert_date)
		else:
			self.startwert = Startwert
			self.endwert = Endwert
		
	def get_data_from_indexpage(self, indexpage):
		links_ = indexpage['Eintraege']
		for link in links_:
			Ergebnis = {}
			for muster in self.read_re_muster():
				# import pdb; pdb.set_trace()
				Zwischen_Ergebnis = self.re_auslesen(muster[1],link)
				if Zwischen_Ergebnis:
					Ergebnis[muster[0]] = Zwischen_Ergebnis[0]
				if muster[0] == 'download_link':
					Ergebnis[muster[0]] = '%s/%s.jp2' %(self.Datenbank_Url,Ergebnis[muster[0]])
			if not(self.datum_vergleichen(Ergebnis['Erscheinungsdatum'],self.startwert_date)['Summe']>0 or self.datum_vergleichen(Ergebnis['Erscheinungsdatum'],self.endwert_date)['Summe']<0 or self.startwert > indexpage['Indexnummer'] or self.endwert < indexpage['Indexnummer']):
				yield Ergebnis
			else:
				print Ergebnis['Erscheinungsdatum']
				print indexpage['Indexnummer']
				#import pdb; pdb.set_trace()
				if not(self.datum_vergleichen(Ergebnis['Erscheinungsdatum'],self.startwert_date)['Summe']>0 or self.datum_vergleichen(Ergebnis['Erscheinungsdatum'],self.endwert_date)['Summe']<0):
					import pdb; pdb.set_trace()
			# ort =self.re_auslesen(self.re_Erscheinungsort,link)[0]
			# datum=self.datum_kuerzen(self.re_auslesen(self.re_datum,link)[0])
			# name=self.re_auslesen(self.re_name,link)[0]
			# adresse='%s/%s.jp2' %(self.Datenbank_Url, self.re_auslesen(self.re_download_link,link)[0])
			# Seite = self.re_auslesen(self.re_seite, link)[0]
			
			# if not(self.datum_vergleichen(datum,self.startwert_date)<0 or self.datum_vergleichen(datum,self.endwert_date)>0 or self.startwert > indexpage['Indexnummer'] or self.endwert < indexpage['Indexnummer']):
				# yield {"Ort":ort,"Datum":datum,"Name":name,"Download":adresse, 'Seitennummer':Seite}
	
	def getPapers(self):
		for Indexseite in self.Indexseiten:
			self.addZeitungen(self.get_data_from_indexpage(Indexseite))
			# for data in self.get_data_from_indexpage(Indexseite):
				# import pdb; pdb.set_trace()
				# self.addZeitungen(data)
				
	def summary(self):
		i= 0
		j= 0
		k= 0
		for Zeitung in self.Zeitungen:
			i+=1
			for Ausgabe in Zeitung.Ausgaben:
				j+=1
				k+= Ausgabe.Seiten.length()
		print u"Die Datenbank enthält %s verschiedene Zeitungen mit insgesamt %s Ausgaben und %s Seiten" %(i,j,k)
		return i,j,k
		
	def __call__(self, startwert, endwert):
		print 'Suche nach Start und Endwert'
		self.datum_oder_index(startwert, endwert)
		print u"Die Indexseiten werden nun ausgelesen"
		self.fill(self.startwert, self.endwert)
		self.Indexseiten.sort()
		print "Die dazugehörigen Elemente werden geladen"
		self.getPapers()
		print u"Zeitungen erstellt. Datenbankfunktion download_files startet den Download"
		
		
		
		# url = self.Katalog_index_url
		# alter_wert=self.index_from_url(url)[0]
		# for indexwert in range(self.startwert,self.endwert):
			# url = self.neue_index_url(url,self.index_steuer_string, indexwert, alter_wert)
			# daten = self.retrieveInformationsFromUrl(url)
			# self.addInformations(daten)
			# alter_wert = indexwert
			
			
