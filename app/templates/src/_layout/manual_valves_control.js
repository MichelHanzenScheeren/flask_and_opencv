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

function submitValvesConfig() {
  let valves = [];
  let toggles = document.getElementsByName('valveToggle');
  for (let i = 0; i < toggles.length; i++) {
    if (toggles[i].checked) valves.push(i + 1);
  }
  axios.post('{{url_for("submit_valves_config")}}', { 'valves': valves })
    .then(_successSubmitValvesConfig)
    .catch(showErrorMessage);
}

function _successSubmitValvesConfig(_) {
  $("#unsavedDiv").css("display", "none");
  $("#savedDiv").css("display", "block");
}
