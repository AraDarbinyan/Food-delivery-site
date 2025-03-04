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
                } else {
                    let quantityElement = document.querySelector(`#quantity-${productId}`);
                    let priceElement = document.querySelector(`#price-${productId}`);
                    let totalPriceElement = document.querySelector("#total-price");

                    if (data.quantity === 0) {
                        document.querySelector(`#cart-item-${productId}`).remove();
                    } else {

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