############################################################################
# Disciplina: CMP259
# Profa: Karin Becker
#
# Atividade Pratica: Estudo Dirigido 01 - 
#                    Mineracao de dados usando regras de associacao
#                                     
#
# Conjunto de dados: Titanic, disponivel em http://www.rdatamining.com/data
#
############################################################################

# SE NAO TIVER O PACKAGE ARULES, instale o pacote via a aba Packages
# Voce pode tambem executar o comando install abaixo, mas execute APENAS UMA VEZ
#install.packages("arules")

# Voce deve definir seu diret??rio de trabalho

# Carrega o arquivo de dados
load("titanic.raw.rdata")

# Visualizando conjunto de dados
View(titanic.raw)

# Analisando a estrutura do objeto titanic criado
str(titanic.raw)

# Realizando analise estatistica sobre os dados
summary(titanic.raw)

# Visualizando a distribuicao dos passageiros por classe
plot(titanic.raw$Class, main="Histograma - Distribuicao dos passageiros em classes", 
     xlab="Classes", ylab="Total passageiros",
     ylim=c(0,1000), las=0)

# Visualizando a distribuicao dos passageiros por idade
# MODIFIQUE O COMANDO ACIMA PARA FAZER A DISTRIBUICAO POR IDADE
# USE YLIM=c(0,2000) para uma melhor visualizacao
plot(titanic.raw$Age, main="Histograma - Distribuicao dos passageiros por idade", 
     xlab="Idade", ylab="Total passageiros",
     ylim=c(0,2000), las=0)

#
# Carregando biblioteca para usar regras de associacao
#
library("arules")

# Encontrando regras de associacao com configuracao padrao da funcao
rules.all <- apriori(titanic.raw)

# Inspecionando as regras de associacao geradas
inspect(rules.all)

# Ordenando as regras por suporte e inspecionando novamente o resultado
rules.sorted <- sort(rules.all, by="support")
inspect(rules.sorted)

# Ordenando as regras por confianca e inspecionando novamente o resultado
rules.sorted <- sort(rules.all, by="confidence")
inspect(rules.sorted)

# Executando o apriori com suporte e confianca de 90% e inspecinando as regras de associacao ordenadas
rules.all <- apriori(titanic.raw, parameter = list(supp=0.9, conf=0.9))
rules.sorted <- sort(rules.all, by="support")
inspect(rules.sorted)

# Reduzindo o suporte e confianca para 10% e 30%, respectivamente
rules.all <- apriori(titanic.raw, parameter = list(supp=0.1, conf=0.3))
rules.sorted <- sort(rules.all, by="support")
inspect(rules.sorted)

# Restringindo a busca de regras de associacao para retornar somente
# regras que contenham o atributo "sobrevivente"
# usando valores intermediarios para suporte e confianca
rules.all <- apriori(titanic.raw, control = list(verbose=F),
                     parameter = list(minlen=2, supp=0.3, conf=0.6),
                     appearance = list(rhs=c("Survived=No", "Survived=Yes"), default="lhs"))
quality(rules.all) <- round(quality(rules.all), digits=2)
rules.sorted <- sort(rules.all, by="support")
inspect(rules.sorted)

#
# Re-executando com suporte mais baixo, e Removendo regras redundantes
#

rules.all <- apriori(titanic.raw, control = list(verbose=F),
                     parameter = list(minlen=2, supp=0.05, conf=0.6),
                     appearance = list(rhs=c("Survived=No", "Survived=Yes"), default="lhs"))
quality(rules.all) <- round(quality(rules.all), digits=3)
rules.sorted <- sort(rules.all, by="support")
inspect(rules.sorted)

# Encontrando regras duplicadas
subset.matrix <- is.subset(rules.sorted, rules.sorted, sparse = FALSE)
subset.matrix[lower.tri(subset.matrix, diag=T)] <- NA
redundant <- colSums(subset.matrix, na.rm=T) >= 1

# Se desejar, pode ver quais as as regras redundantes encontradas no comando comentado abaixo
#which(redundant)

# Removendo regras redundantes e listando resultado
rules.pruned <- rules.sorted[!redundant]
inspect(rules.pruned)

## Usando o lift para avaliar as regras
## Quando o lift e 
# - > 1, a presenta do valor a esquerda aumenta a probabilidade de ocorrencia do valor a direita (positivamente correlacionados).
# - = 1, a ocorrencia do valor a esquerda nao afeta a ocorrencia do valor a direita (estatisticamente independentes).
# - < 1, a ocorrencia do valor a esquerda diminui a probabilidade de ocorrencia do valor a direita (negativamente correlacionados).
rules.all <- apriori(titanic.raw, control = list(verbose=F),
                     parameter = list(minlen=2,supp=0.01,conf=0.5),
                     appearance = list(rhs=c("Survived=No", 
                                             "Survived=Yes"), 
                                       default="lhs"))
quality(rules.all) <- round(quality(rules.all), digits=3)
rules.sorted <- sort(rules.all, by="lift")
# Eliminar as regras duplicadas
subset.matrix <- is.subset(rules.sorted,rules.sorted,sparse=FALSE)
subset.matrix[lower.tri(subset.matrix, diag=T)] <- NA
redundant <- colSums(subset.matrix, na.rm=T) >= 1
rules.pruned <- rules.sorted[!redundant]
# Examine os resultados
inspect(rules.pruned)


# Interpretando regras de sobrevivencia de criancas
rules <- apriori(titanic.raw,
                 parameter = list(minlen=3, supp=0.002, conf=0.3),
                 appearance = list(rhs=c("Survived=Yes", "Survived=No"),
                                   lhs=c("Class=1st", "Class=2nd", 
                                         "Class=3rd",
                                         "Age=Child", "Age=Adult"),
                                   default="none"),
                 control = list(verbose=F))
rules.sorted <- sort(rules, by="confidence")
inspect(rules.sorted)

#
# explorando recursos de visualizacao
#
library(arulesViz)
#geracao de regras 
rules.all <- apriori(titanic.raw, control = list(verbose=F),
                     parameter = list(minlen=2,supp=0.005,conf=0.2),
                     appearance = list(rhs=c("Survived=No", 
                                             "Survived=Yes"), 
                                       default="lhs"))
quality(rules.all) <- round(quality(rules.all), digits=2)
rules.sorted <- sort(rules.all, by="lift")
# Eliminar as regras duplicadas
subset.matrix <- is.subset(rules.sorted,rules.sorted,sparse=FALSE)
subset.matrix[lower.tri(subset.matrix, diag=T)] <- NA
redundant <- colSums(subset.matrix, na.rm=T) >= 1
rules.pruned <- rules.sorted[!redundant]
# Examine os resultados
inspect(rules.pruned)

# Scatterplot por lift/confianca
#Plot SubRules
# plot estatico
plot(rules.pruned)
# plot dinamico
plot(rules.pruned,engine = "htmlwidget")

# Selecionar apenas um conjunto de regras
subrules<-rules.pruned[quality(rules.pruned)$confidence>0.5]
inspect(subrules)

# plot na forma de gr??fos (limitado a 100 regras)
# plot estatico
plot(subrules, method = "graph")
# plot dinamico
plot(subrules, method = "graph",  engine = "htmlwidget")


