#Read command line arguments
args <- commandArgs(trailingOnly = TRUE)
inputFile <- args[1]
rm(args)


#Read data and compute errors for each cluster
inputData <- read.table(inputFile, header = TRUE)

pdf(paste(inputFile,".pdf",sep=""))
#Plot empirical CDF of tweet polarity
graphTitle <- paste("Polarity CDF -",dim(inputData)[1],"tweets")
plot(ecdf(inputData$Polarity),col="orange",xlab="Polarity value",main=graphTitle)

#Plot histogram representing mood distributions
graphTitle <- paste("Polarity distribution across",dim(inputData)[1],"tweets")
hist(inputData$Polarity,xlab="Polarity values",col="orange",main=graphTitle)

#Plot empirical CDF of tweet subjectivity
graphTitle <- paste("Subjectivity CDF -", dim(inputData)[1],"tweets")
plot(ecdf(inputData$Subjectivity),col="green",xlab="Subjectivity value",main=graphTitle)

#Plot histogram representing subjectivity distributions
graphTitle <- paste("Subjectivity distribution across", dim(inputData)[1],"tweets")
hist(inputData$Subjectivity,xlab="Subjectivity values",col="green",main=graphTitle)

#Scatterplot subjectivity - polarity
graphTitle <- paste("Subjectivity-Polarity scatterplot -", dim(inputData)[1], "tweets")
plot(x=inputData$Polarity,y=inputData$Subjectivity,
     xlab="Polarity values",ylab="Subjectivity values",
     col="blue",pch=20,main=graphTitle)


moodTable <- table(inputData$Mood)
labelList <- paste(names(moodTable), "\n", moodTable, sep="")
pie(moodTable, labels = labelList, col=rainbow(length(labelList)), 
    main="Pie Chart of Mood types\n (with tweet number)")
dev.off()
