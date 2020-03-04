        var desenho = document.getElementById('desenho'),
        rect = {},
        drag = false;

        function init() {
          desenho.addEventListener('mousedown', mouseDown, false);
          desenho.addEventListener('mouseup', mouseUp, false);
          desenho.addEventListener('mousemove', mouseMove, false);
        }
        function mouseDown(e) {
          rect.startX = e.pageX - this.offsetLeft;
          rect.startY = e.pageY - this.offsetTop;
          drag = true;

          document.getElementById("x1").value = rect.startX;
          document.getElementById("y1").value = rect.startY;
        }
        function mouseUp() {
          drag = false;
          draw();
        }
        function mouseMove(e) {
          if (drag) {
            rect.w = (e.pageX - this.offsetLeft) - rect.startX;
            rect.h = (e.pageY - this.offsetTop) - rect.startY;

            document.getElementById("x2").value = rect.startX + rect.w;
            document.getElementById("y2").value = rect.startY + rect.h;
          }
        }
        function draw() {
            var xhttp = new XMLHttpRequest();
            xhttp.open("POST", "{{ url_for('get_measures') }}"
            + "/" + rect.startX + "/" + rect.startY
            + "/" + (rect.startX + rect.w) + "/" + (rect.startY + rect.h), true);
            xhttp.send();
        }
        init();

        function clear_rectangle(){
            var xhttp = new XMLHttpRequest();
            xhttp.open("POST", "{{ url_for('clear_rectangle') }}", true);
            xhttp.send();

            document.getElementById("x1").value = 0;
            document.getElementById("y1").value = 0;
            document.getElementById("x2").value = 0;
            document.getElementById("y2").value = 0;
            document.getElementById("start").disabled = true
        }

        function refresh_rectangle(){
            x1 = document.getElementById("x1").value;
            y1 = document.getElementById("y1").value;
            x2 = document.getElementById("x2").value;
            y2 = document.getElementById("y2").value;
            if(x1.length>=1 && y1.length>=1 && x2.length>=1 && y1.length>=1){
                if(parseInt(x1)>=0 && parseInt(y1)>=0 && parseInt(x2)>=0 && parseInt(y2)>=0){
                    var xhttp = new XMLHttpRequest();
                    xhttp.open("POST", "{{ url_for('get_measures') }}"
                    + "/" + x1 + "/" + y1 + "/" + x2 + "/" + y2, true);
                    xhttp.send();
                }
            }
        }
