fetch("https://mlaguna.pythonanywhere.com/api/images")
  .then(res => res.json())
  .then(data => {
    const gallery = document.getElementById("gallery");

    data.forEach(img => {
      const image = document.createElement("img");
      image.src = "https://mlaguna.pythonanywhere.com/static/uploads/" + img.filename;
      gallery.appendChild(image);
    });
  })
  .catch(err => console.error(err));
 