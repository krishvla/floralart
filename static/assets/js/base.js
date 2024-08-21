let cart = JSON.parse(localStorage.getItem('cart')) || {};

function syncCartWithCookies() {
    const cart = localStorage.getItem('cart');
    if (cart) {
        // URL-encode the cart data before setting it in the cookie
        document.cookie = `cart=${encodeURIComponent(cart)};path=/;`;
    } else {
        // Handle the case where localStorage cart is not available
        document.cookie = `cart={};path=/;`;
    }
}


// Call this function to sync the cart data when necessary
syncCartWithCookies();
