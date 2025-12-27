---
title: A starter kit for reproducible research with R
date: 2019-11-01
tags:
  - R
  - reproducibleResearch
---

This accompanies my draft short article for the UKES Bulletin: *[A reproducible workflow for evaluation reports](http://www.pogol.net/reproducible-workflow)*.

Here are just two files which together get you started with a bare-bones reproducible research project. 


- Install and install [R](http://r-project.org) and [RStudio](https://www.rstudio.com/products/rstudio/download/).
- Download [this little example of a reproducible source file](https://www.dropbox.com/s/0yczy7xfsgsjksz/report.Rmd?dl=0) and an accompanying [example Excel file](https://www.dropbox.com/s/289c3x62kiv702n/data.xlsx?dl=0) describing the heights and ages of a bunch of boys and girls in a school.
- Save them together in a new folder.
- Double-click the source file to open it in RStudio. The source file has a couple of commands to read the Excel file, clean it and make a table and a chart, as well as plain text which becomes the headings and body of the document. 
- Press the blue "Knit" button in RStudio, you will get a beautiful Word document. 
- Try editing the text and then press "Knit" again to see what happens.
