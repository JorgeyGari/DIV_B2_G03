// assets/pruebahtml.js

document.addEventListener('DOMContentLoaded', function() {
    var bubbles = document.querySelectorAll('.bubble');

    bubbles.forEach(function(bubble) {
        bubble.addEventListener('mousedown', function() {
            document.getElementById('resultados').style.display = 'none';
        });

        bubble.addEventListener('mouseup', function() {
            document.getElementById('resultados').style.display = 'block';
        });
    });
});
