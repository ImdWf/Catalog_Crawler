# -*- coding: utf-8 -*-

from Datenbank import Zeitungsdatenbank

print u"Modul chronam geladen"
print u"Initialisieren Sie bitte die Datenbank über Variable = chronam.Chronam()"

class Chronam(Zeitungsdatenbank):
	#Für 'https://chroniclingamerica.loc.gov':
	daten_init = {
	'Datenbank_Url' : 'https://chroniclingamerica.loc.gov',
	'Katalog_index_Url' : 'https://chroniclingamerica.loc.gov/search/pages/results/list/?date1=1863&date2=1863&language=&sequence=&lccn=&state=&rows=20&ortext=&proxtext=&year=&phrasetext=&andtext=&proxValue=&dateFilterType=yearRange&page=1149&sort=date',
	'index_steuer_string' : 'page=1149',
	'teiler' : '=',
	'Datum_schema':'%b %d, %Y'}
	re_muster_init = {
	're_link_liste': '<ul class="results_list">.*?<\/ul>',
	're_Eintraege' : '<li>.*?<\/li>',
	're_download_link': '\"\/(.*?)\/;',
	're_Erscheinungsdatum': "(\w*? \d+, \d\d\d\d)",
	're_Zeitungsname': "<strong>(.*?)<\/strong>",
	're_Erscheinungsort': '\((.*?)\)',
	're_Seitennummer': "Image (\d+)",
	're_Indexnummer': '%s\=(\d+)' %daten_init['index_steuer_string'].split(daten_init['teiler'])[0]}
	
	
	def __init__(self, daten_init = daten_init, re_muster_init = re_muster_init):
		super(Chronam, self).__init__()
		print u"Die Anfangswerte für Chronic America werden geladen"
		self.fill_values(daten_init)
		self.fill_re_muster(re_muster_init)
		print u"Die Datenbank zur Abfrage der Chronic America ist bereit"
	