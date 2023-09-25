simulerARMA<- function(n, m, Phi, Theta, s2){
  E= rnorm(n, 0, sqrt(s2))
  p=length(Phi)
  q= length(Theta)
  r=max(p,q)
  
  Y=rep(0,n)
  Y[1:r] = E[1:r]
  
  for (i in ((r+1):n)){
    ar = ifelse(p>0, t(Phi)%*%Y[(i-1):(i-p)], 0)
    ma = ifelse(q>0, t(Theta)%*%Y[(i-1):(i-q)], 0)
    Y[i]= (ar + E[i] + ma)
  }
  X=Y+m
  plot(X, type="l", main="Simulation ARMA", col="red")
}

simulerARMA(100, 5, c(0.2, -0.3), c(0.5),2)
simulerARMA(500, 5, c(0.95), c(),2)   #avec 0.95 il y a une corrélation bcp plus forte, plus la valeur est faible plus on dirait des bruits blancs

simulerARMA(500, 5, c(-0.95), c(),2) 
#avec des grosses valeurs négatives, parceque le négatif fait que si on est haut on va en bas etc















