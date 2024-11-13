document.addEventListener("DOMContentLoaded", () => {
    const minusBtn = document.querySelector(".minus-btn");
    const plusBtn = document.querySelector(".plus-btn");
    const quantityDisplay = document.querySelector(".quantity");

    let quantity = parseInt(quantityDisplay.textContent);

    // Decrease quantity
    minusBtn.addEventListener("click", () => {
        if (quantity > 1) {
            quantity--;
            quantityDisplay.textContent = quantity;
        }
    });

    // Increase quantity
    plusBtn.addEventListener("click", () => {
        quantity++;
        quantityDisplay.textContent = quantity;
    });
});


// send data 

function sendData(data) {
    // Construct the URL with the data as a query parameter
    const url = `/your-server-endpoint?data=${encodeURIComponent(data)}`;

    // Send the GET request using the Fetch API
    fetch(url)
        .then(response => response.text())
        .then(result => {
            console.log("Server response:", result);
        })
        .catch(error => {
            console.error("Error:", error);
        });
}
