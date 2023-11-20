
# Data Explanation

## Data Sources

All data was sourced from the [Vugraph Project](http://www.sarantakos.com/bridge/vugraph/), a community archive of contract bridge tournaments from 1955 to 2016.
The source data is in the .lin format, which is a proprietary file format that stores play-by-play information for a segment in a bridge tournament.

## Scraping Process

The data was scraped from the Vugraph Project's website using the Python script crawler.py, which uses beautifulsoup and a few of Python's builtin libraries to 
traverse all pages in the website's hierarchy and download any pages that end in .lin. This process resulted in ~12,000 discrete lin files. Many of these files
describe games that are out of the scope of this project, which we discuss in the cleaning process section.

## Cleaning Process

After being scraped, the data was cleaned using the Python script linparser.py, which imports parser_classes.py as a module. linparser.py takes a list of lin
files 

## File Hierarchy