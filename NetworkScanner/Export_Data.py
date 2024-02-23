#select_format.py
from PyQt5.QtWidgets import QFileDialog
import csv
import json

class ExportData:
    '''Handles data export functionality for the application.'''

    def __init__(self):
        '''Initializes the ExportData class.'''
        pass   # No initialization needed for now

    def trigger_export(self, table_widget):
        '''Initiates the export process by asking the user to select a file format.'''
        self.select_format(table_widget)

    def select_format(self, table_widget):
        '''Displays a dialog for the user to select the export file format and filename.'''
        # Opens a file dialog to choose the format and filename for the export
        filename, filetype = QFileDialog.getSaveFileName(None, 'Export Data', '', 'CSV Files (*.csv);;JSON Files (*.json)')
        
        if filename:    # If a filename was selected
            if filetype == 'CSV Files (*.csv)':
                self.export_to_csv(table_widget, filename)    # Export to CSV
                
            elif filetype == 'JSON Files (*.json)':
                self.export_to_json(table_widget, filename)    # Export to JSON

    def export_to_csv(self, table_widget, filename):
        '''Exports the data in the table widget to a CSV file.'''
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the headers
            headers = [table_widget.horizontalHeaderItem(i).text() for i in range(table_widget.columnCount())]
            writer.writerow(headers)

            # Write the row data
            for row in range(table_widget.rowCount()):
                row_data = [table_widget.item(row, col).text() if table_widget.item(row, col) else '' for col in range(table_widget.columnCount())]
                writer.writerow(row_data)

    def export_to_json(self, table_widget, filename):
        '''Exports the data in the table widget to a JSON file.'''
        data = []    # List to hold all rows' data
        headers = [table_widget.horizontalHeaderItem(i).text() for i in range(table_widget.columnCount())]

        # Iterate over each row to construct a dict of cell data
        for row in range(table_widget.rowCount()):
            row_data = {}
            for col in range(table_widget.columnCount()):
                item = table_widget.item(row, col)
                row_data[headers[col]] = item.text() if item else ''
            data.append(row_data)
        
        # Write the JSON data to file
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
