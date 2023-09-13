# Installation
Requirements are shown in pyproject.toml. Install requirements via this command:
```
    cd [project folder]
    pip install -e .
```
You may run a series of demo functions in the terminal via this command:
```
    python wikiwrapper.py
```
Or the test suite via this command:
```
    python tests.py
```


# Assumptions
Assumption: Top 1000 per day is a reasonable data set for calculating most viewed for a week or month. 
This assumption could be invalid if you had widely varying read counts from day to day. e.g. 
```
    Day 1: Article 1: 50 reads, Article 2: 40 reads, etc… 
    Day 2: Article 2: 11 reads, Articles 3 through 1000: 10 reads each
           Article 1: 9 reads - but counted as 0 since it is out of the top 1000

    Actual read counts after two days: 1: 59, 2: 51
    Calculated read counts after two days: 1: 50, 2: 51
```
- Alternate Considerations: Depending on production resources, project goals, and how often we expect to hit this calculation, we may choose to use even a smaller dataset than 1000 to calculate with at the expense of accuracy. It appears that 1000 is the maximum provided by the wikipedia API.

Assumption: we are only concerned with the en.wikipedia domain, since that was the link provided in the assessment.
- Alternate Considerations: wikipedia’s API provides other domains (e.g. pt.wikipedia, en.wikisource) and we may wish to include those.

Assumption: all-agents is appropriate for our use case.
- Alternate Considerations: you may wish to limit to only human users or more specific criteria


# Additional Thoughts
- I have manually specified utf-8 encoding as needed since I was working on a Windows host which attempted to enforce cp1252, but in a production environment this may not be necessary and/or you may wish to handle multiple encodings.

- For the concept of "most viewed" articles, you could reasonably omit pages such as "Main_Page" or "Special:Search" as they are likely not topically relevant to our application, in which case you'd filter those out before returning the list. Since there isn't a full context (defining which pages should be omitted) for this test application, I left those in the return value.

- What you select for your application's empty or error return values depends on what you want the application to do. Since there isn't a full context for this test application, I have chosen to return None for empty and to print out error messages directly with print(), including passing along Wikipedia's error codes to print. 
Other options could be [], {}, "", etc. and console.log, raise Exception, trigger a monitoring framework such as Rollbar, etc.

- Again, depending on application context, you may wish to validate article title to certain formatting, or you may just wish to pass along Wikipedia's own 404 response if you submit a bad title. I opted for the latter since no definition was given for correct formatting. I considered limiting whitespace just to say I did, but turns out the wikipedia API actually handles whitespace fine.

- If, in the context of a real application, we expected to do repeated operations on the same article or same date range, I would almost certainly store/cache the requested and calculated information (most viewed or top view day, for example) locally to avoid costly repetitions since the source data from Wikipedia will never change for dates in the past.