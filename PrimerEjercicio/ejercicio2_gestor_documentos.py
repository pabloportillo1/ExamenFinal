from abc import ABC, abstractmethod
from datetime import datetime
import json
from typing import Dict, List


# Estrategias de generación de contenido

class ReportGenerator(ABC):
    @abstractmethod
    def generate(self, data: Dict) -> str:
        raise NotImplementedError


class SalesReportGenerator(ReportGenerator):
    def generate(self, data: Dict) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = "=" * 60 + "\n"
        content += " REPORTE DE VENTAS\n"
        content += "=" * 60 + "\n"
        content += f"Fecha de generación: {timestamp}\n\n"
        total_sales = sum(item["amount"] for item in data["sales"])
        content += f"Total de ventas: ${total_sales:.2f}\n"
        content += f"Número de transacciones: {len(data['sales'])}\n"
        content += f"Periodo: {data['period']}\n\n"
        content += "Detalle de ventas:\n"
        content += "-" * 60 + "\n"
        for sale in data["sales"]:
            content += f" • Producto: {sale['product']} - ${sale['amount']:.2f}\n"
        return content


class InventoryReportGenerator(ReportGenerator):
    def generate(self, data: Dict) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = "=" * 60 + "\n"
        content += " REPORTE DE INVENTARIO\n"
        content += "=" * 60 + "\n"
        content += f"Fecha de generación: {timestamp}\n\n"
        total_items = sum(item["quantity"] for item in data["items"])
        content += f"Total de productos: {total_items}\n"
        categories = len(set(item["category"] for item in data["items"]))
        content += f"Categorías: {categories}\n\n"
        content += "Inventario actual:\n"
        content += "-" * 60 + "\n"
        for item in data["items"]:
            content += (
                f" • {item['name']} ({item['category']}): "
                f"{item['quantity']} unidades\n"
            )
        return content


class FinancialReportGenerator(ReportGenerator):
    def generate(self, data: Dict) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = "=" * 60 + "\n"
        content += " REPORTE FINANCIERO\n"
        content += "=" * 60 + "\n"
        content += f"Fecha de generación: {timestamp}\n\n"
        content += f"Ingresos: ${data['income']:.2f}\n"
        content += f"Gastos: ${data['expenses']:.2f}\n"
        content += f"Balance: ${data['income'] - data['expenses']:.2f}\n"
        return content


# Estrategias de formato

class ReportFormatter(ABC):
    @abstractmethod
    def format(self, content: str) -> str:
        raise NotImplementedError


class PDFFormatter(ReportFormatter):
    def format(self, content: str) -> str:
        print(" Generando reporte en formato PDF...")
        return f"[PDF FORMAT]\n{content}\n[END PDF]"


class ExcelFormatter(ReportFormatter):
    def format(self, content: str) -> str:
        print(" Generando reporte en formato Excel...")
        return f"[EXCEL FORMAT]\n{content}\n[END EXCEL]"


class HTMLFormatter(ReportFormatter):
    def format(self, content: str) -> str:
        print(" Generando reporte en formato HTML...")
        return f"<html><body><pre>{content}</pre></body></html>"


# Estrategias de entrega

class ReportDelivery(ABC):
    @abstractmethod
    def deliver(self, formatted: str, report_type: str, output_format: str) -> None:
        raise NotImplementedError


class EmailDelivery(ReportDelivery):
    def deliver(self, formatted: str, report_type: str, output_format: str) -> None:
        print(" Enviando reporte por email...")
        print(" Destinatario: admin@company.com")


class DownloadDelivery(ReportDelivery):
    def deliver(self, formatted: str, report_type: str, output_format: str) -> None:
        filename = (
            f"report_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}."
            f"{output_format}"
        )
        print(f" Reporte disponible para descarga: {filename}")


class CloudDelivery(ReportDelivery):
    def deliver(self, formatted: str, report_type: str, output_format: str) -> None:
        print(" ☁️ Subiendo reporte a la nube...")
        print(f" URL: https://cloud.company.com/reports/{report_type}")


# Factory Method: crea las estrategias necesarias

class ReportFactory:
    GENERATORS = {
        "sales": SalesReportGenerator,
        "inventory": InventoryReportGenerator,
        "financial": FinancialReportGenerator,
    }

    FORMATTERS = {
        "pdf": PDFFormatter,
        "excel": ExcelFormatter,
        "html": HTMLFormatter,
    }

    DELIVERIES = {
        "email": EmailDelivery,
        "download": DownloadDelivery,
        "cloud": CloudDelivery,
    }

    @classmethod
    def get_generator(cls, report_type: str) -> ReportGenerator:
        generator_class = cls.GENERATORS.get(report_type)
        if not generator_class:
            raise ValueError(f"Tipo de reporte no soportado: {report_type}")
        return generator_class()

    @classmethod
    def get_formatter(cls, output_format: str) -> ReportFormatter:
        formatter_class = cls.FORMATTERS.get(output_format)
        if not formatter_class:
            raise ValueError(f"Formato de salida no soportado: {output_format}")
        return formatter_class()

    @classmethod
    def get_delivery(cls, delivery_method: str) -> ReportDelivery:
        delivery_class = cls.DELIVERIES.get(delivery_method)
        if not delivery_class:
            raise ValueError(f"Método de entrega no soportado: {delivery_method}")
        return delivery_class()


# Sistema principal

class ReportSystem:
    def __init__(self, factory: ReportFactory | None = None):
        self.reports_generated: List[Dict] = []
        self._factory = factory or ReportFactory

    def generate_report(
        self,
        report_type: str,
        data: Dict,
        output_format: str,
        delivery_method: str,
    ) -> str:
        """Genera, formatea y entrega un reporte usando estrategias configurables."""
        generator = self._factory.get_generator(report_type)
        formatter = self._factory.get_formatter(output_format)
        delivery = self._factory.get_delivery(delivery_method)

        content = generator.generate(data)
        formatted_report = formatter.format(content)
        delivery.deliver(formatted_report, report_type, output_format)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.reports_generated.append(
            {
                "type": report_type,
                "format": output_format,
                "delivery": delivery_method,
                "timestamp": timestamp,
            }
        )

        print("\n✅ Reporte generado exitosamente\n")
        print(formatted_report)
        print("\n" + "=" * 60 + "\n")
        return formatted_report

    def get_report_history(self) -> List[Dict]:
        return self.reports_generated


# Código de prueba (main)

if __name__ == "__main__":
    system = ReportSystem()

    # Reporte de ventas
    sales_data = {
        "period": "Enero 2024",
        "sales": [
            {"product": "Laptop HP", "amount": 899.99},
            {"product": "Mouse Logitech", "amount": 25.50},
            {"product": "Teclado Mecánico", "amount": 120.00},
            {"product": 'Monitor LG 24"', "amount": 199.99},
        ],
    }
    system.generate_report("sales", sales_data, "pdf", "email")

    # Reporte de inventario
    inventory_data = {
        "items": [
            {"name": "Laptop HP", "category": "Computadoras", "quantity": 15},
            {"name": "Mouse Logitech", "category": "Accesorios", "quantity": 50},
            {"name": "Teclado Mecánico", "category": "Accesorios", "quantity": 30},
            {"name": "Monitor LG", "category": "Pantallas", "quantity": 20},
        ]
    }
    system.generate_report("inventory", inventory_data, "excel", "download")

    # Reporte financiero
    financial_data = {"income": 50000.00, "expenses": 32000.00}
    system.generate_report("financial", financial_data, "html", "cloud")

    print("\nHISTORIAL DE REPORTES GENERADOS:")
    print(json.dumps(system.get_report_history(), indent=2, ensure_ascii=False))
