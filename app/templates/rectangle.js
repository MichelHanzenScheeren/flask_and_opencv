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
        }

        function mouseUp() {
          drag = false;
          draw();
        }

        function mouseMove(e) {
          if (drag) {
            rect.w = (e.pageX - this.offsetLeft) - rect.startX;
            rect.h = (e.pageY - this.offsetTop) - rect.startY ;
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
