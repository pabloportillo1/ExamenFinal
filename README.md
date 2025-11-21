# ExamenFinal

Ejercicio 1 - ejercicio1_tienda_online.py
 I. Principios SOLID aplicados:

  1. Single Responsibility Principle :
  
   Cada clase tiene una responsabilidad clara:
    
   EmailNotificationSender, SmsNotificationSender, PushNotificationSender : todas envian unicamente un solo tipo de notificación.
    
   OrderNotificationSystem : maneja el proceso del pedido y registra el historial.
    
   NotificationFactory : crea el sender correcto.
    
  2. Open/Closed  y Dependency Inversion Principles:
    
   OrderNotificationSystem depende de la abstracción NotificationSender (no de clases concretas).
    
   Para agregar un nuevo canal solo hay que crear una nueva clase e inscribir el tipo en la NotificationFactory, sin modificar la lógica principal.
    
II. Patrones de diseño aplicados
    
  1. Strategy (comportamental)
    
   Cada NotificationSender es una estrategia distinta para el envío (email, sms, push).
    
  2. Factory Method (creacional)
    
   NotificationFactory.create_sender(tipo) crea la instancia correcta de la estrategia, a partir de un string ("email", "sms", "push").

Ejercicio 2 – ejercicio2_gestor_documentos.py

 I. Principios : SOLID aplicados

  1. SRP (Single Responsibility Principle)

   SalesReportGenerator, InventoryReportGenerator, FinancialReportGenerator solo generan contenido.

   PDFFormatter, ExcelFormatter, HTMLFormatter solo formatean.

   EmailDelivery, DownloadDelivery, CloudDelivery solo entregan.

   ReportSystem coordina el flujo : genera despues formatea y enseguida entrega, finalmente guarda el historial.

  2. Open/Closed y Dependency Inversion

   Nuevos tipos de reportes, formatos o métodos de entrega se agregan creando nuevas clases que implementen las interfaces, sin modificar ReportSystem.
   
   ReportSystem trabaja con abstracciones: ReportGenerator, ReportFormatter, ReportDelivery.

 II. Patrones de diseño aplicados
   
  1. Strategy (comportamental)
   
   Estrategia de generación (ReportGenerator), de formato (ReportFormatter) y de entrega (ReportDelivery).
   
  2. Factory Method (creacional)

   ReportFactory devuelve el generador, formateador y método de entrega adecuados según los strings ("sales", "pdf", "email", etc.).

