document.querySelectorAll(".cart-action").forEach(button => {
    button.addEventListener("click", function() {
        let productId = this.dataset.productId;
        let action = this.dataset.action;
        let quantityElement = document.getElementById(`quantity-${productId}`);
        let priceElement = document.getElementById("total-price");

        fetch(`/update_cart/${productId}/${action}`, { method: "POST" })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                if (action === "remove" || data.quantity === 0) {
                    document.getElementById(`cart-item-${productId}`).remove();
                } else {
                    quantityElement.innerText = `(x${data.quantity})`;
                }
                priceElement.innerText = `Total price: ${data.total_price} AMD`;
            }
        });
    });
});