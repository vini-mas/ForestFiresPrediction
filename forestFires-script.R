
library("arules")

df <- read.csv("centralized_2020.csv", row.names=NULL, sep =",")


# https://www.datacamp.com/community/tutorials/market-basket-analysis-r

incomeItems <- grep("^fire_power=", itemLabels(Adult), value = TRUE)

rules.all <- apriori(df, control = list(verbose=F),
                     parameter = list(minlen=5, supp=0.2, conf=0.8))
#rules.sorted <- sort(rules.all, by="confidence")
#inspect(rules.sorted)

rules_subset <- subset(rules.all, (grepl(rhs, "Product=", fixed=TRUE)))
inspect(rules_subset)