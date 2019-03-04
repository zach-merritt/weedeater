size <- 100
link <-
  paste0(
    "https://weedsample.herokuapp.com/return_sample_data/sim/",
    size,
    ".json"
  )
df <- jsonlite::fromJSON(link)

df <- df %>%
  mutate(timestamp = ymd_hms(str_replace(timestamp,"T|z"," ")))


small <- 3
greenLeafIcon <- makeIcon(
  iconUrl = "http://leafletjs.com/examples/custom-icons/leaf-green.png",
  iconWidth = 38/small, iconHeight = 95/small,
  iconAnchorX = 22/small, iconAnchorY = 94/small,
  shadowUrl = "http://leafletjs.com/examples/custom-icons/leaf-shadow.png",
  shadowWidth = 50/small, shadowHeight = 64/small,
  shadowAnchorX = 4/small, shadowAnchorY = 62/small
)

df[1:((size/2)),c("lon","lat")] <- cbind(runif(size/2,-117.848974, -100),runif(size/2,32, 40))  
df[((size/2)+1):nrow(df),c("lon","lat")] <- cbind(runif(size/2,17, 47),runif(size/2,0, 10))  

leaflet(data = df) %>%
  addProviderTiles(providers$Wikimedia) %>%
  addMarkers(~lon, ~lat,
             popup = paste("Pump Time:", df$pump_time, "<br>",
                           "Radishes:", df$radish, "<br>",
                           "Peas:", df$pea, "<br>",
                           "Marigolds:", df$marigold, "<br>",
                           "Morning Glories:", df$morning_glory, "<br>",
                           "Unidentified:", df$unidentified),
             icon = greenLeafIcon)
