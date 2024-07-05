import os
import sys
import threading

from PyQt6 import QtWidgets

from ast_monitor.simulation import Simulation

try:
    from ast_monitor.model import AST
except ModuleNotFoundError:
    sys.path.append('../')
    from ast_monitor.model import AST

hr_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.', 'sensor_data', 'hr.txt')
gps_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.', 'sensor_data', 'gps.txt')
route_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.', 'development', 'routes', 'route.json')

def start_simulation():
    sim = Simulation()
    threading.Thread(target=sim.simulate_gps, daemon=True).start()
    threading.Thread(target=sim.simulate_hr, daemon=True).start()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AST(hr_data, gps_data, route_data)
    window.show()

    start_simulation()

    sys.exit(app.exec())
