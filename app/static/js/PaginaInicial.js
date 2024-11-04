document.getElementById('toggle-contrast').addEventListener('click', function() {
  document.body.classList.toggle('alto-contraste');
    });

function toggleMenu() {
      const menu = document.getElementById("menu");
      menu.style.display = menu.style.display === "block" ? "none" : "block";
    }