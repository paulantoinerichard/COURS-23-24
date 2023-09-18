library(datasets)
Data= AirPassengers
Data
typeof(Data)   
class(Data)   #ts pour time series, les données sont deja au bon format


# GRAPHE DES VARIABLES
plot(Data, ylab="AirPassengers")
grid()

frequency(Data)


# ON PASSE AU LOG pour réduire l'amplitude des périodes
LData= log(Data)
plot(LData, ylab="AirPassengers")
grid()

frequency(LData)


library(stats)
Decomp = decompose(LData, type ="additive")

plot(Decomp$seasonal)
plot(Decomp$trend)
plot(Decomp$random)
plot(Decomp$figure, type="l")
plot(Decomp)



n= length(Decomp$trend)
Tps=1:n
RegLinTrend = lm(Decomp$trend ~Tps)

summary(RegLinTrend)


estA0 = RegLinTrend$coefficients[1]   #R part de 0 pas de 1
estA1 = RegLinTrend$coefficients[2]

plot(Tps, Decomp$trend, type = "l", ylab="Trend")
lines(Tps, estA0+estA1*Tps, col="red", lty=2)



#création de 2  nouvelles périodes

#Xt = Mt + St + Zt
#Mt = A0 + A1*temps
#St = decomp$figure
#Zt aléatoire

Ntps = (n+1):(n+24)
PredT = estA0 + estA1*Ntps
PredS = Decomp$figure
Pred = PredT + PredS
plot(ts(c(LData, Pred), frequency = 12, start=1949),ylab="Log(AirPassengers)", type="l")
lines(ts(exp(Pred), frequency = 12, start=1961) , col="red")
grid()


























































