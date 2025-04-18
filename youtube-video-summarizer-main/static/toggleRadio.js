document.addEventListener("DOMContentLoaded", function () {
    const radios = document.querySelectorAll("input[type='radio']");

    radios.forEach((radio) => {
        radio.addEventListener("click", function (e) {
            // If the radio button is already selected, deselect it
            if (this.checked && this.previousChecked) {
                this.checked = false;
                this.previousChecked = false;
            } else {
                // Otherwise, mark it as selected
                this.previousChecked = true;
            }
        });
    });
});