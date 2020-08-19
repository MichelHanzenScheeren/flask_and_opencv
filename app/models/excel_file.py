from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.chart import ScatterChart, Reference, Series
from io import BytesIO
import base64

class Excel_File():
    def __init__(self, title = ""):
        self.excel_file = Workbook()
        self.spreadsheet = self.excel_file.active
        self.spreadsheet.title = title
        self.to_merge_cells = []
    

    def build_file(self, general_info, differentiator_info, captures_info):
        row_count = self.generate_table(general_info, 1)
        row_count = self.generate_table(differentiator_info, row_count)
        row_count = self.generate_table(captures_info, row_count)
        self.configure_columns_width()
        self.merge_cells()
        self.generate_captures_graph(captures_info, row_count)
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
        for value in self.to_merge_cells:
            self.spreadsheet.merge_cells(start_row=value[0], start_column=1, end_row=value[0], end_column=value[1])
            self.spreadsheet.cell(row=value[0], column=1).fill = PatternFill(fgColor="D3D3D3", fill_type = "solid")


    def generate_captures_graph(self, captures_info, row_count):
        my_chart = ScatterChart()
        my_chart.title = "Gráfico dos Sinais"
        my_chart.style = 16
        my_chart.y_axis.title = 'Sinal'
        my_chart.x_axis.title = 'Tempo (segundos)'
        x_values = Reference(self.spreadsheet, min_col=1, min_row=row_count - len(captures_info), max_row=row_count - 3)
        y_values = Reference(self.spreadsheet, min_col=5, min_row=row_count - len(captures_info) - 1, max_row=row_count - 3)
        series = Series(y_values, x_values, title_from_data=True)
        my_chart.series.append(series)
        my_chart.width = 23
        my_chart.height = 10
        self.spreadsheet.add_chart(my_chart, f"A{row_count}")


    def encode_excel(self, excel_file):
        encoded = BytesIO()
        excel_file.save(encoded)
        encoded.seek(0)
        base_64 = base64.b64encode(encoded.read())
        return base_64
