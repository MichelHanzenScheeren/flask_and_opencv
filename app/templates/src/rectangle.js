const htmlXY = {
	x1: document.getElementById("x1"),
    y1: document.getElementById("y1"),
    x2: document.getElementById("x2"),
    y2: document.getElementById("y2"),
}
const rect = {};
let drag = false;

(function initRectangle() {
	var desenho = document.getElementById('desenho');
	desenho.addEventListener('mousedown', mouseDown, false);
	desenho.addEventListener('mouseup', mouseUp, false);
	desenho.addEventListener('mousemove', mouseMove, false);
	document.getElementById("refresh_button").setAttribute("onclick", "refresh_rectangle()");
	document.getElementById("clear_button").setAttribute("onclick", "clear_rectangle()");
}) ();

function mouseDown(e) {
	rect.startX = e.pageX - this.offsetLeft;
	rect.startY = e.pageY - this.offsetTop;
	drag = true;
	htmlXY.x1.value = rect.startX;
	htmlXY.y1.value = rect.startY;
}

function mouseUp() {
	drag = false;
	draw();
}

function mouseMove(e) {
	if (drag) {
		rect.w = (e.pageX - this.offsetLeft) - rect.startX;
		rect.h = (e.pageY - this.offsetTop) - rect.startY;
		htmlXY.x2.value = rect.startX + rect.w;
		htmlXY.y2.value = rect.startY + rect.h;
	}
}

function draw() {
	axios.post(`{{url_for("get_measures")}}/${rect.startX}/${rect.startY}/
	${(rect.startX + rect.w)}/${(rect.startY + rect.h)}`);
}

function clear_rectangle(){
    axios.post("{{ url_for('clear_rectangle') }}");
    htmlXY.x1.value = 0;
	htmlXY.x2.value = 0;
	htmlXY.y1.value = 0;
	htmlXY.y2.value = 0;
}

function refresh_rectangle(){
	let x1 = htmlXY.x1.value;
	let y1 = htmlXY.y1.value;
	let x2 = htmlXY.x2.value;
	let y2 = htmlXY.y2.value;
	if(x1.length>=1 && y1.length>=1 && x2.length>=1 && y1.length>=1){
		if(parseInt(x1)>=0 && parseInt(y1)>=0 && parseInt(x2)>=0 && parseInt(y2)>=0){
			axios.post(`{{url_for("get_measures")}}/${x1}/${y1}/${x2}/${y2}`);
		}
	}
}

