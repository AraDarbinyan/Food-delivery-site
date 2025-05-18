document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".cart-action").forEach(button => {
        button.addEventListener("click", function () {
            let productId = this.dataset.productId;
            let action = this.dataset.action;

            fetch(`/update_cart/${productId}/${action}`, {
                method: "POST",
                headers: { "X-Requested-With": "XMLHttpRequest" }
            })
                .then(response => response.json())
                .then(data => {
                    if ("error" in data) {
                        alert(data.error);
                    } else if (action === "remove") {
                        document.querySelector(`#cart-item-${productId}`).remove();
                        document.querySelector(`button[data-product-id="${productId}"][data-action="increase"]`).remove();
                        document.querySelector(`button[data-product-id="${productId}"][data-action="decrease"]`).remove();
                        document.querySelector(`button[data-product-id="${productId}"][data-action="remove"]`).remove();
                        document.querySelector("#total-price").textContent = `Total price: ${data.total_price} AMD`;
                    } else {
                        let quantityElement = document.querySelector(`#quantity-${productId}`);
                        let priceElement = document.querySelector(`#price-${productId}`);
                        let totalPriceElement = document.querySelector("#total-price");

                        if (data.quantity === 0) {
                            let itemRow = document.querySelector(`#cart-item-${productId}`);
                            if (itemRow) {
                                itemRow.remove();
                            }
                        }
                        else {

                            quantityElement.textContent = `(x${data.quantity})`;
                            priceElement.textContent = `Price: ${data.item_total_price} AMD`;
                        }

                        totalPriceElement.textContent = `Total price: ${data.total_price} AMD`;
                    }
                })
                .catch(error => console.error("Error:", error));
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            let productId = this.dataset.productId;

            fetch(`/add_to_cart/${productId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                }
            })
                .then(response => response.json())
                .then(data => {
                    if ("error" in data) {
                        alert(data.error);
                    } else {
                        let existingMessage = document.querySelector(`#message-${productId}`);
                        if (existingMessage) existingMessage.remove();

                        // Create a success message
                        let message = document.createElement("p");
                        message.id = `message-${productId}`;
                        message.textContent = "Added to cart!";
                        message.classList.add("cart-success-message");

                        // Append message below the button
                        this.parentElement.appendChild(message);

                        // Force reflow to ensure CSS is applied
                        setTimeout(() => {
                            message.classList.add("show"); // Add a class for transition effect
                        }, 10);

                        // Remove message after 3 seconds
                        setTimeout(() => {
                            message.remove();
                        }, 3000);
                    }
                })
                .catch(error => console.error("Error:", error));
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("registerForm").addEventListener("submit", function (event) {
        let email = document.getElementById("email").value;
        let phone = document.getElementById("phone").value;

        let emailPattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
        let phonePattern = /^\+?\d{1,3}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$/;

        if (!emailPattern.test(email) && !phonePattern.test(phone)) {
            alert("Invalid email and phone formats");
            event.preventDefault();
        }
        else if (!emailPattern.test(email)) {
            alert("Invalid email format");
            event.preventDefault();
        }
        else if (!phonePattern.test(phone)) {
            alert("Invalid phone number");
            event.preventDefault();
        }
    });
});

setTimeout(function () {
    let flashMessages = document.querySelectorAll(".flashes li");
    flashMessages.forEach(msg => msg.style.display = "none");
}, 3000); 