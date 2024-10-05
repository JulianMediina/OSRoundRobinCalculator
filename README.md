# Round Robin CPU Scheduler Simulator with PyQt5 Interface

## Overview

Author Brayan Julián Barrantes Medina.

This is a visual simulator of the **Round Robin** scheduling algorithm used in operating systems to manage processes. Developed in **Python** using the **PyQt5** library, this program provides an easy-to-use graphical interface where users can input process information such as **Arrival Time (AT)**, **Burst Time (BT)**, and the system's **Quantum**.. 

The simulator processes these inputs and displays the results in a table format, detailing each process's **Completion Time (CT)**, **Turnaround Time (TAT)**, **Waiting Time (WT)**, and **Normalized Turnaround Time (NTAT)**. Additionally, the program calculates and shows the **average waiting time** and **average TAT**.

### Key Features

- **Graphical Interface:** Built using **PyQt5**, offering a simple and interactive user experience.
- **Support for multiple processes:** You can input different arrival and burst times for several processes.
- **Dynamic simulation:** The algorithm simulates how processes are managed using the Round Robin scheduling technique, adjusting based on their arrival and burst times.
- **Clear result visualization:** The results are displayed in a table with the following columns:
  - **Process**
  - **AT (Arrival Time)**
  - **BT (Burst Time)**
  - **CT (Completion Time)**
  - **TAT (Turnaround Time)**
  - **NTAT (Normalized TAT)**
  - **WT (Waiting Time)**
- **Average Calculations:** Displays average **waiting time** and average **TAT** in the application window.

## How to Use

1. **Installation:**

   Clone this repository and ensure you have **Python 3** installed. You will also need to install **PyQt5** if it's not already installed.

   ```bash
   git clone https://github.com/JulianMediina/OSRoundRobinCalculator.git
   pip install PyQt5
