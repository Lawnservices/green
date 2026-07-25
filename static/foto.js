fetch("https://www.creantunegocio.com/api/images")
  .then(res => res.json())
  .then(data => {
    const gallery = document.getElementById("gallery");

    data.forEach(img => {
      const image = document.createElement("img");
      image.src = "https://www.creantunegocio.com/static/uploads/" + img.filename;
      gallery.appendChild(image);
    });
  })
  .catch(err => console.error(err));
 