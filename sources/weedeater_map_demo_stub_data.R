#
# code to generate map in R
#
library(jsonlite)
library(ggplot2)
library(ggmap)

df <- fromJSON("https://weedsample.herokuapp.com/return_sample_data/sim/30.json")

lon.center = mean(df$lon)
lat.center = mean(df$lat)
margin = 0.1
bbox.c = c(left = lon.center-margin, bottom = lat.center-margin,
           right = lon.center+margin, top = lat.center+margin)

m <-get_stamenmap( bbox = bbox.c,
                   zoom = 11)

df.pea <- df[df$pea > df$radish,]
df.radish <- df[df$radish > df$pea,]

ggmap(m) + geom_point(data=df.radish, aes(x = lon, y = lat, fill = "Radish"), size = 2, shape = 21) +
           geom_point(data=df.pea, aes(x = lon, y = lat, fill = "Pea"), size = 2, shape = 21)
           
