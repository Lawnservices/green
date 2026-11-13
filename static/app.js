// document.getElementById('formulario').addEventListener('submit', async (e) => {
//     e.preventDefault();

//     const nombre = document.getElementById('nombre').value;
//     const telefono = document.getElementById('telefono').value;
//     const mensaje = document.getElementById('mensaje').value;

//     await fetch('https://www.creantunegocio.com/mensajesnuevo', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             nombre,
//             telefono,
//             mensaje
//         })
//     });

// });

document.getElementById("name").addEventListener("input", function () {
    this.value = this.value.replace(/[^A-Za-z\s]/g, "");

    if (this.value.length < 3) {
        this.setCustomValidity("The name must be at least 3 characters long.");
    }
    else if (this.value.length > 30) {
        this.setCustomValidity("The name is too long.");
    }
    else {
        this.setCustomValidity("");
    }
});


document.getElementById("tel").addEventListener("input", function () {
    this.value = this.value.replace(/[^0-9]/g, "");

    if (this.value.length < 10) {
        this.setCustomValidity("The number must have 10 digits.");
    } else {
        this.setCustomValidity("");
    }
});

document.querySelector("form").addEventListener("submit", function () {
    setTimeout(() => {
        this.reset();
    }, 500);
});