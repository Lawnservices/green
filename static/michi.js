function scrollToSection(id) {
    document.getElementById(id).scrollIntoView({ behavior: "smooth" });
}

function playVideo(videoId, title) {

    const player = document.getElementById("youtubePlayer");
    const placeholder = document.getElementById("playerPlaceholder");
    const videoTitle = document.getElementById("videoTitle");

    // Ocultar imagen inicial
    placeholder.style.display = "none";

    // Mostrar video
    player.style.display = "block";

    player.src =
        "https://www.youtube.com/embed/" +
        videoId +
        "?autoplay=1&rel=0";

    // Cambiar título
    videoTitle.textContent = title;

    // Subir al reproductor
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}