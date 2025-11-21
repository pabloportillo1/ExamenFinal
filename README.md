# ExamenFinal

Ejercicio 1
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

