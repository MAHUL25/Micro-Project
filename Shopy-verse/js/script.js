
// Event listener for search button
document.getElementById('search-button').addEventListener('click', function() {
    const query = document.getElementById('search-input').value.trim();
    if (query) {
        window.location.href = `shop.html?search=${encodeURIComponent(query)}`;
    }
});
// Function to add item to cart
function addToCart(name, price, image) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart.push({name, price, image});
    localStorage.setItem('cart', JSON.stringify(cart));
}

// Event listener for add to cart buttons
document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', function() {
        const name = this.getAttribute('data-name');
        const price = this.getAttribute('data-price');
        const image = this.getAttribute('data-image');
        addToCart(name, price, image);
        alert(`${name} has been added to your cart!`);
    });
});

