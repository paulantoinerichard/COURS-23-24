data = read.csv('/users/2024/ds2/118004830/Téléchargements/BTC-USD.csv')
head(data)


#plot(data$Close, type='l', main="Action BTC", ylab="Close", xlab="Jours")

logClose=log(data$Close)
plot(logClose,type='l', main="Action BTC", ylab="Close", xlab="Jours")
plot()
#processus non stationnaire -> ARMA

modele=Arima(logClose, include.mean = TRUE)
modele


n <- length(logClose)
temps <- 1:n
RegLin <- lm(logClose ~ temps)
summary(RegLin)

# Afficher la ligne de régression
plot(temps, logClose, main="Régression Linéaire", xlab="Temps", ylab="logClose", typ='l')
abline(RegLin, col='red')

Res= RegLin$residuals
checkupRes = function(Res, l, lagmax=40, lblag=5){
  
  # Partitionnement de la fenêtre graphique 
  layout(matrix(c(1,1,1,2:7), nrow=3, ncol=3, byrow=TRUE))
  par(oma=c(0, 0, 0, 0))
  #par(mgp=c(0, 0, 0))
  par(mar=c(2.5, 2, 1.5, 2))
  
  m = mean(Res)
  s = sd(Res)
  
  # Série des résidus
  plot(Res, type="l", col="black", main="Série", xlab="", ylab="", cex=0.6)
  
  # ACF/PACF
  ACF = acf(Res, lag.max=lagmax, plot=FALSE)
  plot(ACF, ylim=c(-1, 1), xlab="", ylab="")
  title("ACF")
  PACF = pacf(Res, lag.max=lagmax, plot=FALSE)
  plot(PACF, ylim=c(-1, 1), xlab="", ylab="")
  title("PACF")
  
  # Nuage de points avec décalage de 1 dans le temps
  n = length(Res)
  plot(Res[1:(n-1)], Res[2:n], type="p", col="blue", main=substitute(bold("t / t-1")), xlab="", ylab="")
  
  # Test de Ljung-Box
  lbpv = Box.test(Res, lag=lblag, type="Ljung-Box")$p.value
  cat("Test de Ljung-Box : p-val=", lbpv, sep="")
  
  # Histogramme
  hist(Res, breaks=sqrt(n), freq=FALSE, col="skyblue", main="Densité", xlab="", ylab="")
  curve(dnorm(x, m=m, sd=s), col="red", lty=2, add=TRUE)
  
  # Test de Shapiro-Wilk
  swpv = shapiro.test(Res)$p.value
  cat("\nTest de Shapiro : p-val=", swpv, sep="")
  
  # QQ plots
  qqnorm(Res, main="Quantiles", xlab="", ylab="")
  qqline(Res, distribution=qnorm, lty=2)
  
  # Nuage de points standardisé
  plot((Res-m)/s, type="p", main=substitute(bold("Série standardisée")), xlab="", ylab="")
  abline(h=c(-1.96, 1.96), lty=2, col="red")
}
checkupRes(Res)
#pas une tendance  mais normal parceque on a juste enlever les tendances
#pas gaussien d'après shapiro, masi plutot correct quand meme
# plein de corélation, mais est ce que c'et stationnaire ?

library(tseries)
adf.test(Res)
kpss.test(Res)  #on ne sait pas, dans le doute on va tester arma

#ACF décroissance pas si rapide, coincide que les tests de stationnarités sont perdus aussi
# par contre PACF puis plus rien, donc caractéristique d'un AR(1)

library(forecast)
ARMA = Arima(Res, order=c(1,0,0), include.drift = FALSE, include.mean = FALSE)
summary(ARMA)
ResARMA = ARMA$residuals

checkupRes(ResARMA)
dev.off()
Mod=fitted(RegLin)+fitted(ARMA)

plot(logClose, type='l', main='action btc', ylab="Close", xlab="Jours")
#lines(Mod, col='red', lty=2)
BI=Mod - 1.96*sqrt(ARMA$sigma2)
BS=Mod + 1.96*sqrt(ARMA$sigma2)
lines(BI, col='red', lty=2)
lines(BS, col='red', lty=2)

polygon(c(1:n,n:1),c(BI,rev(BS)),col="gray",border='red')
lines(logClose, type='l', main='action btc', ylab="Close", xlab="Jours")


ARMA2=Arima(logClose, order=c(1,0,0),include.drift=TRUE)
summary(ARMA2)

plot(logClose, type='l',main='action btc', ylab="Close", xlab="Jours")
lines(fitted(RegLin)+fitted(ARMA),col='blue', lty=2)
lines(fitted(ARMA2), col='red', lty=2)

#on doit mtn repasser a l'exponentiel

RegLin2 <- lm(data$Close ~ temps)
Res2= RegLin2$residuals
ARMA22 = Arima(Res, order=c(1,0,0), include.drift = FALSE, include.mean = FALSE)


plot(data$Close, type='l', main='Action BTC', ylab='Close', xlab='Jours')
lines(fitted(RegLin2)+fitted(ARMA22),col='blue')





















