const products = [
    {
        id: 0,
        image: 'images/gg-1.jpg',
        title: 'Z Flip Foldable Mobile',
        price: 120,
    },
    {
        id: 1,
        image: 'images/hh-2.jpg',
        title: 'Air Pods Pro',
        price: 60,
    },
    {
        id: 2,
        image: 'images/ee-3.jpg',
        title: '250D DSLR Camera',
        price: 230,
    },
    {
        id: 3,
        image: 'images/aa-1.jpg',
        title: 'Head Phones',
        price: 100,
    }
];

let cart = [];

function addToCart(productId) {
    const product = products[productId];
    const productInCart = cart.find(item => item.id === product.id);

    if (productInCart) {
        productInCart.quantity += 1;
    } else {
        cart.push({...product, quantity: 1});
    }
    displayCart();
}

function deleteElement(index) {
    cart.splice(index, 1);
    displayCart();
}

function updateQuantity(index, quantity) {
    if (quantity < 1) {
        deleteElement(index);
    } else {
        cart[index].quantity = quantity;
    }
    displayCart();
}

function displayCart() {
    let total = 0;
    let tax = 0;
    let subtotal = 0;

    if (cart.length === 0) {
        document.querySelector('.cart-items').innerHTML = "<p>Your cart is empty</p>";
        document.querySelector(".total").innerHTML = "$0.00";
        document.querySelector("#count").innerHTML = "0";
    } else {
        document.querySelector('.cart-items').innerHTML = cart.map((item, index) => {
            const itemTotal = item.price * item.quantity;
            subtotal += itemTotal;

            return `
                <div class='cart-item'>
                    <img src='${item.image}' alt='${item.title}' />
                    <div class='item-info'>
                        <h3>${item.title}</h3>
                        <p class='price'>$${itemTotal}.00</p>
                    </div>
                    <div class='quantity'>
                        <input type='number' min='1' value='${item.quantity}' 
                            onchange='updateQuantity(${index}, this.value)' />
                    </div>
                    <div class='remove'>
                        <button onclick='deleteElement(${index})'>Remove</button>
                    </div>
                </div>`;
        }).join('');

        tax = subtotal * 0.10; // Example tax rate of 10%
        total = subtotal + tax;

        document.querySelector(".subtotal").innerHTML = `$${subtotal}.00`;
        document.querySelector(".tax").innerHTML = `$${tax.toFixed(2)}`;
        document.querySelector(".total").innerHTML = `$${total.toFixed(2)}`;
        document.querySelector("#count").innerHTML = cart.length;
    }
}

// Example of adding items to the cart (this would normally be called when the user adds a product)
document.querySelector("#checkout-button").addEventListener("click", function() {
    alert("Proceeding to checkout...");
});
