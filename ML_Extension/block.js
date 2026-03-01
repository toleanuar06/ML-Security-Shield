document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);

    let url = params.get('url');
    let score = params.get('score');

    if (url) document.getElementById('url').innerText = url;
    if (score) document.getElementById('score').innerText = score;
});
