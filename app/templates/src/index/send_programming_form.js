function saveProgramming() {
  let map = {};
  saveConfiguration(map);
  submitProgramation(map);
  saveState();
  return false;
}

function saveConfiguration(map) {
  let findeds = $('tr').filter('.valve_data');
  let programacao = {};
  let grupoAtual = 0, linhaAtual = 0;
  programacao[`grupo_${grupoAtual}`] = {};
  for (let index = 0; index < findeds.length; index++) {
    if (findeds[index].className.includes('white_line')) {
      grupoAtual += 1;
      linhaAtual = 0;
      programacao[`grupo_${grupoAtual}`] = {};
    } else {
      programacao[`grupo_${grupoAtual}`][`linha_${linhaAtual}`] = saveCurrentGroupData(findeds[index]);
      linhaAtual += 1;
    }
  };
  map["programacao"] = programacao;
  map['qtd_valvulas'] = parseInt('{{ parameters["valves_number"] }}');
  map["triplicata"] = document.getElementById("triplicate_checkbox").checked;
  map["legenda"] = {}
  let ps = $('p').filter('.valve_name');
  for (let j = 0; j < ps.length; j++) {
    if (ps[j].textContent.trim() != `Valv${j + 1}`) {
      map["legenda"][`Valv${j + 1}`] = ps[j].textContent.trim();
    }
  }
}

function saveCurrentGroupData(finded) {
  let valves = [];
  let checkboxs = finded.getElementsByClassName('valve_checkbox');
  for (let j = 0; j < checkboxs.length; j++) {
    if (checkboxs[j].checked)
      valves.push(j + 1);
  }
  let configuracao = {}
  configuracao["valvulas_abertas"] = valves;
  configuracao["tempo_espera"] = parseFloat(finded.getElementsByClassName('time_input')[0].value);
  configuracao["inicio_ciclo"] = finded.getElementsByClassName('cycle_checkbox')[0].checked;
  return configuracao;
}

function submitProgramation(map) {
  axios.post('{{url_for("submit_programming")}}', map).catch(showErrorMessage)
}

function saveState() {
  savedProgramming = true;
  changeOptionOfSelectAnalyzeMethodToComlete();
  checkIfNeedToChangeAnalyzeButtonOptions();
  $('#openProgrammingModal').html('Editar programação');
  $('#programmingModal').modal('hide');
}
