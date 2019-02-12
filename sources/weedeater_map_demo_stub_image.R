#
# code to generate map in R
#
library(jsonlite)
library(imager)

df <- fromJSON("https://weedsample.herokuapp.com/return_sample_images/SPRAYER0002.json")

image_url <- df$url[2] #there are two image URLs on SPRAYER0002, could pick either one of them.

jj <- load.image(image_url)
plot(jj)


