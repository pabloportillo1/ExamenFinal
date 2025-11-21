import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

@dataclass
class Customer:
    name: str
    email: str
    phone: str
    device_id: str

@dataclass
class Order:
    order_id: str
    customer: Customer
    total: float
  
# Strategy: estrategias de envío de notificaciones

class NotificationSender(ABC):
    """Interfaz para cualquier tipo de envío de notificación."""

    @abstractmethod
    def send(self, order: Order) -> Dict:
        """Envía la notificación y devuelve el registro generado."""
        raise NotImplementedError

class EmailNotificationSender(NotificationSender):
    def send(self, order: Order) -> Dict:
        message = (
            f"Estimado {order.customer.name}, "
            f"su pedido #{order.order_id} por ${order.total} ha sido confirmado."
        )
        print(f" EMAIL enviado a {order.customer.email}")
        print(f" Asunto: Confirmación de Pedido #{order.order_id}")
        print(f" Mensaje: {message}\n")

        return {
            "type": "email",
            "to": order.customer.email,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }

class SmsNotificationSender(NotificationSender):
    def send(self, order: Order) -> Dict:
        message = (
            f"Pedido #{order.order_id} confirmado. "
            f"Total: ${order.total}. Gracias por su compra!"
        )
        print(f" SMS enviado a {order.customer.phone}")
        print(f" Mensaje: {message}\n")

        return {
            "type": "sms",
            "to": order.customer.phone,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }

class PushNotificationSender(NotificationSender):
    def send(self, order: Order) -> Dict:
        message = f"¡Pedido confirmado! #{order.order_id} - ${order.total}"
        print(f" PUSH enviada al dispositivo {order.customer.device_id}")
        print(f" Mensaje: {message}\n")

        return {
            "type": "push",
            "to": order.customer.device_id,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }

# Factory Method: crea la estrategia correcta

class NotificationFactory:
    """Factory Method para crear NotificationSender según el tipo."""

    _registry = {
        "email": EmailNotificationSender,
        "sms": SmsNotificationSender,
        "push": PushNotificationSender,
    }

    @classmethod
    def create_sender(cls, notif_type: str) -> NotificationSender:
        sender_class = cls._registry.get(notif_type)
        if not sender_class:
            raise ValueError(f"Tipo de notificación no soportado: {notif_type}")
        return sender_class()

# Orquestador principal (alta cohesión, bajo acoplamiento)

class OrderNotificationSystem:
    def __init__(self, factory: NotificationFactory | None = None):
        self.notifications_sent: List[Dict] = []
        # DIP: depende de la abstracción (factory), se puede inyectar una factory distinta.
        self._factory = factory or NotificationFactory()

    def process_order(self, order: Order, notification_types: List[str]) -> None:
        """Procesa un pedido y envía notificaciones usando estrategias configurables."""
        print(f"\n{'=' * 50}")
        print(f"Procesando pedido #{order.order_id}")
        print(f"Cliente: {order.customer.name}")
        print(f"Total: ${order.total}")
        print(f"{'=' * 50}\n")

        for notif_type in notification_types:
            sender = self._factory.create_sender(notif_type)
            notification_record = sender.send(order)
            self.notifications_sent.append(notification_record)

    def get_notification_history(self) -> List[Dict]:
        """Devuelve el historial de notificaciones enviadas."""
        return self.notifications_sent


if __name__ == "__main__":
    system = OrderNotificationSystem()

    order1 = Order(
        order_id="ORD-001",
        customer=Customer(
            name="Ana García",
            email="ana.garcia@email.com",
            phone="+34-600-123-456",
            device_id="DEVICE-ABC-123",
        ),
        total=150.50,
    )

    system.process_order(order1, ["email", "sms", "push"])

    order2 = Order(
        order_id="ORD-002",
        customer=Customer(
            name="Carlos Ruiz",
            email="carlos.ruiz@email.com",
            phone="+34-600-789-012",
            device_id="DEVICE-XYZ-789",
        ),
        total=75.00,
    )

    system.process_order(order2, ["email"])

    print("\n" + "=" * 50)
    print("HISTORIAL DE NOTIFICACIONES")
    print("=" * 50)
    print(json.dumps(system.get_notification_history(), indent=2, ensure_ascii=False))
