
// Get all nav links
const navLinks = document.querySelectorAll('.nav-link');

// Get the current path
const currentPath = window.location.pathname;

// Loop through links and add 'active' class if the href matches the current path
navLinks.forEach(link => {
  if (link.getAttribute('href') === currentPath) {
    link.classList.add('active');
  }
});

// Redirect to cart page when click on shpping cart icon
let iconCart = document.querySelector('.icon-cart');

iconCart.addEventListener('click', () => {
    window.location.href = '/cart';
});

//Hamburger menu
const hamburgerMenu = document.querySelector(".hamburger-menu");

const navMenu = document.querySelector(".nav-menu");

hamburgerMenu.addEventListener("click", () => {
    hamburgerMenu.classList.toggle("active");
    navMenu.classList.toggle("active");
})

document.querySelectorAll(".nav-link").forEach(n => n.addEventListener("click", () => {
        hamburgerMenu.classList.remove("active");
        navMenu.classList.remove("active");
}))

document.addEventListener('DOMContentLoaded', function () {
    // Add to Cart Functionality
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            const productId = this.getAttribute('data-product-id');

            fetch(`/add-to-cart/${productId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
                .then(response => {
                    console.log('Raw response:', response);
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Parsed server response:', data);
                    if (!data || typeof data !== 'object') {
                        throw new Error('Invalid server response');
                    }

                    // Update Cart Count
                    const cartCountElement = document.getElementById('cart-count');
                    if (cartCountElement) {
                        cartCountElement.textContent = data.cart_count;
                    }


                    // Update Quantity for the Product
                    const quantityElement = document.getElementById(`product-quantity-${data.product_id}`);
                    if (quantityElement) {
                        quantityElement.textContent = `x${data.new_quantity}`;
                        quantityElement.style.display = 'inline-block'; // Ensure it becomes visible
                        console.log(`Updated quantity for product ${data.product_id}`);
                    } else {
                        console.warn(`Quantity element not found for product ${data.product_id}`);
                    }

                    // Add or Update .back_col
                    const productElement = document.querySelector(`#pizza_col .add-to-cart[data-product-id="${data.product_id}"]`);
                    if (productElement) {
                        const backColElement = productElement.closest('.box').querySelector('.back_col');
                        if (backColElement) {
                            backColElement.style.display = 'block'; // Show the .back_col
                            console.log(`Displayed .back_col for product ${data.product_id}`);
                        } else {
                            console.warn(`.back_col not found for product ${data.product_id}`);
                        }
                    } else {
                        console.warn(`Product element not found for product ${data.product_id}`);
                    }

                    // Update Item Quantity and Subtotal
                    const itemElement = document.getElementById(`cart-item-${productId}`);
                    if (itemElement) {
                        itemElement.querySelector('.item-quantity').textContent = data.new_quantity;
                        itemElement.querySelector('.item-subtotal').textContent = data.subtotal.toFixed(2);
                    }

                    // Update Total Price
                    const totalPriceElement = document.getElementById('total-price');
                    if (totalPriceElement) {
                        totalPriceElement.textContent = data.total_price.toFixed(2);
                    }
                })
                .catch(error => console.error('Error adding to cart:', error));
        });
    });

    // Remove from Cart Functionality
    document.querySelectorAll('.remove-from-cart').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            const productId = this.getAttribute('data-product-id');

            fetch(`/remove-from-cart/${productId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
                .then(response => response.json())
                .then(data => {
                    // Update Cart Count
                    const cartCountElement = document.getElementById('cart-count');
                    if (cartCountElement) {
                        cartCountElement.textContent = data.cart_count;
                    }

                    // Update or Remove Item from List
                    const itemElement = document.getElementById(`cart-item-${productId}`);
                    if (itemElement) {
                        if (data.new_quantity > 0) {
                            itemElement.querySelector('.item-quantity').textContent = data.new_quantity;
                            itemElement.querySelector('.item-subtotal').textContent = data.subtotal.toFixed(2);
                        } else {
                            itemElement.remove();
                        }
                    }

                    // Update Total Price
                    const totalPriceElement = document.getElementById('total-price');
                    if (totalPriceElement) {
                        totalPriceElement.textContent = data.total_price.toFixed(2);
                    }
                })
                .catch(error => console.error('Error removing from cart:', error));
        });
    });
});

