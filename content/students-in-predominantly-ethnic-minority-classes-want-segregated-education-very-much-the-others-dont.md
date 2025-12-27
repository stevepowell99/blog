---
title: Students in predominantly ethnic minority classes want segregated education very much. The others don't.
date: 2010-10-07
tags:
  - Bosnia-Herzegovina
  - education
  - ggplot
  - research
---

![](http://stevepowell.blot.im/Public/charleston.png)

I just did this for what will hopefully be a book chapter on our Divided
Education - Divided Citizens research project with NEPC. Explanation
further below for anyone more interested in the actual topic ;-)

About the graphic:   
I like raw-data plots like this, made possible by Hadley Wickhams's
amazing ggplot2 package for the stats package R. Every school class in
the survey is on there somewhere. The line types need making a bit more
distinct though. Oh, and it would presumably get printed in greyscale,
so no colours.

I have spent weeks trying to analyse this data properly - spent ages
with a stuctural equation model, and then scrapped that and went for a
series of mixed effects models because of the class-level variance, but
I found trying to implement that kind of model very difficult.

In the end I will probably just go for this graph and one very simple
regression at class level and perhaps just one mixed effects regression.
I think together they say all that needs to be said. In statistics as
everywhere else the difficulty is in not saying too much. I am not sure
I succeeded here yet, true there is only one graph but it is a pretty
complicated one.

About the topic:  
It's about how support amongst students for segregated education is
much stronger in minority schools. Minority students, or rather,
students in predominantly minority classes, want segrated education very
much. The others don't.

The graph shows mean support for segregated schooling in each class by
percentage of majority children in each class. Dots represent individual
classes. Lines represent smoothed means per country.

The sample consisted of 2417 students from 134 schools in Bosnia &
Herzegovina, Estonia, Latvia and Slovakia. To represent the school-level
differences, the means of student support for segregation in each school
were calculated along with the percentage of majority students in each
school.


The figure shows that nearly all the classes had either heavily majority
or heavily minority composition; very few classes lie between the 20%
and 80% lines, and there are many classes which are 100% majority or
minority children. Also, there are rather more minority classes with a
few majority children than the other way round. The figure also shows
clearly that the larger the proportion of minority students in a school,
the stronger the support for segregation. In  Bosnia & Hergovina the children are not
such strong supporters of segregation. A linear regression predicting
support for segregation at class level on the basis only of country and
percentage majority children as predictors confirms this, with a
remarkable 63% of the class-level variance explained (adjusted R^2^).

Then another analysis shows that *majority children in predominantly
minority classes do not differ from their classmates in their strong
support for segregation*, whereas minority children in predominantly
majority classes are a little stronger than their classmates in their
support for segregation, but not as strong as their peers in minority
classes. 

