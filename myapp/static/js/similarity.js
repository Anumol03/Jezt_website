function showImageThumbnail(input, thumbnailId) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var thumbnail = document.getElementById(thumbnailId);
            thumbnail.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}
function showImageThumbnail(input, thumbnailId) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var thumbnail = document.getElementById(thumbnailId);
            thumbnail.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function openImagePopup(imageId) {
    var popup = document.getElementById("imagePopup");
    var popupImage = document.getElementById("popupImage");
    popupImage.src = document.getElementById(imageId).src;
    popup.style.display = "block";
}

function closeImagePopup() {
    var popup = document.getElementById("imagePopup");
    popup.style.display = "none";
}
function onFormSubmit() {
    // Get references to the form and input elements
    var form = document.getElementById("imageForm");
    var input1 = document.getElementById("formFile1");
    var input2 = document.getElementById("formFile2");

    // Check if both inputs have files selected
    if (input1.files.length > 0 && input2.files.length > 0) {
        // If both inputs have files, submit the form
        form.submit();
    } else {
        // If either input is empty, show an error message or alert
        alert("Please select both images before submitting.");
    }
}