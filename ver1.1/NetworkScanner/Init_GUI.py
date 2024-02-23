#Init_GUI.py
# Import PyQt5 modules for building the application's GUI
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from .Process_Manager import ProcessManager
from .Gui_Manager import GuiManager
from .Export_Data import ExportData
from . import Constants
import logging

class InitGUI(QMainWindow):
    '''
    This class initializes the main GUI window of the application,
    sets up the layout, and configures the widgets.
    '''
    def __init__(self):
        super().__init__()
        logging.info('Application initialization started.')
        # Initialize components responsible for managing GUI, processes, and data export
        self.gui_manager = GuiManager(self)
        self.process_manager = ProcessManager(self, self.gui_manager)
        self.export_data = ExportData()
        self.InitUI()

    def InitUI(self):
        '''
        Setup the UI components, including labels, input fields, buttons, and layouts.
        Each part of the GUI is initialized here and configured to interact with the system.
        '''
        #Window setup
        self.setWindowTitle(Constants.WINDOW_TITLE)
        self.resize(600, 400)

        #Labels, input fields, buttton setup
        Vlayout1 = QVBoxLayout()
        Hlayout1 = QHBoxLayout()
        Hlayout2 = QHBoxLayout()

        self.scan_type_label = QLabel(Constants.SCAN_TYPE_ARP)
        self.scan_type_combo = QComboBox()
        self.scan_type_combo.setFixedWidth(150)
        self.scan_type_combo.addItems([Constants.SCAN_TYPE_ARP, Constants.SCAN_TYPE_PING, Constants.SCAN_TYPE_PORT])
        self.scan_type_combo.currentIndexChanged.connect(self.gui_manager.UpdateUI)
        Vlayout1.addWidget(self.scan_type_label)
        Vlayout1.addWidget(self.scan_type_combo)

        self.start_ip_label = QLabel(Constants.START_IP)
        self.start_ip_input = QLineEdit()
        self.start_ip_input.setMaxLength(15)
        self.start_ip_input.setFixedWidth(150)
        Vlayout1.addWidget(self.start_ip_label)
        Vlayout1.addWidget(self.start_ip_input)

        self.end_ip_label = QLabel(Constants.END_IP)
        self.end_ip_input = QLineEdit()
        self.end_ip_input.setMaxLength(15)
        self.end_ip_input.setFixedWidth(150)
        Vlayout1.addWidget(self.end_ip_label)
        Vlayout1.addWidget(self.end_ip_input)

        self.prefix_label = QLabel(Constants.PREFIX)
        self.prefix_input = QLineEdit()
        self.prefix_input.setMaxLength(2)
        self.prefix_input.setFixedWidth(150)
        Vlayout1.addWidget(self.prefix_label)
        Vlayout1.addWidget(self.prefix_input)

        ## Ping sweep variables
        self.timeout_label = QLabel(Constants.TIMEOUT)
        self.timeout_input = QLineEdit()
        default_timeout = Constants.DEFAULT_TIMEOUT
        self.timeout_input.setText(default_timeout)
        self.timeout_input.setMaxLength(3)
        self.timeout_input.setFixedWidth(150)
        Vlayout1.addWidget(self.timeout_label)
        Vlayout1.addWidget(self.timeout_input)

        self.ttl_label = QLabel(Constants.TTL)
        self.ttl_input = QLineEdit()
        default_ttl = Constants.DEFAULT_TTL
        self.ttl_input.setText(default_ttl)
        self.ttl_input.setMaxLength(3)
        self.ttl_input.setFixedWidth(150)
        Vlayout1.addWidget(self.ttl_label)
        Vlayout1.addWidget(self.ttl_input)

        self.interval_label = QLabel(Constants.INTERVAL)
        self.interval_input = QLineEdit()
        default_interval = Constants.DEFAULT_INTERVAL
        self.interval_input.setText(default_interval)
        self.interval_input.setMaxLength(2)
        self.interval_input.setFixedWidth(150)
        Vlayout1.addWidget(self.interval_label)
        Vlayout1.addWidget(self.interval_input)

        self.packet_size_label = QLabel(Constants.PACKET_SIZE)
        self.packet_size_input = QLineEdit()
        default_packet_size = Constants.DEFAULT_PACKET_SIZE
        self.packet_size_input.setText(default_packet_size)
        self.packet_size_input.setMaxLength(5)
        self.packet_size_input.setFixedWidth(150)
        Vlayout1.addWidget(self.packet_size_label)
        Vlayout1.addWidget(self.packet_size_input)

        self.start_port_label = QLabel(Constants.START_PORT)
        self.start_port_input = QLineEdit()
        self.start_port_input.setMaxLength(5)
        self.start_port_input.setFixedWidth(150)
        Vlayout1.addWidget(self.start_port_label)
        Vlayout1.addWidget(self.start_port_input)

        self.end_port_label = QLabel(Constants.END_PORT)
        self.end_port_input = QLineEdit()
        self.end_port_input.setMaxLength(5)
        self.end_port_input.setFixedWidth(150)
        Vlayout1.addWidget(self.end_port_label)
        Vlayout1.addWidget(self.end_port_input)

        ##Start scan/Abort scan button
        ###Start scan button
        self.scan_button = QPushButton(Constants.START_SCAN_BUTTON)
        self.scan_button.setFixedWidth(100)
        self.scan_button.clicked.connect(self.process_manager.start_scan)
        Hlayout1.addWidget(self.scan_button)
        Vlayout1.addLayout(Hlayout1)

        ###Abort scan button
        self.abort_button = QPushButton(Constants.ABORT_SCAN_BUTTON)
        self.abort_button.setFixedWidth(100)
        self.abort_button.clicked.connect(self.process_manager.abort_scan)
        Hlayout1.addWidget(self.abort_button)
        Hlayout1.addStretch()

        ##status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignLeft)
        self.status_label.setWordWrap(True)
        Vlayout1.addWidget(self.status_label)

        ###status label font
        font = QFont()
        font.setPointSize(14)
        self.status_label.setFont(font)

        ##result table
        container_widget = QWidget()
        container_widget.setLayout(Vlayout1)
        self.setCentralWidget(container_widget)
        self.setFixedWidth(570)

        self.result_table = QTableWidget()
        Vlayout1.addWidget(self.result_table)
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels([Constants.TABLE_COLOUM_IP , Constants.TABLE_COLOUM_MAC, Constants.TABLE_COLOUM_HOST, Constants.TABLE_COLOUM_PORT])
        self.result_table.setColumnWidth(0, 100)
        self.result_table.setColumnWidth(1, 100)
        self.result_table.setColumnWidth(2, 150)
        self.result_table.setColumnWidth(3, 200)
        self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)

        ##export button
        self.export_button = QPushButton(Constants.EXPORT_DATA_BUTTON, self)
        self.export_button.setFixedWidth(120)
        self.export_button.clicked.connect(lambda: self.export_data.trigger_export(self.result_table))
        Hlayout2.addStretch(1)
        Hlayout2.addWidget(self.export_button)
        Vlayout1.addLayout(Hlayout2)

        #Hide all the optional inputs
        self.hide_all_optinoal_inputs()

    def hide_all_optinoal_inputs(self):
        '''
        Hides optional input fields initially. They are shown based on the selected scan type.
        This method is called during initialization to simplify the UI for the user.
        '''
        self.timeout_label.hide()
        self.timeout_input.hide()
        self.ttl_label.hide()
        self.ttl_input.hide()
        self.interval_label.hide()
        self.interval_input.hide()
        self.packet_size_label.hide()
        self.packet_size_input.hide()
        self.start_port_label.hide()
        self.start_port_input.hide()
        self.end_port_label.hide()
        self.end_port_input.hide()