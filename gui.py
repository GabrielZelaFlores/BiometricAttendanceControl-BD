from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, 
    QLabel, QMessageBox, QTableWidget, QTableWidgetItem
)
import sys
from db_connection import get_connection
import datetime


# ---------------------------------------------------------
# FUNCIONES DE BASE DE DATOS
# ---------------------------------------------------------
def registrar_marcacion(empleado_id, tipo):
    conn = get_connection()
    if not conn:
        return "❌ Error al conectar"

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO marcaciones (empleado_id, tipo, fecha_hora, origen)
            VALUES (%s, %s, NOW(), 'GUI')
        """, (empleado_id, tipo))
        conn.commit()
        return "✔ Marcación registrada"

    except Exception as e:
        conn.rollback()
        return f"❌ Error: {e}"

    finally:
        conn.close()


def obtener_tabla(query):
    conn = get_connection()
    if not conn:
        return []

    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows


# ---------------------------------------------------------
# INTERFAZ
# ---------------------------------------------------------
class BiometricSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Biometric Attendance Control - QT")
        self.setGeometry(200, 200, 600, 500)

        layout = QVBoxLayout()

        # ------- Etiqueta -------
        self.label = QLabel("Sistema de Control de Asistencia Biométrica", self)
        layout.addWidget(self.label)

        # ------- Botones -------
        btn_entrada = QPushButton("Registrar Entrada")
        btn_salida = QPushButton("Registrar Salida")
        btn_reporte = QPushButton("Reporte de Asistencia")
        btn_tardanzas = QPushButton("Tardanzas")
        btn_ausencias = QPushButton("Ausencias")

        btn_entrada.clicked.connect(self.registrar_entrada)
        btn_salida.clicked.connect(self.registrar_salida)
        btn_reporte.clicked.connect(self.mostrar_reporte)
        btn_tardanzas.clicked.connect(self.mostrar_tardanzas)
        btn_ausencias.clicked.connect(self.mostrar_ausencias)

        layout.addWidget(btn_entrada)
        layout.addWidget(btn_salida)
        layout.addWidget(btn_reporte)
        layout.addWidget(btn_tardanzas)
        layout.addWidget(btn_ausencias)

        # ------- Tabla -------
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)

    # -----------------------------------------------------
    # ACCIONES
    # -----------------------------------------------------
    def registrar_entrada(self):
        empleado_id = 1
        msg = registrar_marcacion(empleado_id, "E")
        QMessageBox.information(self, "Entrada", msg)

    def registrar_salida(self):
        empleado_id = 1
        msg = registrar_marcacion(empleado_id, "S")
        QMessageBox.information(self, "Salida", msg)

    def mostrar_reporte(self):
        query = "SELECT * FROM vista_reporte_completo LIMIT 50;"
        self.cargar_tabla(query)

    def mostrar_tardanzas(self):
        query = "SELECT * FROM vista_tardanzas LIMIT 50;"
        self.cargar_tabla(query)

    def mostrar_ausencias(self):
        query = "SELECT * FROM vista_ausencias LIMIT 50;"
        self.cargar_tabla(query)

    # -----------------------------------------------------
    # Cargar tabla en la GUI
    # -----------------------------------------------------
    def cargar_tabla(self, query):
        rows = obtener_tabla(query)
        if not rows:
            QMessageBox.warning(self, "Aviso", "No hay datos para mostrar")
            return

        column_names = ["col" + str(i) for i in range(len(rows[0]))]

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(rows[0]))
        self.table.setHorizontalHeaderLabels(column_names)

        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(value)))


# ---------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# ---------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = BiometricSystem()
    ventana.show()
    sys.exit(app.exec())
