function config_analyze(){
  document.getElementById("div1").style.display = "none";
  document.getElementById("div2").style.display = "block";
}

async function get_differentiator(){
  let response = await axios.post("{{ url_for('get_differentiator') }}");
  document.getElementById("red").innerHTML = "Red: " + response.data[0];
  document.getElementById("green").innerHTML = "Green: " + response.data[1];
  document.getElementById("blue").innerHTML = "Blue: " + response.data[2];
  document.getElementById("start").disabled = false;
}
