# COVID-19-EDA
Going through the 4 GB (currently) Kaggle COVID-19 Data set to find some interesting information about COVID-19 and predict some things.

Get the data set here: https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge

## What do we know about Incubation?

I essentially searched each sentence of each body text of the articles for the word incubation and then with regex searched for digits followed by the string "day" or "days". After this, I stripped all non-numerical characters in order to preserve pharses such as 3-7. There were still some serious outliers in the 600 range, but I ended up trimming the graph before the outliers begun.

![alt text](https://github.com/jbofill10/COVID-19-EDA/blob/master/Charts/IncubHist.png)

From the data I extrapolated, I arrived at an average of 12 days is how long COVID-19 should take to incubate. In hindsight, that is right around with what is common knowledge now (7-14 days).  

I plan to still tamper with the regular expression to get more accurate numbers.
