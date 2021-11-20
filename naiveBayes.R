library("arules")

df <- read.csv("centralized_AMAZONAS-APUI-Amazonia.csv", row.names=NULL, sep =",")
df[is.na(df)] <- 0
breaks = seq(from = 0, to = 260, by = 10)
print(breaks)
df$fire_power_category <- discretize(df$fire_power, method = "fixed", breaks=breaks)

library(caret)

set.seed(7267166)

#p is the percentage of data that goes to training
trainIndex=createDataPartition(df$fire_power_category, p=0.7)$Resample1
train=df[trainIndex, ]
test=df[-traindIndex, ]

#check balance
print(table(df$fire_power_category))

print(table(train$fire_power_category))

library(e1071)

NBclassifier = naiveBayes(fire_power_category~hum_median+precip_sum, data=train)

print(NBclassifier)
