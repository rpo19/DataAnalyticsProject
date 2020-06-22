library(sentix)

model <- load.udpipe()

dataReviews_NEG = read.csv("../data/dataReviews_NEG.csv")  # read csv file 
sentiment_NEG = sentix.df.sentiment(dataReviews_NEG$body, model)

dataReviews_POS = read.csv("../data/dataReviews_POS.csv")  # read csv file 
sentiment_POS = sentix.df.sentiment(dataReviews_POS$body, model)

dataReviews_NEUT = read.csv("../data/dataReviews_NEUT.csv")  # read csv file 
sentiment_NEUT = sentix.df.sentiment(dataReviews_NEUT$body, model)