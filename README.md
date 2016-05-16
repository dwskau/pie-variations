Pie and Donut Chart Evaluation
========

This project was used in a study that used the Mechanical Turk platform to test a series of pie chart variations.

The study is built on the excellent [Experimentr.js project](https://github.com/codementum/experimentr/blob/master/public/experimentr.js).

Running The Study
===

To run the project, you'll need [Redis](http://redis.io/) and [Node.js](https://nodejs.org/en/).

To start the Redis server, run the following command from the project directory:

	redis-server redis.conf

The Node server works on port 80, so it needs root access, and the project is set to use [Forever.js](https://github.com/foreverjs/forever) to ensure it keeps running:

	forever start app.js

Once you have the project running, you can visit _localhost_ in your browser to see the survey.