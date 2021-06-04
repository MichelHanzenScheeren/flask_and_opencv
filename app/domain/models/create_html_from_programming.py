from app.domain.errors.app_error import AppError
from app.configuration import *


class CreateHtmlFromProgramming:
    def __init__(self, dictionary):
        self._dictionary = dictionary
        self._validate_dictionary()

    def _validate_dictionary(self):
        if type(self._dictionary) is not dict:
            message = 'Dados inváldos para criação do arquivo json'
            raise AppError('CreateHtmlFromJson.dictionary', message)

    def create(self):
        try:
            html = self._generate_triplicate_and_subtitle('', self._dictionary)
            html = self._generate_table(html, self._dictionary)
            return html
        except:
            message = 'O arquivo de programação não é válido!'
            raise AppError('CreateHtmlFromJson.dictionary', message)

    def _generate_triplicate_and_subtitle(self, html, dictionary):
        html += '<div id="programmingDataDiv"> <div class="row">  <div class="col"> '
        checked = 'checked' if dictionary[WORKING_IN_TRIPLICATE] else ''
        html += f'<input type="checkbox" id="triplicate_checkbox" style="height:14px;width:14px" {checked}>'
        html += '<label class="px-2" style="font-size:16px">CONSIDERAR CADA CICLO EM TRIPLICATA</label> '
        html += '</div> </div> <hr class="my-0 py-1"> '
        html += '<div class="table-responsive"> <table id="programmingTable" class="table table-bordered table-hover"> '
        html += '<thead class="table-dark" id="tableHead"> '
        html += '<tr align="center" class="titlesRow"> '
        html += '<th scope="col" class="align-middle" style="font-size:15px"> Novo ciclo</th> '
        html += '<th scope="col" class="align-middle" style="font-size:15px"> Tempo </th> '
        for i in range(1, dictionary[VALVES_QUANTITY] + 1):
            html += f'<th id="{i}" scope="col" style="font-size:17px">{i} <p onclick="ChangeToInput(this)" '
            name = f'Valv. {i}' if dictionary[SUBTITLE].get(
                f'Valv. {i}') == None else dictionary[SUBTITLE].get(f'Valv. {i}')
            html += f' style="font-size:12px;cursor:pointer;"class="m-0 valve_name">{name}</p></th> '
        html += '<th scope="col" class="align-middle">#</th> </tr> </thead> '
        return html

    def _generate_table(self, html, dictionary):
        html += '<tbody>'
        for i in range(0, len(dictionary[PROGRAMMING])):
            html += '' if i == 0 else self._generate_white_line(dictionary)
            grupo = dictionary[PROGRAMMING][f'{GROUP_NUMBER}{i}']
            for j in range(0, len(grupo)):
                linha = grupo[f'{LINE_NUMBER}{j}']
                html += '<tr align="center" class="valve_data"> '
                checked = 'checked' if linha[CYCLE_START] else ''
                html += f'<td class="align-middle"> <input type="checkbox" class="cycle_checkbox" {checked}> </td> '
                html += '<td class="align-middle"> '
                value = linha[SLEEP_TIME] or 0
                html += f'<input style="width:50px;font-size:14px;" min="1" type="number" value="{value}" required '
                html += 'class="form-control time_input p-1 m-0 title="Campo obrigatório" /> </td>'
                for k in range(0, dictionary[VALVES_QUANTITY]):
                    checked = ''
                    if (k + 1) in linha[OPEN_VALVES]:
                        checked = 'checked'
                    html += f'<td class="align-middle"> <input type="checkbox" class="valve_checkbox" {checked}></td>'
                html += '<td> <button class="btn btn-sml px-0 mx-0" onclick="RemoveTableRow(this)">'
                html += '<span class="fa fa-times"></span> </button> </td> </tr>'
        html += '</tbody> <tfoot> <tr align="center"> <td colspan="3">'
        html += '<button type="button" class="btn btn-sml btn-outline-primary" onclick="AddTableRow(this)">Adicionar linha</button>'
        html += ' </td> <td colspan="3">'
        html += '<button type="button" class="btn btn-sml btn-outline-primary" onclick="AddTableGroup(this)">Novo grupo</button>'
        html += '</td> </tr> </tfoot> </table> </div> </div>'
        return html

    def _generate_white_line(_, dictionary):
        linha_em_branco = '<tr align="center" class="to_remove valve_data white_line bg-secondary"> '
        for i in range(0, dictionary[VALVES_QUANTITY] + 3):
            linha_em_branco += '<td> </td> '
        linha_em_branco += '</tr>'
        return linha_em_branco
