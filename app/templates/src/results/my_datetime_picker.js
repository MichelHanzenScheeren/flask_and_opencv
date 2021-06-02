function registerDatetimePicker(format) {
  $('#myDatetimePicker')
    .datetimepicker({ format: format, ignoreReadonly: true })
    .on("dp.hide", () => saveNewAnalyzeDate());
}

function saveNewAnalyzeDate() {
  axios.post(`{{url_for("saveNewAnalyzeDate")}}/${document.getElementById("myDatetimePicker").value}`)
    .catch(showErrorMessage);
}
