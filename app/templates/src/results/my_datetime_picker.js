function registerDatetimePicker(format) {
  $('#myDatetimePicker')
    .datetimepicker({ format: format, ignoreReadonly: true })
    .on("dp.hide", () => saveNewAnalyzeDate());
}

function saveNewAnalyzeDate() {
  axios.post(`{{url_for("save_new_analyze_date")}}/${document.getElementById("myDatetimePicker").value}`)
    .catch(showErrorMessage);
}
