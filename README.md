Pie and Donut Chart Evaluation
========

This project was used in a study that used the Mechanical Turk platform to test a series of pie chart variations.

The study is built on the excellent [Experimentr.js project](https://github.com/codementum/experimentr/blob/master/public/experimentr.js).

Data
===
The collected data files are in the `analysis` directory, together with some scripts and the R code to create the figures in the paper.

### Data Files

* `pie-variations-data.json`: the original data as collected during the study, in JSON format
* `pie-variations-reshaped-unique.csv`:  trial data in CSV format, with incomplete trials removed
* `pie-variations-demographics.csv`: demographics data in CSV format
* `predictions.csv`: predicted values for the different charts based on area and arc length, for all angles in half-degree steps
* `pie-variations-enriched.csv`: same as `pie-variations-reshaped-unique.csv` but with additional columns for predicted values based on arc length and area

### Scripts

* `enrich.py`: creates the `predictions.csv` file and adds predictions to the trials data to create `pie-variations-enriched.csv`
* `cleanup.py`: parses the original JSON data and reshapes the data into one row per trial, generates `pie-variations-reshaped-unique.csv` and `pie-variations-demographics.csv`
* `variationviolins.R`: R code to do analysis and generate the figures in the paper

Running The Study
===

To run the project, you'll need [Redis](http://redis.io/) and [Node.js](https://nodejs.org/en/).

To start the Redis server, run the following command from the project directory:

	redis-server redis.conf

The Node server works on port 80, so it needs root access, and the project is set to use [Forever.js](https://github.com/foreverjs/forever) to ensure it keeps running:

	forever start app.js

Once you have the project running, you can visit _localhost_ in your browser to see the survey.