let fecha = new Date().getFullYear();

document.getElementById('fecha').innerHTML = `${fecha} THE BEST PRICES IN THE AREA 🌿`;

const btn = document.getElementById("menu-btn");
const links = document.getElementById("nav-links");

btn.addEventListener("click", () => {
    links.classList.toggle("active");
});
