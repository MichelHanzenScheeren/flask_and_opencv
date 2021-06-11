$('#programmingModal').on('shown.bs.modal', function () {
  $('#programmingTable').stickyTableHeaders(); // Habilita header da tabela que acompanha o scroll
});

// Se necessário, limpa as legendas e inputs preenchidos
$('#programmingModal').on('hidden.bs.modal', function () {
  $('programmingTable').stickyTableHeaders('destroy'); // Desabilita header da tabela que acompanha o scroll
  if (!savedProgramming) {
    $(this).find('form').trigger('reset');
    $(".to_remove").remove();
    var p = $('p').filter('.valve_name');
    for (let index = 0; index < p.length; index++)
      p[index].textContent = `Valv${index + 1}`;
  }
});

// Chama a função que movimenta o header com o scroll
document.getElementById('programmingModal').addEventListener('scroll', function (_) {
  $(window).trigger('resize.stickyTableHeaders');
});

function createTableRow() {
  let tableRow = '<tr align="center" class="to_remove valve_data">';
  tableRow += '<td class="align-middle"> <input type="checkbox" class="cycle_checkbox"> </td>';
  tableRow += ' <td class="align-middle"> <input style="width:50px;font-size:14px;" class="form-control';
  tableRow += ' time_input p-1 m-0" type="number" value="0" min="1" required title="Campo obrigatório" /> </td>';
  for (let i = 0; i < valves_number; i++)
    tableRow += ' <td class="align-middle"> <input type="checkbox" class="valve_checkbox"> </td>'
  tableRow += ' <td> <button class="btn btn-sml px-0 mx-0" onclick="RemoveTableRow(this)">';
  tableRow += ' <span class="fa fa-times"></span> </button></td>';
  tableRow += ' </tr>';
  return tableRow;
}

function RemoveTableRow(item) {
  if ($('tr').filter('.valve_data').length > 1) {
    $(item).closest('tr').remove();
    removeWhiteLineIfNecessary();
  }
}

function removeWhiteLineIfNecessary() {
  let trs = $('tr');
  if (trs[trs.length - 2].className.includes('white_line'))
    trs[trs.length - 2].remove();
}

function AddRow(item) {
  $(item).closest('table').append(createTableRow());
}

function AddGroup(item) {
  let linhaEmBranco = '<tr align="center" class="to_remove valve_data white_line bg-secondary">';
  for (let i = 0; i < valves_number + 3; i++)
    linhaEmBranco += ' <td> </td>'
  linhaEmBranco += '</tr>';
  let table = $(item).closest('table');
  table.append(linhaEmBranco);
  table.append(createTableRow());
}

function ChangeToInput(item) {
  let parent_id = "#" + $(item).parent()[0].id;
  let inputConfig = { type: 'text', style: 'width:50px;font-size:12px;', class: 'm-0 p-1', onblur: 'ChangeToLabel(this)' };
  let newInput = $("<input />", inputConfig);
  $(parent_id).append(newInput);
  $(newInput).focus();
  $(newInput).val(item.textContent.trim());
  item.remove();
}

function ChangeToLabel(item) {
  let valvId = $(item).parent()[0].id;
  let parent_id = "#" + valvId;
  let pConfig = { onclick: "ChangeToInput(this)", style: "font-size:12px;cursor:pointer;", class: "m-0 valve_name" };
  let newLabel = $("<p>", pConfig);
  newLabel.html(item.value != "" ? item.value : `Valv${valvId}`);
  $(parent_id).append(newLabel);
  item.remove();
}
