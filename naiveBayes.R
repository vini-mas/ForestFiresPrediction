library("arules")
library(caret)
library(e1071)

discretize_into_gaps <- function(column, interval_gap)
{
  category_breaks = seq(from = min(column), to = max(column)+interval_gap, by = interval_gap)
  return(discretize(column, method = "fixed", breaks=category_breaks))
}

# Read into a dataframe
rawDf <- read.csv("centralized_data/full/centralized_2020.csv", row.names=NULL, sep =",")

# Select the used rows only
# df <- rawDf[ , which(names(rawDf) %in% c('hum_median', 'temp_median', 'wind_median', 'fire_power'))]
df <- rawDf[ , which(names(rawDf) %in% c('biome', 'hum_median', 'temp_median', 'wind_median', 'fire_power'))]

# Remove NAs
df[is.na(df)] <- 0

# Create firepower categories
df$fire_power_category <- discretize_into_gaps(df$fire_power, 30)

# Visualizando a distribuicao dos fogos por dia
barplot(df$fire_power,
        names.arg=df$date,
        main="Histograma - Distribuicao dos fogos por dia", 
        xlab="Dia", 
        ylab="Poder de Fogo")

# Visualizando a humidade por dia
plot(df$temp_median, 
     main="Histograma - Distribuicao de humidade por dia", 
     xlab="Dia", 
     ylab="Poder de Fogo",
)

#Set a random seed for partitioning
set.seed(Sys.time())

#Create 2 partitions, 80% being the training, 30% being the testing
trainingPercentage = 0.8
trainIndex=createDataPartition(df$fire_power_category, p=trainingPercentage)$Resample1
trainingPartition=df[trainIndex, ]
testingPartition=df[-trainIndex, ]

#Watch each partitions amount of data
print(table(df$fire_power_category))
print(table(trainingPartition$fire_power_category))
print(table(testingPartition$fire_power_category))

#Generate a classifier
NBclassifier = naiveBayes(fire_power_category~biome+hum_median+temp_median+wind_median, data=trainingPartition)

#Watch the classifier percentages
print(NBclassifier)

# Train with the training partition
trainPred=predict(NBclassifier, newdata=trainingPartition, type = "class")
trainTable=table(trainingPartition$fire_power_category, trainPred)

# Train with the testing partition
testPred=predict(NBclassifier, newdata=testingPartition, type="class")
testTable=table(testingPartition$fire_power_category, testPred)

# Generate the accuracy of each table
trainAcc=(trainTable[1,1]+trainTable[2,2]+trainTable[3,3])/sum(trainTable)
testAcc=(testTable[1,1]+testTable[2,2]+testTable[3,3])/sum(testTable)

message("Contingency Table for Training Data")
print(trainTable)

message("Contingency Table for Test Data")
print(testTable)

message("Accuracy")
print(round(cbind(trainAccuracy=trainAcc, testAccuracy=testAcc),3))

# Below we added a way of testing the prediction of a single value
# Just add the desired values in the list(value1, value2, valueN...)
# Create a single testing data
# 'hum_median', 'temp_median', 'wind_median', 'fire_power'
singlePartition <- df[1,]
print(singlePartition)
singlePartition[1,] <- list(99999, 27, 80, 1.38, singlePartition[,5])
print(singlePartition)

# Predict with the training partition
singlePred=predict(NBclassifier, newdata=singlePartition, type = "class")
print('Fire predicted:')
print(singlePred)

