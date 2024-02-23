# Gui_Manager.py
from PyQt5.QtWidgets import QTableWidgetItem
from . import Constants
import logging

class GuiManager:
    '''Manages the GUI components and interactions for the network scanner application.'''

    def __init__(self, init_gui):
        '''Initializes the GUI manager with a reference to the main GUI class.'''
        self.init_gui = init_gui

    def UpdateUI(self):
        '''Updates the UI elements based on the selected scan type.'''
        self.init_gui.hide_all_optinoal_inputs()
        if self.init_gui.scan_type_combo.currentText() == Constants.SCAN_TYPE_PING:
            self.show_PINGsweep_inputs()
        elif self.init_gui.scan_type_combo.currentText() == Constants.SCAN_TYPE_PORT:
            self.show_PORTscan_inputs()

    def show_PINGsweep_inputs(self):
        '''Displays input fields relevant to ping sweep scans.'''
        self.init_gui.timeout_label.show()
        self.init_gui.timeout_input.show()
        self.init_gui.ttl_label.show()
        self.init_gui.ttl_input.show()
        self.init_gui.interval_label.show()
        self.init_gui.interval_input.show()
        self.init_gui.packet_size_label.show()
        self.init_gui.packet_size_input.show()

    def show_PORTscan_inputs(self):
        '''Displays input fields relevant to port scans.'''
        self.init_gui.start_port_label.show()
        self.init_gui.start_port_input.show()
        self.init_gui.end_port_label.show()
        self.init_gui.end_port_input.show()

    def collect_inputs(self):
        '''Collects and returns inputs from the GUI.'''
        inputs = {
            Constants.KEY_CURRENT_SCAN_TYPE: self.init_gui.scan_type_combo.currentText(),
            Constants.KEY_START_IP: self.init_gui.start_ip_input.text(),
            Constants.KEY_END_IP: self.init_gui.end_ip_input.text(),
            Constants.KEY_PREFIX: self.init_gui.prefix_input.text(),
            Constants.KEY_TIMEOUT: self.init_gui.timeout_input.text(),
            Constants.KEY_TTL: self.init_gui.ttl_input.text(),
            Constants.KEY_INTERVAL: self.init_gui.interval_input.text(),
            Constants.KEY_PACKET_SIZE: self.init_gui.packet_size_input.text(),
            Constants.KEY_START_PORT: self.init_gui.start_port_input.text(),
            Constants.KEY_END_PORT: self.init_gui.end_port_input.text(),
        }
        return inputs

    def update_status_label(self, message):
        '''Updates the status label with a message.'''
        self.init_gui.status_label.setText(message)

    def on_scan_started(self):
        '''Handles actions when a scan starts.'''
        self.reset_scan_result()
        self.init_gui.status_label.setStyleSheet('QLabel { color : black; }')
        self.update_status_label(Constants.SCAN_IN_PROGRESS)
        self.init_gui.scan_button.setEnabled(False)
        self.init_gui.abort_button.setEnabled(True)

    def update_result_table(self, scan_results):
        '''Updates the result table with scan results.'''
        for device_info in scan_results:
            row_position = self.init_gui.result_table.rowCount()
            self.init_gui.result_table.insertRow(row_position)
            self.init_gui.result_table.setItem(row_position, 0, QTableWidgetItem(device_info.get(Constants.TABLE_COLOUM_IP)))
            self.init_gui.result_table.setItem(row_position, 1, QTableWidgetItem(device_info.get(Constants.TABLE_COLOUM_MAC)))
            self.init_gui.result_table.setItem(row_position, 2, QTableWidgetItem(device_info.get(Constants.TABLE_COLOUM_HOST)))
            open_ports = ', '.join(map(str, device_info.get(Constants.TABLE_COLOUM_PORT, [])))
            self.init_gui.result_table.setItem(row_position, 3, QTableWidgetItem(open_ports))

    def on_scan_aborted(self):
        '''Handles actions when a scan is aborted.'''
        self.init_gui.status_label.setStyleSheet('QLabel { color : red; }')
        self.update_status_label(Constants.SCAN_ABORTED)
        self.init_gui.scan_button.setEnabled(True)
        self.init_gui.abort_button.setEnabled(False)

    def on_scan_completed(self):
        '''Handles actions when a scan is completed.'''
        self.init_gui.status_label.setStyleSheet('QLabel { color : green; }')
        self.update_status_label(Constants.SCAN_COMPLETED)
        self.init_gui.scan_button.setEnabled(True)
        self.init_gui.abort_button.setEnabled(False)
        logging.info('Scan completed successfully.')

    def handle_error(self, error_message):
        '''Displays an error message in the status label.'''
        self.init_gui.status_label.setStyleSheet('QLabel { color : red; }')
        self.update_status_label(error_message)
        self.init_gui.scan_button.setEnabled(True)
        self.init_gui.abort_button.setEnabled(False)
    
    def reset_scan_result(self):
        '''Resets the scan result table and clears the status label.'''
        self.init_gui.result_table.setRowCount(0)
        self.init_gui.status_label.clear()