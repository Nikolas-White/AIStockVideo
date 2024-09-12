document.getElementById('upload-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    alert(result.message);
});

document.getElementById('search-button').addEventListener('click', async function() {
    const searchQuery = document.getElementById('search-bar').value;
    const response = await fetch(`/search?q=${encodeURIComponent(searchQuery)}`);
    const videos = await response.json();

    const videoResults = document.getElementById('video-results');
    videoResults.innerHTML = '';

    videos.forEach(video => {
        const videoElement = document.createElement('video');
        videoElement.src = `/download/${video.filename}`;
        videoElement.controls = true;
        videoResults.appendChild(videoElement);
    });
});
