document.addEventListener('DOMContentLoaded', () => {
    const markLearningBtn = document.getElementById('mark-learning');
    const clearMarkerBtn = document.getElementById('clear-marker');
    const goMarkerBtn = document.getElementById('go-marker');

    if (markLearningBtn) {
        markLearningBtn.addEventListener('click', () => {
            localStorage.setItem('learningMarker', window.location.href);
            alert('Page marked as learning!');
        });
    }

    if (clearMarkerBtn) {
        clearMarkerBtn.addEventListener('click', () => {
            localStorage.removeItem('learningMarker');
            alert('Marker cleared!');
        });
    }

    if (goMarkerBtn) {
        goMarkerBtn.addEventListener('click', () => {
            const marker = localStorage.getItem('learningMarker');
            if (marker) {
                window.location.href = marker;
            } else {
                alert('No marker set!');
            }
        });
    }
});
