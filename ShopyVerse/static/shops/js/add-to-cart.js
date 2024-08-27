// add-to-cart.js

document.addEventListener('DOMContentLoaded', () => {
    // Event listener for Add to Cart buttons
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', addToCart);
    });
});

function addToCart(event) {
    const button = event.target;
    const productElement = button.closest('.product-item'); // Adjust selector as needed

    const productId = productElement.getAttribute('data-id');
    const productName = productElement.querySelector('.product-name').textContent;
    const productPrice = parseFloat(productElement.querySelector('.product-price').textContent.replace('$', ''));
    const productImage = productElement.querySelector('img').src;
    const productQuantity = 1; // Default quantity

    const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
    
    // Check if item is already in cart
    const existingItemIndex = cartItems.findIndex(item => item.id === productId);
    if (existingItemIndex > -1) {
        // Update quantity if item already exists
        cartItems[existingItemIndex].quantity += productQuantity;
    } else {
        // Add new item
        cartItems.push({
            id: productId,
            name: productName,
            price: productPrice,
            image: productImage,
            quantity: productQuantity
        });
    }

    localStorage.setItem('cartItems', JSON.stringify(cartItems));
    alert('Item added to cart!');
}
