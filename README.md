# Running
We assume you have virtualenvwrapper installed and run these commands from the project root:
`mkvirtualenv skillscraper`

`pip install -r requirements.txt`

`python -m skillscraper.main`

This will run a hardcoded search over the first page of results for "Software developer" in "Waterloo, ON" 
and output a dict of all 1,2,3-grams and their counts.