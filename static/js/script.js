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
// document.addEventListener("DOMContentLoaded", function () {
//     // Select all cart action buttons
//     document.querySelectorAll(".cart-action").forEach(button => {
//         button.addEventListener("click", function () {
//             const productId = this.getAttribute("data-product-id");
//             const action = this.getAttribute("data-action");

//             fetch(`/update_cart/${productId}/${action}`, {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                 },
//             })
//             .then(response => response.json())
//             .then(data => {
//                 if ("error" in data) {
//                     console.error("Error:", data.error);
//                     return;
//                 }

//                 // Update the quantity displayed
//                 if (action !== "remove") {
//                     document.querySelector(`#quantity-${productId}`).textContent = `(x${data.quantity})`;
//                     document.querySelector(`#price-${productId}`).textContent = `Price: ${data.price} AMD`;
//                 }

//                 // Update the total price
//                 document.querySelector("#total-price").innerHTML = `<strong>Total price: ${data.total_price} AMD</strong>`;

//                 // If the item is removed, delete the element from the DOM
//                 if (action === "remove") {
//                     document.querySelector(`#cart-item-${productId}`).remove();
//                     document.querySelector(`button[data-product-id="${productId}"][data-action="increase"]`).remove();
//                     document.querySelector(`button[data-product-id="${productId}"][data-action="decrease"]`).remove();
//                     document.querySelector(`button[data-product-id="${productId}"][data-action="remove"]`).remove();
//                 }
//             })
//             .catch(error => console.error("Fetch error:", error));
//         });
//     });
// });

