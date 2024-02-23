# Process_Manager.py
from .Scan_Thread import ScanThread
from .UserInput_Handler import UserInputHandler
import logging

class ProcessManager:
    '''
    Manages the scanning process, including starting, aborting, and handling the completion
    of scans. It interacts with GUI elements to reflect the state of scanning processes.
    '''
    def __init__(self, init_gui, gui_manager):
        self.init_gui = init_gui
        self.gui_manager = gui_manager
        self.scan_abort_flag = False
        self.scan_thread = None

    def start_scan(self):
        '''
        Initiates a scan based on user inputs collected from the GUI.
        Validates inputs and configures the scan thread for execution.
        '''
        logging.info('Starting scan.')
        user_inputs = self.gui_manager.collect_inputs()

        try:
            Current_ScanType = self.init_gui.scan_type_combo.currentText()
            self.UserInputHandler_instance = UserInputHandler(**user_inputs)
            validated_inputs = self.UserInputHandler_instance.validate_all()
            self.scan_thread = ScanThread(Current_ScanType=Current_ScanType,**validated_inputs)
            self.setup_scan_thread()

        except ValueError as e:
            logging.warning(f'Validation error during scan setup: {e}')
            self.gui_manager.handle_error(str(e))

        except Exception as e:
            self.gui_manager.handle_error('An unexpected error occurred. Please try again.')
            return

    def setup_scan_thread(self):
        if self.scan_thread is not None:
            self.scan_thread.started.connect(self.gui_manager.on_scan_started)
            self.scan_thread.error_signal.connect(self.gui_manager.handle_error)
            self.scan_thread.result_signal.connect(self.gui_manager.update_result_table)
            self.scan_thread.finished.connect(self.end_scan)
            
            self.scan_thread.start()

    def abort_scan(self):
        '''
        Aborts the currently running scan if possible.
        Sets a flag to signal the scan thread to stop execution.
        '''
        logging.info('Scan aborted by user.')
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_abort_flag = True
            self.scan_thread.stop()
            self.scan_thread.wait()

    def end_scan(self):
        '''
        Handles the cleanup and UI updates upon scan completion or abortion.
        Resets flags and updates the GUI to reflect the end of scanning.
        '''
        if self.scan_thread.error:
            pass
        elif self.scan_abort_flag:
            self.gui_manager.on_scan_aborted()
        else:
            self.gui_manager.on_scan_completed()
        
        self.scan_abort_flag = False
