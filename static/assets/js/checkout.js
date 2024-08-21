const baseUrl = window.location.origin;
const productBasePath = '/product/';

// Helper function to update localStorage and sync with cookies if needed
function updateLocalStorage(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    document.cookie = `cart=${encodeURIComponent(JSON.stringify(cart))};path=/;`;
}

// Function to calculate and update the total amount and item count in the summary
function updateSummary(cart) {
    let totalAmount = 0;
    let totalItems = 0;

    Object.keys(cart).forEach(id => {
        const item = cart[id];
        totalAmount += item.price * item.quantity;
        totalItems += item.quantity;
    });

    document.getElementById('total_amount').innerText = totalAmount.toFixed(2);
    document.getElementById('total_items').innerText = totalItems;
}

// Function to increase item quantity
function increaseQuantity(id) {
    const cart = JSON.parse(localStorage.getItem('cart')) || {};
    const maxStock = parseInt(document.querySelector(`#product-${id} .product-qty`).getAttribute('max-stock'));

    if (cart[id].quantity < maxStock) {
        cart[id].quantity += 1;
        updateLocalStorage(cart);
        document.querySelector(`#product-${id} .product-qty`).innerText = cart[id].quantity;
        updateSummary(cart);
    }
}

// Function to decrease item quantity
function decreaseQuantity(id) {
    const cart = JSON.parse(localStorage.getItem('cart')) || {};

    if (cart[id].quantity > 1) {
        cart[id].quantity -= 1;
        updateLocalStorage(cart);
        document.querySelector(`#product-${id} .product-qty`).innerText = cart[id].quantity;
        updateSummary(cart);
    }
}

// Function to remove an item from the cart
function removeItem(id) {
    const cart = JSON.parse(localStorage.getItem('cart')) || {};

    delete cart[id];
    updateLocalStorage(cart);
    document.getElementById(`product-${id}`).remove();
    updateSummary(cart);
}

function generateProductViewUrl(productId) {
    return baseUrl + productBasePath + productId + '/';
}
// Function to handle checkout (e.g., send cart details via WhatsApp)
function checkout() {
    const cart = JSON.parse(localStorage.getItem('cart')) || {};
    let cartDetails = '';

    Object.entries(cart).forEach(([id, item]) => {
        const productUrl = generateProductViewUrl(id);

        cartDetails += `*${item.name}*\n`;
        cartDetails += `_Quantity_: ${item.quantity}\n`;
        cartDetails += `_Price_: ₹${item.price.toFixed(2)}\n`;
        cartDetails += `_Total_: ₹${(item.price * item.quantity).toFixed(2)}\n`;
        cartDetails += `_SKU_: ${item.sku}\n`;
        cartDetails += `[View Product](${productUrl})\n`;
        cartDetails += `\n-----------------------\n`;
    });

    const totalAmount = document.getElementById('total_amount').innerText;
    const totalItems = document.getElementById('total_items').innerText;

    const message = `*Checkout details:*\n\n${cartDetails}\n*Total Amount:* ₹${totalAmount}\n*Total Items:* ${totalItems}`;

    const whatsappUrl = `https://api.whatsapp.com/send?phone=+918971550677&text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
}

// Add event listener for checkout button
document.getElementById('checkout-button').addEventListener('click', checkout);


// Adding event listeners to buttons
document.querySelectorAll('.increase-qty').forEach(button => {
    button.addEventListener('click', function() {
        const id = this.closest('.card').getAttribute('id').replace('product-', '');
        console.log(id)
        increaseQuantity(id);
    });
});

document.querySelectorAll('.decrease-qty').forEach(button => {
    button.addEventListener('click', function() {
        const id = this.closest('.card').getAttribute('id').replace('product-', '');
        decreaseQuantity(id);
    });
});

document.querySelectorAll('.btn-remove').forEach(button => {
    button.addEventListener('click', function() {
        const id = this.closest('.card').getAttribute('id').replace('product-', '');
        removeItem(id);
    });
});

// Initial update of the summary when the page loads
document.addEventListener('DOMContentLoaded', function() {
    const cart = JSON.parse(localStorage.getItem('cart')) || {};
    updateSummary(cart);
});

// Add event listener for checkout button
document.getElementById('checkout-button').addEventListener('click', checkout);
