# bookstore_project/store/context_processors.py

from .views import get_cart, CART_SESSION_ID # Import helper and constant

def cart_context(request):
    """
    Makes the cart item count available in templates.
    """
    cart = get_cart(request)
    cart_item_count = sum(cart.values()) # Sum of quantities
    return {
        'cart_item_count': cart_item_count
    }