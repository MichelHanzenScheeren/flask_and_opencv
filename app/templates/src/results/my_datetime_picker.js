function registerDatetimePicker(format) {
  $('#myDatetimePicker')
  .datetimepicker({format: format, ignoreReadonly:true})
  .on( "dp.hide", () => saveNewAnalyzeDate());

}

async function saveNewAnalyzeDate() {
  try {
    let result = await axios.post(`{{url_for("saveNewAnalyzeDate")}}/${document.getElementById("myDatetimePicker").value}`);
    if(result.data.length != 0) showErrorMessage(result);
  } catch(error) {
    showErrorMessage(error);
  }
}
