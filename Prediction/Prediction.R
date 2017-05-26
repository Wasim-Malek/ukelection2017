
#This code uses the following link as a basis
#https://www.r-bloggers.com/time-series-analysis-building-a-model-on-non-stationary-time-series/

#Install and load packages
install.packages("astsa")
require(astsa)

#Import dummy data
data<- read.table(file="C:/Users/Student/Documents/Twitter Project/dummydata.csv",header=TRUE,sep= ",",dec=".",na.string="NA")

#Check imported data looks correct
str(data)
head(data)

#Filter data to select sentiment only
ConsSent = ts(data[1:31,3],frequency=31)

#Plot the sentiment
plot(ConsSent, xlab="Time", ylab="Average Sentiment", main="Conservative Party's Average Sentiment on Twitter, May 2017")

#Check whether data is non-statonary
plot(diff(ConsSent))
acf2(diff(ConsSent))

#Prediction from 1st to 8th June
sarima.for(diff(ConsSent),8,0,1,1)

