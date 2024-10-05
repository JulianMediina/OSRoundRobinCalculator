import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHBoxLayout, QMessageBox
)

# Función para calcular el tiempo de espera de los procesos usando Round Robin
def find_waiting_time(processes, n, burst_time, arrival_time, quantum):
    rem_bt = burst_time.copy()  # Copia de los tiempos de ejecución
    waiting_time = [0] * n
    completion_time = [0] * n  # Almacenará el tiempo de finalización
    t = 0  # Tiempo actual
    completed = 0  # Contador de procesos completados

    while completed < n:
        done = True
        for i in range(n):
            if rem_bt[i] > 0 and arrival_time[i] <= t:  # El proceso se ejecuta si ha llegado
                done = False  # Hay un proceso pendiente
                if rem_bt[i] > quantum:
                    t += quantum
                    rem_bt[i] -= quantum
                else:
                    t += rem_bt[i]
                    waiting_time[i] = t - burst_time[i] - arrival_time[i]  # Calcula el tiempo de espera
                    completion_time[i] = t  # Guarda el tiempo de finalización
                    rem_bt[i] = 0
                    completed += 1
        
        if done:
            next_arrival = min([arrival_time[j] for j in range(n) if rem_bt[j] > 0], default=t)
            t = max(t, next_arrival)
            
    return waiting_time, completion_time

# Función para calcular el tiempo de retorno (TAT)
def find_turn_around_time(processes, n, burst_time, waiting_time):
    turn_around_time = [0] * n
    for i in range(n):
        turn_around_time[i] = burst_time[i] + waiting_time[i]  # TAT = BT + WT
    return turn_around_time

# Función para calcular el tiempo promedio de espera y TAT
def find_avg_time(processes, n, burst_time, arrival_time, quantum):
    waiting_time, completion_time = find_waiting_time(processes, n, burst_time, arrival_time, quantum)
    turn_around_time = find_turn_around_time(processes, n, burst_time, waiting_time)
    return waiting_time, completion_time, turn_around_time

# Clase que implementa la interfaz gráfica usando PyQt5
class RoundRobinApp(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle('Simulador de Round Robin')
        self.setGeometry(100, 100, 900, 900)

        # Diseño de la interfaz
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Campos de entrada
        self.quantum_input = QLineEdit()
        self.processes_input = QLineEdit()
        self.burst_input = QLineEdit()
        self.arrival_input = QLineEdit()

        # Añadir etiquetas y campos de entrada al formulario
        form_layout.addRow(QLabel('Tiempo Quantum:'), self.quantum_input)
        form_layout.addRow(QLabel('Número de Procesos (ej: 3):'), self.processes_input)
        form_layout.addRow(QLabel('Duración de Procesos (ej: 10,5,8):'), self.burst_input)
        form_layout.addRow(QLabel('Tiempos de Llegada (ej: 0,1,2):'), self.arrival_input)

        # Botón para ejecutar la simulación
        self.run_button = QPushButton('Ejecutar')
        self.run_button.clicked.connect(self.run_simulation)

        # Tabla para mostrar los resultados
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(7)
        self.result_table.setHorizontalHeaderLabels(["Proceso", "AT", "BT", "CT", "TAT", "NTAT", "WT"])

        # Etiquetas para mostrar los promedios
        self.avg_wt_label = QLabel('Promedio de tiempo de espera: ')
        self.avg_tat_label = QLabel('Promedio de TAT: ')

        layout.addLayout(form_layout)
        layout.addWidget(self.run_button)
        layout.addWidget(self.result_table)
        layout.addWidget(self.avg_wt_label)
        layout.addWidget(self.avg_tat_label)

        self.setLayout(layout)

    # Función que muestra un mensaje de error en pantalla
    def show_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

    # Función que ejecuta la simulación
    def run_simulation(self):
        try:
            # Validación y obtención de valores ingresados por el usuario
            quantum = int(self.quantum_input.text())
            num_processes = int(self.processes_input.text())
            burst_time = list(map(int, self.burst_input.text().split(',')))
            arrival_time = list(map(int, self.arrival_input.text().split(',')))

            # Validar si los valores de tiempos coinciden con el número de procesos
            if len(burst_time) != num_processes or len(arrival_time) != num_processes:
                raise ValueError("El número de procesos no coincide con los valores ingresados.")

            # Calcular tiempos de espera, finalización y TAT
            waiting_time, completion_time, turn_around_time = find_avg_time(
                range(num_processes), num_processes, burst_time, arrival_time, quantum
            )

            # Mostrar los resultados en la tabla
            self.result_table.setRowCount(num_processes)
            for i in range(num_processes):
                self.result_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))  # Proceso
                self.result_table.setItem(i, 1, QTableWidgetItem(str(arrival_time[i])))  # AT
                self.result_table.setItem(i, 2, QTableWidgetItem(str(burst_time[i])))  # BT
                self.result_table.setItem(i, 3, QTableWidgetItem(str(completion_time[i])))  # CT
                self.result_table.setItem(i, 4, QTableWidgetItem(str(turn_around_time[i])))  # TAT
                ntat = turn_around_time[i] / burst_time[i]  # Calculo del TAT normalizado
                self.result_table.setItem(i, 5, QTableWidgetItem(f"{ntat:.2f}"))  # NTAT
                self.result_table.setItem(i, 6, QTableWidgetItem(str(waiting_time[i])))  # WT

            # Calcular y mostrar los promedios
            avg_wt = sum(waiting_time) / num_processes
            avg_tat = sum(turn_around_time) / num_processes

            self.avg_wt_label.setText(f'Promedio de tiempo de espera: {avg_wt:.2f}')
            self.avg_tat_label.setText(f'Promedio de TAT: {avg_tat:.2f}')

        except ValueError as e:
            # Mostrar mensaje de error si ocurre un problema de validación
            self.show_error(str(e))

        except Exception as e:
            # Mostrar cualquier otro error inesperado
            self.show_error(f"Ha ocurrido un error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoundRobinApp()
    window.show()
    sys.exit(app.exec_())
