document.addEventListener('DOMContentLoaded', function () {
    // Get product details (these would typically come from the backend)
    const productId = document.getElementById("product-id").textContent; // Example product ID
    const productSKU = document.getElementById("product-sku").textContent;
    const productName = document.getElementById('product-name').textContent;
    const productPrice = parseFloat(document.getElementById('product-price').textContent);
    const productDiscountPrice = parseFloat(document.getElementById('product-discount-price').textContent);
    const maxStock = parseInt(document.getElementById('max-stock').textContent, 10);

    // Update UI based on localStorage
    function updateQuantityUI() {
        document.getElementById('quantity').textContent = cart[productId]?.quantity || 1;
    }

    // Increase quantity
    document.getElementById('increase-qty').addEventListener('click', function () {
        if (!cart[productId]) {
            cart[productId] = { name: productName, price: productPrice, quantity: 0, dicountPrice: productDiscountPrice, sku: productSKU };
        }
        if (cart[productId].quantity < maxStock) {
            cart[productId].quantity++;
            localStorage.setItem('cart', JSON.stringify(cart));
            updateQuantityUI();
        } else {
            alert('Cannot increase quantity beyond available stock.');
        }
    });

    // Decrease quantity
    document.getElementById('decrease-qty').addEventListener('click', function () {
        if (cart[productId] && cart[productId].quantity > 1) {
            cart[productId].quantity--;
            localStorage.setItem('cart', JSON.stringify(cart));
            updateQuantityUI();
        }
    });

    // Add to cart
    document.getElementById('add-to-cart').addEventListener('click', function () {
        if (!cart[productId]) {
            cart[productId] = { name: productName, price: productPrice, quantity: 0, dicountPrice: productDiscountPrice, sku: productSKU };
        }
        cart[productId].quantity = parseInt(document.getElementById('quantity').textContent, 10);
        if (cart[productId].quantity > maxStock) {
            cart[productId].quantity = maxStock;
        }
        localStorage.setItem('cart', JSON.stringify(cart));
        alert('Product added to cart!');
        syncCartWithCookies();
    });

    // Update UI on page load
    updateQuantityUI();
});
