#Read command line arguments
args <- commandArgs(trailingOnly = TRUE)
statsFile <- args[1]
wordsFile <- args[2]
rm(args)


#Read data from stats file
inputData <- read.table(statsFile, header = TRUE)

pdf(paste(inputFile,".pdf",sep=""))

#Plot empirical CDF of tweet length
graphTitle <- paste("Length CDF -",dim(inputData)[1],"tweets")
plot(ecdf(inputData$Length),col="orange",xlab="Polarity value",main=graphTitle)

#Plot histogram representing tweet lengths
graphTitle <- paste("Length distribution across",dim(inputData)[1],"tweets")
hist(inputData$Length,xlab="Length values",col="orange",main=graphTitle)

#Plot empirical CDF of tweet polarity
graphTitle <- paste("Polarity CDF -",dim(inputData)[1],"tweets")
plot(ecdf(inputData$Polarity),col="orange",xlab="Polarity value",main=graphTitle)

#Plot histogram representing polarity distribution
graphTitle <- paste("Polarity distribution across",dim(inputData)[1],"tweets")
hist(inputData$Polarity,xlab="Polarity values",col="orange",main=graphTitle)

#Plot empirical CDF of tweet subjectivity
graphTitle <- paste("Subjectivity CDF -", dim(inputData)[1],"tweets")
plot(ecdf(inputData$Subjectivity),col="green",xlab="Subjectivity value",main=graphTitle)

#Plot histogram representing subjectivity distribution
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

report <- data.frame()
report["Polarity","Mean"] <- mean(inputData["Polarity"])
report["Subjectivity","Mean"] <- mean(inputData["Subjectivity"])
report["Polarity","Standard Deviation"] <- sd(inputData["Polarity"])
report["Subjectivity","Standard Deviation"] <- sd(inputData["Subjectivity"])
report["Polarity","Median"] <- median(inputData["Polarity"])
report["Subjectivity","Median"] <- median(inputData["Subjectivity"])
report["Polarity","Min"] <- min(inputData["Polarity"])
report["Subjectivity","Min"] <- min(inputData["Subjectivity"])
report["Polarity","Max"] <- max(inputData["Polarity"])
report["Subjectivity","Max"] <- max(inputData["Subjectivity"])

#Write reporting dataframe
write.table(report, paste(inputFile,".summary",sep=""),sep="\t",row.names=TRUE,col.names=TRUE)


#Read data and compute errors for each cluster
wordsData <- read.table(wordsFile, header = TRUE)

#Wordcloud - Style 1
#png(paste(wordsFile,".cloud.png",sep=""), width=1280,height=800)
#wordcloud(wordsData$Words,wordsData$Frequency, scale=c(8,.3),min.freq=2,max.words=100, random.order=T, rot.per=.15, colors=pal, vfont=c("sans serif","plain"))
#dev.off()

#Wordcloud - Style 2
png(paste(wordsFile,".cloud.png",sep=""), width=1280,height=800)
wordcloud(wordsData$Words,wordsData$Frequency, scale=c(8,.2),min.freq=3,
          max.words=Inf, random.order=FALSE, rot.per=.15, colors=pal2)
dev.off()