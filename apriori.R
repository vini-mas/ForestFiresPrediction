library("arules")
library(caret)
library(e1071)

discretize_into_gaps <- function(column, interval_gap)
{
  category_breaks = seq(from = min(column), to = 900, by = interval_gap)
  return(discretize(column, method = "fixed", breaks=category_breaks, infinity = TRUE))
}

# Read into a dataframe
rawDf <- read.csv("centralized_data/full/centralized_2020.csv", row.names=NULL, sep =",")

smallDf <- rawDf[sample(nrow(rawDf), size=700000), ]

smallDf <- smallDf[order(smallDf$date), ]

# Select the used rows only
# df <- rawDf[ , which(names(rawDf) %in% c('hum_median', 'temp_median', 'wind_median', 'fire_power'))]
#df <- rawDf[ , which(names(rawDf) %in% c('biome', 'hum_median', 'temp_median', 'wind_median', 'fire_power'))]
df <- smallDf[ , which(names(smallDf) %in% c('date', 'biome', 'hum_median', 'temp_median', 'wind_median', 'fire_power', 'days_wo_rain'))]

# Remove NAs
df[is.na(df)] <- 0


discDf <- df['date']
discDf$disc_temp_median <- discretize(df$temp_median, method="fixed", breaks=c(0, 10, 20, 30, 40, 50), infinity=TRUE)
discDf$days_wo_rain <- discretize(df$days_wo_rain, method="interval", breaks=10, infinity=TRUE)
discDf$hum_median <- discretize(df$hum_median, method="interval", breaks=10, infinity=TRUE)
discDf$wind_median <- discretize(df$wind_median, method="interval", breaks=10, infinity=TRUE)

# discDf$fire_power_category <- discretize_into_gaps(df$fire_power, 100)
discDf$fire_power_category <- discretize(df$fire_power, method="interval", breaks=10, infinity=TRUE)

# View(discDf)

View(discDf)

discDf[discDf$fire_power_category %in% c(54)]
                                         
categories <- discDf$fire_power_category[!duplicated(discDf$fire_power_category)]
categories <- sort(categories)
categories_string <- paste('fire_power_category', categories, sep="=")
categories_without_zero <- categories_string[ - c(1) ]
categories_without_zero
categories
# First Impression
rules.all <- apriori(discDf, appearance = list(rhs=c("fire_power_category=[-Inf,168)"), default="lhs"))
#rules.all <- apriori(discDf, appearance = list(rhs=c("fire_power_category=[270,300)", "fire_power_category=[300,330]"), default="lhs"))

print("\n\n=======================================\n\n")
high_power <- c("fire_power_category=[700,800)", "fire_power_category=[800, Inf]")
rules.all <- apriori(discDf,
                     parameter = list(supp=0.001, conf=0.1),
                     appearance = list(rhs=categories_without_zero,
                                       default="lhs"))

# inspect(rules.all)

# Ordenando as regras por suporte e inspecionando novamente o resultado
rules.sorted <- sort(rules.all, by="support")
inspect(rules.sorted)

# Ordenando as regras por confianca e inspecionando novamente o resultado
rules.sorted <- sort(rules.all, by="confidence")
inspect(rules.sorted)
