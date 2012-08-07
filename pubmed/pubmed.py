#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys, os
from httpclient import HttpClient
from htmlparser import between

unrecognized_authors = {
			'Mller'		: 'Mueller',
			'Schfer'	: 'Schaefer',
			'Msch'		: 'Moesch',
			'Grner'		: 'Goerner',
			'Martnez'	: 'Martinez',
			'Martnez-Pastor': 'Martinez-Pastor',
			'Vzina'		: 'Vezina'
			}

def downloadCitation(ID):
	browser = HttpClient()
	browser.GET('http://www.ncbi.nlm.nih.gov/pubmed/'+ID)

	q = {}
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_SearchBar.SearchResourceList'] = 'pubmed'
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_SearchBar.Term'] = ''
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_SearchBar.CurrDb'] = 'pubmed'
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_PageController.PreviousPageName'] = 'results'
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sPresentation'] = 'xml'
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FFormat'] = 'abstract'
	q['email_format'] = 'abstract'
	q['email_address'] = ''
	q['email_subj'] = '1+selected+item%3A+'+ID+'+-+PubMed'
	q['email_add_text'] = ''
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FileFormat'] = 'abstract'
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastPresentation'] = 'abstract'
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.Presentation'] = 'xml'
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.PageSize'] = '20'
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastPageSize'] = '20'
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.Sort'] = ''
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastSort'] = ''
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FileSort'] = ''
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.Format'] = 'text'
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastFormat'] = ''
	q['CitationManagerStartIndex'] = '1'
	q['CitationManagerCustomRange'] = 'false'
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_ResultsController.ResultCount'] = '1'
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_ResultsController.RunLastQuery'] = ''
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.HistoryDisplay.Cmd'] = 'displaychanged'
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailReport'] = ''
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailFormat'] = ''
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailCount'] = ''
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailStart'] = ''
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailSort'] = ''
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.Email'] = ''
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailSubject'] = ''
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailText'] = ''
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailQueryKey'] = ''
	q['EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.QueryDescription'] = ''
	q['EntrezSystem2.PEntrez.DbConnector.Db'] = 'pubmed'
	q['EntrezSystem2.PEntrez.DbConnector.LastDb'] = 'pubmed'
	q['EntrezSystem2.PEntrez.DbConnector.Term'] = ''
	q['EntrezSystem2.PEntrez.DbConnector.LastTabCmd'] = ''
	q['EntrezSystem2.PEntrez.DbConnector.LastQueryKey'] = '1'
	q['EntrezSystem2.PEntrez.DbConnector.IdsFromResult'] = ''
	q['EntrezSystem2.PEntrez.DbConnector.LastIdsFromResult'] = ''
	q['EntrezSystem2.PEntrez.DbConnector.LinkName'] = ''
	q['EntrezSystem2.PEntrez.DbConnector.LinkReadableName'] = ''
	q['EntrezSystem2.PEntrez.DbConnector.LinkSrcDb'] = ''
	q['EntrezSystem2.PEntrez.DbConnector.Cmd'] = 'displaychanged'
	q['EntrezSystem2.PEntrez.DbConnector.TabCmd'] = ''
	q['EntrezSystem2.PEntrez.DbConnector.QueryKey'] = ''
	q['p%24a'] = 'EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.SetDisplay'
	q['p%24l'] = 'EntrezSystem2'
	q['p%24st'] = 'pubmed'

	browser.POST('http://www.ncbi.nlm.nih.gov/pubmed', q, {'Accept': 'application/xml'})

	xml = between(browser.Page, '<pre>', '</pre>').replace('&lt;', '<').replace('&gt;', '>').strip()
	return xml

def parseXML(xml):
	authors = []
	skip = 1
	a = between(xml, '<LastName>', '</LastName>', skip)
	while a != '':
		if a in unrecognized_authors.keys():
			print 'Warning: changing problematic author name '+a+' to '+unrecognized_authors[a]
			a = unrecognized_authors[a]
		authors.append(a.replace(' ','').replace('-',''))
		skip += 1
		a = between(xml, '<LastName>', '</LastName>', skip)

	title = between(xml, '<ArticleTitle>', '</ArticleTitle>').strip('\t .')

	journal = between(xml, '<ISOAbbreviation>', '</ISOAbbreviation>')

	year = between(between(xml, '<PubDate>', '</PubDate>'), '<Year>', '</Year>')

	doi = between(xml, '<ArticleId IdType="doi">', '</ArticleId>')

	url = 'http://www.ncbi.nlm.nih.gov/pubmed/'+ID

	bibtex  = '@article{'+authors[0]+year+',\n'
	bibtex += '\ttitle = "'+title+'",\n'
	bibtex += '\tauthor = "{'+'} and {'.join(authors)+'}",\n'
	bibtex += '\tjournal = "'+journal+'",\n'
	bibtex += '\tyear = '+year+',\n'
	bibtex += '\tdoi = {'+doi+'},\n'
	bibtex += '\turl = {'+url+'}\n'
	bibtex += '}\n\n'

	return bibtex

def cite(ID):
	fname = 'literature/pubmed'+ID+'.xml'
	if os.path.exists(fname):
		return parseXML( open(fname).read() )
	else:
		xml = downloadCitation(ID)
		open(fname, 'w').write(xml)
		return parseXML( xml )

try:
	ID = sys.argv[1]
except:
	ID = 'Master.bib.pubmed'
if os.path.exists(ID):
	compiled = ''
	for line in open(ID).read().split('\n'):
		if line.strip() != '':
			compiled += cite(line)
	open('Master.bib.compiled', 'w').write(compiled)
	open('Master.bib', 'w').write( open('Master.bib.manual').read() + compiled )
else:
	print cite(ID)

