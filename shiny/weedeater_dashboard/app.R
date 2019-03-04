
# Set-Up ------------------------------------------------------------------


library(shiny)
library(shinySignals)   # devtools::install_github("hadley/shinySignals")
library(dplyr)
library(shinydashboard)
library(plotly)  
library(stringr)
library(tidyverse)
library(reticulate)
library(purrr)
library(ggmap)
library(DT)
library(leaflet)
library(maps)
library(lubridate)
library(sp)
library(rworldmap)
library(jsonlite)

source("helpers.R")


# Setup -------------------------------------------------------------------
size <- 100
link <-
  paste0(
    "https://weedsample.herokuapp.com/return_sample_data/sim/",
    size,
    ".json"
  )
df <- jsonlite::fromJSON(link)

df[1:((size/2)),c("lon","lat")] <- cbind(rnorm(size/2,(-117.848974 + -100) / 2, 4),rnorm(size/2,(32 + 40) / 2), 2)  
df[((size/2)+1):nrow(df),c("lon","lat")] <- cbind(rnorm(size/2,(17 + 47) / 2, 3),rnorm(size/2,(0 + 10) / 2), 2)
df[sample(1:nrow(df), size/3),c("lon","lat")] <- cbind(rnorm(size/3,(1 + 37) / 2, 3),rnorm(size/3,(15 + 10) / 2), 2)
df[sample(1:nrow(df), size/4),c("lon","lat")] <- cbind(rnorm(size/4,(-100) / 2, 3),rnorm(size/4,(-40) / 2), 2)

df <- df %>%
  mutate(timestamp = ymd_hms(str_replace(timestamp,"T|z"," ")))

df$continent <- coords2continent(df[,c("lon","lat")])
df$country <- coords2country(df[,c("lon","lat")])


# UI ----------------------------------------------------------------------
ui <- dashboardPage(
  dashboardHeader(title = "Weedeater Organization App"),
  dashboardSidebar(
    width = 300,
    h3("Dashboard Filters"),
    sliderInput("usage_points",
                "Number of usage points:",
                min = 1,
                max = 1000,
                value = 100),
    checkboxGroupInput("continent",
                       label = "Continents:",
                       choices = unique(as.character(df$continent)),
                       selected = unique(as.character(df$continent))),
    
    dropdownButton("Countries:",
                   status = "default", width = 80,
      checkboxGroupInput("country",
                label = "Countries:",
                choices = unique(as.character(df$country)),
                selected = unique(as.character(df$country))
                )),
    br(),
    sidebarMenu(
      menuItem("Global Usage", tabName = "dashboard"),
      menuItem("Raw data", tabName = "rawdata")
    )
  ),
  dashboardBody(
    tabItems(
      tabItem("dashboard",
              fluidRow(
                valueBoxOutput("rate", width = 3),
                valueBoxOutput("count", width = 3),
                valueBoxOutput("ratio", width = 3),
                valueBoxOutput("users", width = 3)
              ),
              fluidRow(
                box(
                  width = 8, status = "info", solidHeader = TRUE,
                  title = "Global Usage Points",
                  fluidRow(
                    column(6, leafletOutput("packagePlot", width = "100%", height = 600)),
                    column(6, 
                           fluidRow(plotlyOutput("packageChart", width = "100%", height = 350)),
                           fluidRow(plotlyOutput("barchart", width = "100%", height = 250)))
                  )
                  
                ),
                box(
                  width = 4, status = "info",
                  title = "Complete dataset:",
                  downloadButton("downloadCsv", "Download as CSV"),
                  h4("Sample of data selected:"),
                  dataTableOutput("packageTable")
                )
              )
      ),
      tabItem("rawdata",
              numericInput("maxrows", "Rows to show", 25),
              verbatimTextOutput("rawtable"),
              downloadButton("downloadCsv2", "Download as CSV")
      )
    )
  )
)

server <- function(input, output, session) {
  

# Value Boxes -------------------------------------------------------------

  observe({
    print(input$continent)
    countries <- unique(as.character(df$country[df$continent %in% input$continent]))
    updateCheckboxGroupInput(session, "country",
                             choices = countries,
                             selected = countries)
  })
  
  output$rate <- renderValueBox({
   
    val <- values[["df"]]
    val <- mean(val$pump_time, na.rm = T)
      
    
    valueBox(
      value = prettyNum(round(val,2), big.mark = ","),
      subtitle = "Pump Time Per Day",
      icon = icon("area-chart"),
      color = "aqua"
    )
  })
  
  output$count <- renderValueBox({
    
    val <- values[["df"]]
    val <- sum(val$pump_time, na.rm = T)
    
    valueBox(
      value = prettyNum(round(val,2), big.mark = ","),
      subtitle = "Total Pump Time",
      icon = icon("calendar")
    )
  })
  
  output$users <- renderValueBox({
    val <- values[["df"]]
    val <- n_distinct(val$serial_number)
    
    valueBox(
      prettyNum(round(val,2), big.mark = ","),
      "Unique users",
      icon = icon("users")
    )
  })
  
  output$ratio <- renderValueBox({
    val <- values[["df"]]
    crop <- sum(val$radish) + sum(val$pea)
    weed <- sum(val$marigold) + sum(val$morning_glory)
    val <- weed/crop
    
    valueBox(
      prettyNum(round(val,2), big.mark = ","),
      "Weed/Crop Ratio",
      icon = icon("paper-plane")
    )
  })
  
  

# Map ---------------------------------------------------------------------

  values <- reactiveValues()
  
  output$packagePlot <- renderLeaflet({
    size <- input$usage_points
    link <-
      paste0(
        "https://weedsample.herokuapp.com/return_sample_data/sim/",
        size,
        ".json"
      )
    df <- jsonlite::fromJSON(link)
    
    df[1:((size/2)),c("lon","lat")] <- cbind(rnorm(size/2,(-117.848974 + -100) / 2, 4),rnorm(size/2,(32 + 40) / 2), 2)  
    df[((size/2)+1):nrow(df),c("lon","lat")] <- cbind(rnorm(size/2,(17 + 47) / 2, 3),rnorm(size/2,(0 + 10) / 2), 2)
    df[sample(1:nrow(df), size/3),c("lon","lat")] <- cbind(rnorm(size/3,(1 + 37) / 2, 3),rnorm(size/3,(15 + 10) / 2), 2)
    df[sample(1:nrow(df), size/4),c("lon","lat")] <- cbind(rnorm(size/4,(-100) / 2, 3),rnorm(size/4,(-40) / 2), 2)
    
    df <- df %>%
      mutate(timestamp = ymd_hms(str_replace(timestamp,"T|z"," ")))
    
    df$continent <- coords2continent(df[,c("lon","lat")])
    df$country <- coords2country(df[,c("lon","lat")])
    
    df <- df %>%
      filter(continent %in% input$continent,
             country %in% input$country)
    
    values[["df"]] <- df

      small <- 3
      greenLeafIcon <- makeIcon(
        iconUrl = "http://leafletjs.com/examples/custom-icons/leaf-green.png",
        iconWidth = 38/small, iconHeight = 95/small,
        iconAnchorX = 22/small, iconAnchorY = 94/small,
        shadowUrl = "http://leafletjs.com/examples/custom-icons/leaf-shadow.png",
        shadowWidth = 50/small, shadowHeight = 64/small,
        shadowAnchorX = 4/small, shadowAnchorY = 62/small
      )
      
      leaflet(data = df) %>%
        addProviderTiles(providers$OpenStreetMap) %>%
        addMarkers(~lon, ~lat,
                   popup = paste("Country:", df$country, "<br>",
                                 "Pump Time:", df$pump_time, "<br>",
                                 "Radishes:", df$radish, "<br>",
                                 "Peas:", df$pea, "<br>",
                                 "Marigolds:", df$marigold, "<br>",
                                 "Morning Glories:", df$morning_glory, "<br>",
                                 "Unidentified:", df$unidentified),
                   icon = greenLeafIcon)
      
      
      
  })
  

# Time Plot ---------------------------------------------------------------
output$packageChart <- renderPlotly({
  df <- values[["df"]]
  
  val <- "pump_time"
  
  df_p <- df %>%
    mutate(day = ymd(word(as.character(timestamp),1)))
  df_p$val <- df_p[[val]]
  
  p <- df_p %>%
    group_by(day, continent) %>%
    summarise(val = mean(val, na.rm = T)) %>%
    ungroup() %>%
    rename(Continent = continent) %>%
    ggplot(aes(day, val, group = Continent, fill = Continent, color = Continent)) +
    geom_point() +
    geom_line() +
    theme_bw() +
    labs(
      title = paste0("'",val, "' Over Time"),
      x = "Day",
      y = ""
    )+ 
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
    facet_wrap(~Continent, ncol = 1)
  
  ggplotly(p)
})


# Bar Chart ---------------------------------------------------------------

  output$barchart <- renderPlotly({
    df <- values[["df"]]
    
    df <- df %>%
      select(-serial_number,-lon, -lat, -timestamp, -pump_time, -country) %>%
      gather(key, val, -continent) %>%
      group_by(key, continent) %>%
      summarize(val = sum(val, na.rm = T))
    
    p <- df %>%
      mutate(Continent = continent) %>%
      ggplot(aes(key, val, fill = Continent)) +
      geom_bar(stat = "identity", color = "black", position = "dodge") +
      labs(title = "Distribution by Plant/Weed Type",
           x = "Identified Species",
           y = "Total Count") +
      theme_bw()+ 
      theme(axis.text.x = element_text(angle = 45, hjust = 1))
    
    ggplotly(p)
  })
  

# Data Table Sample -------------------------------------------------------

  output$packageTable <- renderDataTable({
    datatable(values[["df"]] %>%
      select(serial_number, radish, pea, marigold, morning_glory, unidentified, pump_time) %>%
      head(10),
      options = list(dom = 't'))
  })
  

# Download CSV ------------------------------------------------------------

  output$downloadCsv <- downloadHandler(
    filename = "log.csv",
    content = function(file) {
      write.csv(values[["df"]], file)
    },
    contentType = "text/csv"
  )
  
}


# Run App -----------------------------------------------------------------

shinyApp(ui = ui, server = server)