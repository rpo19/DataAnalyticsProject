# install.packages(c("udpipe", "dplyr", "https://github.com/valeriobasile/sentixR/raw/master/sentix_0.0.0.9000.tar.gz"))
library(sentix)



compute_sentix <- function(df, model) {
  df_polarity = sentix.df.sentiment(df$body, model)
  df_polarity$doc_id = factor(df_polarity$doc_id)
  df$X_id = NULL
  ret = data.frame(df)
  i = 1
  for (level in levels(df_polarity$doc_id)) {
    ret[i, 'polarity'] = head(df_polarity[df_polarity$doc_id == level, 'sentimentXdoc'], 1)$sentimentXdoc
    i = i + 1
  }  
  
  return(ret)
}

# load model
model <- load.udpipe()

# compute negative 
print("compute negative")
dataReviews_NEG = read.csv("../data/dataReviews_NEG.csv", stringsAsFactors=FALSE, sep = ',')  # read csv file 
sentiment_NEG = compute_sentix(dataReviews_NEG, model)
write.csv(sentiment_NEG, "../data/dataReviews_NEG_pol.csv", row.names=FALSE)

# compute positive
print("compute positive")
dataReviews_POS = read.csv("../data/dataReviews_POS.csv", stringsAsFactors=FALSE, sep = ',')  # read csv file 
sentiment_POS = compute_sentix(dataReviews_POS, model)
write.csv(sentiment_POS, "../data/dataReviews_POS_pol.csv", row.names=FALSE)