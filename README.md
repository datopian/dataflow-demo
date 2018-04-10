This is a demo of how dataflow might work.

As an exercise wew took an existing simple piece of data wrangling and converted in into the dataflow pattern (building a shim library in the process):

https://github.com/datasets/s-and-p-500-companies

https://github.com/datasets/s-and-p-500-companies/blob/master/scripts/constituents.py

## An imagined scenario

Here's an imagine scenario:

```
dataflow init https://en.wikipedia.org/wiki/List_of_S%26P_500_companies flow.py
dataflow run flow.py -v

Running retrieve ... 
  spinner
Done
Running ...
Done
  ... file written to
  ... cat file with less
```

Start at step 1 in the flow:

```
dataflow run flow.py --start-at-step=1
```

You can just run the flow.py with python (so dataflow is more just a scaffolding tool like you have in software frameworks):

```
dataflow init https://en.wikipedia.org/wiki/List_of_S%26P_500_companies flow.py
python flow.py -v
```

## What we built

Code is `process.py` with DataOS framework in `dataos/` (a simplistic data package pipelines!).

Run the process

```
# may need to run first pip install beautifulsoup4
python process.py
```

Output is as follows, note some nice debug output (which is super useful when developing):

```
Running ... get
https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
Running ... parse
Stream <http.client.HTTPResponse object at 0x10e0b20f0>
Running ... process
{'fields': [{'name': 'Ticker Symbol'}, {'name': 'Security'}]}
['Ticker symbol', 'Security', 'SEC filings', None, 'GICS Sub Industry',
'Address of Headquarters', None, 'CIK']
['MMM', '3M Company', 'reports', 'Industrials', 'Industrial Conglomerates',
'St. Paul, Minnesota', '', '0000066740']
Running ... csvwriter
{'fields': [{'name': 'Symbol', 'type': 'string'}, {'name': 'Name', 'type':
'string'}, {'name': 'Sector', 'type': 'string'}]}
['MMM', '3M Company', 'Industrials']
['AOS', 'A.O. Smith Corp', 'Industrials']
```

## Patterns and Notes

`dataflow` is more convention and pattern than library.

An analogy is web frameworks which were more about a core pattern plus a set of ready to use components cf python frameworks built around WSGI e.g. Pylons, Flask etc or ExpressJS for Node.


* Convention over configuration: Convention over configuration (also known as coding by convention) is a software design paradigm used by software frameworks that attempt to decrease the number of decisions that a developer using the framework is required to make without necessarily losing flexibility.


### Target Audience

What are we **not**?

### Processors

Processors would look like this -- more complex options could be possible.

```
# dataflow init
def processor(resource, package=None):
    # resource.rows()
    
    return rows (array of arrays) / (array of dictionaries) / buffer/string (utf8) / iterator/stream, (data, schema), (data,schema,metadata), DataResource, DataPackage
    
class Processor(object):
    def __init__(self, resource, package=None, context??):
    
    def run():
        return ...
        
        
def process_row(row, *_):
    row['constant'] = 5
    return row
        
```
