library(dplyr)
library(ggplot2)

# setwd("/<repository location>/pie-variations/analysis")

data <- read.csv("pie-variations-enriched.csv")

dataFiltered <- data %>%
	filter(workerID != "QV69HK91") %>% # filter out the guy who answered in degress rather than percent
	mutate(chart.type = factor(chart.type,
							   levels=c('pie', 'exploded', 'outerRadius', 'square', 'ellipse'),
							   labels=c('Pie', 'Exploded', 'Larger Slice', 'Square', 'Ellipse')),
		   absError = abs(judged.true),
		   opposite = (abs(opposite.ans-correct.ans) < absError) & (abs(50-correct.ans) > 5))

dataAggregated <- dataFiltered %>%
	group_by(chart.type, workerID) %>%
	summarize(meanLogError = mean(log.error),
				ci95LogError = sd(log.error)*1.96/sqrt(n()),
				meanError = mean(judged.true),
				ci95Error = sd(judged.true)*1.96/sqrt(n()),
				meanAbsError = mean(abs(judged.true)),
				ci95AbsError = sd(abs(judged.true))*1.96/sqrt(n()),
				meanRT = mean(time_diff_time.trial, na.rm=TRUE),
				ci95RT = sd(time_diff_time.trial, na.rm=TRUE)*1.96/sqrt(n())
	)

lowerCI <- function(v) {
	mean(v) - sd(v)*1.96/sqrt(length(v))
}

upperCI <- function(v) {
	mean(v) + sd(v)*1.96/sqrt(length(v))
}

# Violin plot of log error for Figure 4
ggplot(dataAggregated, aes(x=chart.type, y=meanLogError, fill=chart.type)) +
	geom_violin(size=1, aes(color=chart.type), show.legend = FALSE) +
	stat_summary(fun.ymin=lowerCI, fun.ymax=upperCI, geom="errorbar", aes(width=.1)) +
	stat_summary(fun.y=mean, geom="point", shape=18, size=3, show.legend = FALSE) + 
	labs(x = NULL, y = "Log Error")

# Violin plot of response time for Figure 5
ggplot(dataAggregated, aes(x=chart.type, y=meanRT, fill=chart.type)) +
	geom_violin(size=1, aes(color=chart.type), show.legend=FALSE) +
	ylim(0, 25) + 
	stat_summary(fun.ymin=lowerCI, fun.ymax=upperCI, geom="errorbar", aes(width=.1)) +
	stat_summary(fun.y=mean, geom="point", shape=18, size=3, show.legend = FALSE) + 
	labs(x = NULL, y = 'Time to Answer (s)')

ggplot(dataAggregated, aes(x=chart.type, fill=chart.type)) +
	geom_violin(size=1, aes(y=meanAbsError, color=chart.type), show.legend = FALSE) + ylim(0, 15) +
	stat_summary(fun.y=mean, geom="point", aes(y=meanAbsError), shape=18, size=4, show.legend = FALSE) + 
	labs(x = NULL, y = "Absolute Error")

ggplot(dataAggregated, aes(x=chart.type, fill=chart.type)) +
	geom_violin(size=1, aes(y=meanError, color=chart.type), show.legend = FALSE) + ylim(-10, 10) +
	stat_summary(fun.y=mean, geom="point", aes(y=meanError), shape=18, size=4, show.legend = FALSE) + 
	labs(x = NULL, y = "Error")

# mean of log error and 95% CI for Table 1
errorByChartType <- dataFiltered %>%
	group_by(chart.type) %>%
	summarize(meanError = mean(log.error),
			  ci95Error = sd(log.error)*1.96/sqrt(n()))

# Models to look at for comparison of predictors
angleModel <- lm(ans.trial ~ correct.ans, dataFiltered)
areaModel <- lm(ans.trial ~ areaPrediction, dataFiltered)
arcModel <- lm(ans.trial ~ arcPrediction, dataFiltered)

anglexTypeModel <- lm(ans.trial ~ correct.ans + chart.type, dataFiltered)
areaxTypeModel <- lm(ans.trial ~ areaPrediction + chart.type, dataFiltered)
arcxTypeModel <- lm(ans.trial ~ arcPrediction + chart.type, dataFiltered)
