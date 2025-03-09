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
                if (data.message) {
                    alert(data.message);  
                } else if (data.error) {
                    alert(data.error);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
