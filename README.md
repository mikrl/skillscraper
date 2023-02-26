# Installation
Assuming you have virtualenvwrapper installed, run these commands from the project root:

`mkvirtualenv skillscraper`

`pip install -r requirements.txt`

# Running
Inside the `skillscraper` virtual environment, invoke the program as a python module:

`python -m skillscraper.main`

An example usage is below:

```
usage: python -m skillscraper.main [-h] [-v VERBOSITY] [-o OUTPUT] [--scrape-only] title location

Scrape job postings from the internet and turn them into ngrams.

positional arguments:
  title                 Job title to search for
  location              Location to search in

options:
  -h, --help            show this help message and exit
  -v VERBOSITY, --verbosity VERBOSITY
                        verbosity level (0 = WARNING, 1 = INFO, 2 = DEBUG)
  -o OUTPUT, --output OUTPUT
                        Output file path. If not specified, results will be printed to the terminal
  --scrape-only         Only scrape the jobs and do not process the output further. Will save jobs if outfile is specified
```

For example, to search for Software Developer jobs in Waterloo, ON and save the n-gram statistics to `ngrams.json`:

`python -m skillscraper.main -o jobs.json "Software Developer" "Waterloo, ON"`

If you wish to do this same search but instead only save the jobs to `jobs.json`:

`python -m skillscraper.main --scrape-only -o jobs.json "Software Developer" "Waterloo, ON"`

The default (and recommended) verbosity level is 1 and will show INFO log lines. 
To suppress all output:

`python -m skillscraper.main -v 0 "Software Developer" "Waterloo, ON"`

# Donate
BTC: bc1q20xzgwn79a5ltgtglmlhhrlh543q9mepwskvqf