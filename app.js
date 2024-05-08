const cameraBtn = document.getElementById('cameraBtn');
const uploadBtn = document.getElementById('uploadBtn');

cameraBtn.addEventListener('click', () => {
    window.location.href = 'camera.html';
});

uploadBtn.addEventListener('click', () => {
    window.location.href = 'upload.html';
});
