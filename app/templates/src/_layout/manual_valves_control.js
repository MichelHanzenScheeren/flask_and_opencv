function uncheckAll() {
  $("[name='valveToggle']").bootstrapToggle("off");
}
function checkAll() {
  $("[name='valveToggle']").bootstrapToggle("on");
}

window.onload = function () {
  $("[name='valveToggle']").change(function () {
    $("#unsavedDiv").css("display", "block");
    $("#savedDiv").css("display", "none");
  });
}

async function submitValvesConfig() {
  let valves = [];
  let toggles = document.getElementsByName('valveToggle');
  for (let i = 0; i < toggles.length; i++) {
    if (toggles[i].checked)
      valves.push(i + 1);
  }
  let response = await axios.post('{{url_for("submit_valves_config")}}', { 'valves': valves });
  if (response.data['success'] == true) {
    $("#unsavedDiv").css("display", "none");
    $("#savedDiv").css("display", "block");
  } else {
    let title = 'Problemas para completar a solicitação &#128533;';
    showMessage(title, response.data['message'], undefined, true);
  }
}
