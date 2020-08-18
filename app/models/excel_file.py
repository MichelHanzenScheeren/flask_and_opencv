from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from io import BytesIO
import base64

class Excel_File():
    def __init__(self, title = ""):
        self.excel_file = Workbook()
        self.spreadsheet = self.excel_file.active
        self.spreadsheet.title = title
        self.to_merge_cells = []
    

    def generate_spreadsheet(self, general_information, differentiator_information, captures_information):
        row_number = self.generate_table(general_information, 1)
        row_number = self.generate_table(differentiator_information, row_number)
        row_number = self.generate_table(captures_information, row_number)
        self.configure_columns_width()
        self.merge_cells()
        return self.encode_excel(self.excel_file)
    

    def generate_table(self, current_info, row_count):
        font1 = Font(name='Arial', size=14, bold=True, )
        font2 = Font(name='Arial', size=12)
        for i, row in enumerate(current_info):
            for j, column in enumerate(row):
                cell = self.spreadsheet.cell(row = row_count + i, column = j + 1)
                cell.font = font1 if i == 0 else font2
                cell.alignment = Alignment(horizontal="center") if i==0 or i == 1 else Alignment(horizontal='right')
                cell.value = column
                if i == 0:
                    self.to_merge_cells.append([row_count, len(current_info[0])])
        return row_count + len(current_info) + 2 #2 linhas em branco
    

    def configure_columns_width(self):
        for column in self.spreadsheet.columns:
            # length = max(len(str(cell.value)) for cell in column)
            self.spreadsheet.column_dimensions[column[0].column_letter].width = 25.0 #length * 1.2
    

    def merge_cells(self):
        for _,value in enumerate(self.to_merge_cells):
            self.spreadsheet.merge_cells(start_row=value[0], start_column=1, end_row=value[0], end_column=value[1])


    def encode_excel(self, excel_file):
        encoded = BytesIO()
        excel_file.save(encoded)
        encoded.seek(0)
        base_64 = base64.b64encode(encoded.read())
        return base_64
