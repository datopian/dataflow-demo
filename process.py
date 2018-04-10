import sys
sys.path.insert(0, '.')

from bs4 import BeautifulSoup

import dataos.run
from dataos.readers import get
from dataos.writers import csvwriter

def parse(resource):
    '''out = {
      schema: makeSchema(['Ticker Symbol', 'Security'])
    }'''

    # turn html in to a Data Resource
    soup = BeautifulSoup(resource.buffer(), 'html.parser')
    table = soup.find("table", { "class" : "wikitable sortable" })
    header = [ x.string for x in table.findAll('th') ]
    def parserow(row):
        return [ ' '.join(f.stripped_strings) for f in row.findAll('td') ]
        
    rows = [ parserow(row) for row in  table.findAll('tr') ]
    rows = [ r for r in rows if r ]

    # basic validation of source data
    # table.headers[0] != ... 
    if header[0] != "Ticker symbol" or header[1] != "Security":
        raise Exception("Can't parse wikipedia's table! Found headers: %s" % header)
        
    schema = { 'fields': [
            { 'name': 'Ticker Symbol' },
            { 'name': 'Security' }
            ]
        }
    return dataos.run.DataResource([header] + rows, schema)


def makeSchema(headers):
    out = { 'fields': [ { 'name': f, 'type': 'string' } for f in headers ] }
    return out

def process(resource):
    table = resource

    # Retreive the values in the table
    records = [ [ row[0], row[1], row[3] ] for row in table.rows() ]
    records.sort(key=lambda s: s[1].lower())
    
    # load this from raw dp.json ??
    newschema = makeSchema(['Symbol', 'Name', 'Sector'])
        
    return dataos.run.DataResource(
      records,
      schema=newschema,
      metadata={ 'path': 'constitutents.csv' }
    )


dataos.run.runFlowSychronous(
    config={
	  'source': 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
	},
    	steps=( get, parse, process, csvwriter )
    )

