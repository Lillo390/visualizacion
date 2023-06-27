
library(shiny)
library(rsconnect)
library(shinythemes)
library(plotly)
library(dplyr)
library(ggplot2)
library(lubridate)



ui<-navbarPage(theme = shinytheme("slate"),
               "App Master Ciencia de datos", 
               tabPanel("Selección de máquina", fluidPage(
                 
                 sidebarLayout(
                   
                   sidebarPanel(
                     p("MAQUINA"), 
                     fileInput("DatosFichero", "Selecciona un fichero", accept = NULL),
                     uiOutput('SelectMachine')),
                   
                   mainPanel("Probabilidad de orden",
                     plotOutput("p_orden"),
                   )
                 )
               )
               
               ),
               navbarMenu("Estado de la máquina",
                          tabPanel("Evolución temporal alarmas",
                                   sidebarPanel(
                                     p("Alarmas RadioButtons"),
                                     uiOutput("AlarmRadioButtons")
                                   ),
                                   mainPanel(
                                     plotOutput("AlarmEv")
                                   )
                          ), 
                          tabPanel("Registros de la máquina",
                                   fluidRow(
                                     column(width = 4,
                                            sidebarPanel(
                                              p("Alarmas checkbox"),
                                              uiOutput("AlarmCheckbox"),
                                              checkboxGroupInput("CheckBoxAlarm", "")
                                            )
                                     ),
                                     column(width = 8,
                                            dataTableOutput('table')
                                     )
                                   )
                          )
               )
               ,
               
               tabPanel("Estadísticos Globales Temporales",
                        sidebarLayout(
                          sidebarPanel(p("PERIODO Y ESTADÍSTICOS"),
                                       dateRangeInput("rango_fechas", "Rango de fechas", start = "2016-01-02", end ="2016-12-14", format = "yyyy-mm-dd", separator= "a",language = "es"),      
                                       
                                       uiOutput("SelectAlarm"),
                                       
                                       sliderInput("slider_bins", label = h3("Selecciona la anchura de las bins del histograma"), 
                                                   min= 1, max = 30, value = 10, step= 1),
                                       p("BOXPLOT"),
                                       checkboxInput("Todas_alarmas", "Todas las alarmas", 
                                                     value = FALSE, width = NULL)
                                       
                                       
                                       
                          ),
                          mainPanel(h5("Histograma de la alarma seleccionada"),plotOutput("Histograma"),
                                    h5("Boxplot de la alarma seleccionada"), plotOutput("Boxplot"))
                        )),
               
)

server <- function(input, output) { 
  
  datos<-reactive({
    a<-input$DatosFichero
    req(a)
    nombre_df<-load(a$datapath)
    Datos<-eval(parse(text=nombre_df))
    return(Datos)
  })

  output$SelectMachine <- renderUI({
    tagList(selectInput("SelMach","Selecciona una máquina", unique(datos()[["matricula"]])))
  })
  
  
  output$AlarmRadioButtons <- renderUI({
    radioButtons("SelAl","Selecciona una alarma para la visualización", names(datos())[4:48])
  })
  
  output$AlarmCheckbox <- renderUI({
    checkboxGroupInput("CheckAl","Selecciona las alarmas presentes en la tabla", names(datos())[4:48])
  })
  
  output$SelectAlarm <- renderUI({ selectInput("SelAl2","Alarma",names(datos())[4:48]) })
  
  output$table <- renderDataTable(datos()[c("matricula","dia",input$CheckAl,"p_orden")])
  
  
  output$p_orden <- renderPlot({
    ggplot(dplyr::filter(datos(),matricula == input$SelMach), aes(x = dia, y = p_orden,color=p_orden)) +
      geom_line() +
      geom_point() +scale_color_gradient(low = "blue", high = "red")+
      labs(x = "Dia", y = "p_orden", title = "Probabilidad de orden")
  })
  
  output$AlarmEv <- renderPlot({
    data <- dplyr::filter(datos(),matricula == input$SelMach)
    print(typeof(data))
    ggplot(data, aes_string(x = 'dia', y = input$SelAl)) +
      geom_line() +
      geom_point() +
      labs(x = "Dia", y = input$SelAl)
  })
  
  output$Boxplot <- renderPlot({
    if(input$Todas_alarmas == F){
    data <- datos() %>% dplyr::filter(matricula==input$SelMach,dia <= input$rango_fechas[2] & dia >= input$rango_fechas[1])
    data_y <- data[,input$SelAl2]
    ggplot(data=data,aes(x=factor(matricula),y=data_y)) + geom_boxplot() +
      labs(x="matricula",y='eval(ALA)')}else{
        data <- datos() %>% dplyr::filter(dia <= input$rango_fechas[2] & dia >= input$rango_fechas[1])
        data_y <- data[,input$SelAl2]
        ggplot(data=data,aes(x=factor(matricula),y=data_y)) + geom_boxplot() +
          labs(x="matricula",y='eval(ALA)')
        
      }
  
  })
  
  
  output$Histograma <- renderPlot({
    data <- datos() %>% dplyr::filter(matricula==input$SelMach,dia <= input$rango_fechas[2] & dia >= input$rango_fechas[1])
    ggplot(data = data, aes_string(x = input$SelAl2))+geom_histogram(binwidth = input$slider_bins) + labs(x=input$SelAl2,y='count')
    
  })
    
  }

shinyApp(ui, server)