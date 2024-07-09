
document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    var helpBtn = document.getElementById('help-btn');
    var popup = document.getElementById('help-popup');
    var popupOverlay = document.getElementById('help-popup-overlay');
    var closeBtn = document.getElementById('close-btn');

    // Show the popup when the help button is clicked
    helpBtn.onclick = function(event) {
        event.preventDefault();
        popup.style.display = 'block';
        popupOverlay.style.display = 'block';
    }

    // Close the popup when the close button is clicked
    closeBtn.onclick = function() {
        popup.style.display = 'none';
        popupOverlay.style.display = 'none';
    }

    // Close the popup when the overlay is clicked
    popupOverlay.onclick = function() {
        popup.style.display = 'none';
        popupOverlay.style.display = 'none';
    }
});
