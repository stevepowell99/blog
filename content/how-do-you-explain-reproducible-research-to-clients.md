---
title: How do you explain reproducible research to clients?
date: 2018-03-01
tags:
  - reproducibleResearch
  - research
---

Most of the statistics work I do now is reproducible research - this   
can offer a big advantage for clients but of course that doesn't   
necessarily mean they realise it ...

Below is a text I have been working on to explain   
reproducible research. Would be very interested if anyone has any   
better ideas ....

---------------------

## Short version

Reproducible research: wherever appropriate, all tables, graphics and statistical analyses in my reports are produced from a "source file" which contains the usual headings, text etc., as well as machine-readable code for producing each table and graphic. Then each time I save a new version of the report, a statistics program called "R" loads the raw data, cleans it, does calculations, replaces the code with the corresponding tables and graphics, and produces a Word, PDF or web document. That means consistency in presentation, up-to-date results, less chance of error, and complete transparency because it is easy to independently check the results.

## Long version

Wherever a report includes quantitative data, I produce it using a "reproducible" workflow: graphs, tables, and even calculated data such as totals in the middle of text passages are produced automatically (according to instructions in a "source file" using a statistics program called ["R"](http://r-project.org)) each time I save a new version of the report. 

Advantages for the client: 

- **Elimination of errors** because there is no manual cutting-and-pasting or editing of data in the original data files, or manual editing of tables or graphics: the original data files (e.g. responses to questionnaires) are not touched at all but are loaded from scratch each time. 
- **Faster workflow** because I can produce preliminary and pre-final report versions even before all data collection is completed. 
- **Better presentation** because it is easy to make global changes to the way data is presented (e.g. to change the font size on dozens of graphics with one click).
- **Freshness of external data** because the latest versions of any data from other sources, e.g. World Bank data, will be loaded live from online repositories to ensure "freshness".
- **Transparency & verifiable accuracy** the client or others can, if desired, use the "source file" to repeat these calculations, see exactly how they are arrived at, and verify for errors.
- **Openness and extensibility** because the client can extend the analyses in later months or years -- or hand them over to others if desired -- without having to start from scratch.   

Things for the client to bear in mind:

- My usual workflow is to produce preliminary versions of the report(s) online at my own domain so you can follow progress. This will update automatically so you will always see the latest version. I can produce Word and PDF documents too, but if you want to make preliminary comments it is better to use email / Slack / Skype etc rather than doing it inside those documents.  
- I will usually produce the final draft in Word format. Up to that point, if you say, e.g. "I want all the table headings up to page 22 in a larger font" or "I want to exclude the data from before 2011 from the whole report", I can make such changes very easily. After that, it is no longer so easy to make global changes to the appearance and content. 



