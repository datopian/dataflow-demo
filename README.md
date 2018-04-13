This is a demo of how dataflow might work. It consists of:

* [x] An exercise converting an existing piece of small data wrangling into "DataOS" form
* [ ] Imagine usage of the tool
* [ ] A simple introductory tutorial
* [ ] Who the tool is for and desired features

"DataFlow" is our name for a data wrangling stack build on data packages and data package pipelines that would be part of the larger "DataOS" framework (https://datahub.io/docs/data-os).

# Tutorial - Introducing Frictionless Flows / dataflow / Data Flow / Data Pipelines

*A tutorial showing how we imagine DataFlow would work. In progress*

Introducing Frictionless [Data] Flows, a toolkit for building lightweight data processing workflows quickly and easily. LAMP for data wrangling!

This is a tutorial in using Frictionless Data Flows

## Install

```
pip install dataflow  # note this name is taken as is flow (by abandoned project)
```

## Getting started

Flows comes with a simple command line tool for scaffolding your data workflow ...  

```
dataflow
```

You can bootstrap your dataflow project by doing:

```
dataflow init
```

This will create a `flow.py` in your current directory.

> TODO: show how we could create a yaml file (like we have for DP Pipelines).

You can also initialise with a URL if you are starting doing data scraping e.g.:

```
dataflow init https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
```

Once the `flow.py` exists you can run it:

```bash
dataflow run flow.py -v

Running retrieve ... 
  spinner
Done
Running ...
Done
  ... file written to
  ... cat file with less
```

You can also also run your flow starting at part way through:

```
dataflow run flow.py --start-at-step=1
```

This is useful if you want to focus on debugging just one part of your data processing and avoid time consuming steps such as downloading data from an online source.

You can just run the flow.py with python (so dataflow is more just a scaffolding tool like you have in software frameworks):

```
python flow.py -v
```

---

~~Frictionless Flows is a pattern along with an implementing tool/library for creating data processing workflows quickly and easily.~~

Data Packages describe a static data file or dataset -- data frozen in time. Data Flows describe how to transform data -- data flowing in time. 


# Experiment with a real data wrangling use case

As an exercise we took an existing simple piece of data wrangling and converted in into the dataflow pattern (building a shim library in the process).

The existing code was this core dataset https://github.com/datasets/s-and-p-500-companies and specifically this script https://github.com/datasets/s-and-p-500-companies/blob/master/scripts/constituents.py.

It was converted into [`process.py`](blob/master/process.py) in this repo plus a minimal DataOS framework in `dataos/` (a simplistic data package pipelines!).

## Running it

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

# DataFlow: What is it and who is it for?

`dataflow` is more convention and pattern than library.

An analogy is web frameworks which were more about a core pattern plus a set of ready to use components cf python frameworks built around WSGI e.g. Pylons, Flask etc or ExpressJS for Node.

* Convention over configuration: Convention over configuration (also known as coding by convention) is a software design paradigm used by software frameworks that attempt to decrease the number of decisions that a developer using the framework is required to make without necessarily losing flexibility.


## Target Audience

Focus:

* Small to medium sized data
* Desktop wrangling -- people who start on their desktop
* Easy transition from desktop to "cloud"
* heterogeneous data sources
* process using basic building blocks
* less technical audience, heterogeneous sources
* limited resources - limit on memory, CPU etc

We like an analogy with the LAMP stack: it was simple, easy to get started and focused on a broad but specific area (simple websites)

* DataFlow (DataOS) is a simple, easy-to-start with stack for data wrangling
* Simple, cheap, lightweight, ubiquitous (CSVs)
* LAMP was a pattern of components loosely joined for a type of problem: quick to start websites
* Quick and customizable to needs
* Small data (and small can be quite big) (small websites that could be quite big)

What are we **not**?

* Big data processing and machine learning. E.g. we want to wrangle TBs of data in a distributed setup or we want to train a machine learning model. NO (?)
* Processing real-time event data.
* No technical expertise needed: we aren't a fancy ETL UI -- you probably need a bit of technical sophistication:w

## Features

* Trivial to get started and easy to scale up
* Set up and run from command line in seconds ...
  * dataflow init => flow.py
  * dataflow run / python flow.py
* Want to cache data from source and even between steps
  * so that we can run quickly (retrieving si slow), i can test flow quickly
* I want to validate input (and esp source) quickly (non-zero length, right structure)
* Immediate test is run: and look at output ...
  * => the main process function must not write but return output in a stream ??
	* Log, debug, rerun
* Degrades to simple python
* Conventions over configuration
* Log exceptions and / or terminate
* I want to write quick tests
* The input to each stage is a Data Package or Data Resource (not a previous task)
	* Data package based and compatible
* Processors can be a function (or a class): resource [or package object]
* A pre-existing decent contrib library of Readers (Collectors) and Processors and Writers
  * Luigi: Targets = Readers and Writers
  * BUT: i don't look at this ...

Minor:

* I want to handcraft my dp.json (including schema) and use in processing (or update? e.g. add schema)

Not priorities:

* Schedule, retry -- these are done in separate frameworks e.g. airflow, luigi

Questions

* What happens if the processors fails?
  * Exception and exit


# Technical specification

*In progress*

## Processors

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

Testing should be easy e.g.

```python

def parse(...): # a processor
		...


def test_extract_table(self):
		sample_table = '<table></table>'
		inresource = DataResource(sample_table)
		parsed_table = parse(inresource)
		assert parser_table = ...
```

## Comparisoin with DPP as it stands today

TODO

