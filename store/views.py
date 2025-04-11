# bookstore_project/store/views.py
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.shortcuts import render
from django.db.models import Q, CharField # Import Q for OR queries, CharField for casting
from django.db.models.functions import Cast # Import Cast function
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from .models import Book
from decimal import Decimal # For accurate price calculations
from store import views

# --- Constants ---
CART_SESSION_ID = 'cart' # Key used to store the cart in the session

def get_cart(request):
    """Retrieves the cart dictionary from the session."""
    cart = request.session.get(CART_SESSION_ID, {})
    # Ensure keys are strings (as they should be in sessions)
    # and values are integers (quantities).
    cleaned_cart = {}
    for book_id, quantity in cart.items():
        try:
            # Keep book_id as a string, ensure quantity is an integer
            cleaned_cart[str(book_id)] = int(quantity)
        except (ValueError, TypeError):
            # Skip invalid entries (e.g., non-integer quantity)
            pass
    # It's good practice to update the session if cleaning occurred
    # Although maybe not strictly necessary if called read-only sometimes
    # request.session[CART_SESSION_ID] = cleaned_cart
    # request.session.modified = True
    return cleaned_cart
# --- View Functions ---

def book_list_view(request):
    """Displays the list of available books."""
    # Start with all books
    books = Book.objects.all()
    
    # Get the search term from the URL ?search=...
    search_query = request.GET.get('search', '')
    
    if search_query:
        # If a search term is provided, filter the queryset
        # We cast numerical/date fields to CharField for text searching with icontains
        books = books.annotate(
            price_str=Cast('price', output_field=CharField()),
            pub_date_str=Cast('publication_date', output_field=CharField()),
        ).filter(
            Q(title__icontains=search_query) |        # Check title (case-insensitive)
            Q(author__icontains=search_query) |       # Check author (case-insensitive)
            Q(price_str__icontains=search_query) |    # Check price as text (case-insensitive)
            Q(pub_date_str__icontains=search_query)   # Check publication_date as text (case-insensitive)
        )
    
    # Apply a simple default ordering
    books = books.order_by('title')
    
    # Prepare the cart item count for the header
    cart = get_cart(request)
    cart_item_count = sum(cart.values())
    
    context = {
        'books': books,
        'cart_item_count': cart_item_count
    }
    return render(request, 'store/book_list.html', context)

@require_POST # Ensure this view only accepts POST requests
def add_to_cart_view(request, book_pk):
    """Adds a book to the session cart."""
    cart = get_cart(request)
    book = get_object_or_404(Book, pk=book_pk) # Get the book or return 404

    book_id_str = str(book.pk) # Use string keys for session dictionary

    quantity = cart.get(book_id_str, 0) # Get current quantity or default to 0
    cart[book_id_str] = quantity + 1 # Increment quantity

    request.session[CART_SESSION_ID] = cart # Save the updated cart back to the session
    request.session.modified = True # Mark session as modified

    # Redirect back to the book list page after adding
    return redirect('store:book_list')

def cart_view(request):
    """Displays the contents of the shopping cart."""
    cart_session = get_cart(request) # Get {book_id: quantity} from session
    cart_items = []
    total_price = Decimal('0.00') # Use Decimal for currency

    # Fetch book objects based on IDs in the cart
    book_ids = cart_session.keys()
    books_in_cart = Book.objects.filter(pk__in=book_ids)

    # Prepare items for the template, including quantity and subtotal
    for book in books_in_cart:
        quantity = cart_session.get(str(book.pk), 0) # Get quantity for this book
        if quantity > 0:
            subtotal = book.price * quantity
            cart_items.append({
                'book': book,
                'quantity': quantity,
                'subtotal': subtotal,
            })
            total_price += subtotal

    # The 'back_url' is simply the book list URL as requested
    back_url = reverse('store:book_list')

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'back_url': back_url, # Pass the back URL to the template
        'cart_item_count': sum(cart_session.values())
    }
    return render(request, 'store/cart.html', context)


@require_POST
def remove_from_cart_view(request, book_pk):
    """Removes one instance of a book from the cart."""
    cart = get_cart(request)
    book_id_str = str(book_pk)

    if book_id_str in cart:
        if cart[book_id_str] > 1:
            cart[book_id_str] -= 1 # Decrease quantity
        else:
            del cart[book_id_str] # Remove item if quantity becomes 0

        request.session[CART_SESSION_ID] = cart
        request.session.modified = True

    return redirect('store:cart') # Redirect back to the cart page

@require_POST
def clear_cart_view(request):
    """Removes all items from the cart."""
    if CART_SESSION_ID in request.session:
        del request.session[CART_SESSION_ID]
        request.session.modified = True
    return redirect('store:cart') # Redirect back to the cart page


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # --- Updated Redirect Logic ---
                # Get the 'next' URL from POST data
                redirect_to = request.POST.get('next', '')

                # Basic check: If 'next' is empty or looks unsafe,
                # default to LOGIN_REDIRECT_URL defined in settings.py
                # (You might add more robust validation if needed)
                if not redirect_to or redirect_to.startswith('//') or ' ' in redirect_to:
                    redirect_to = settings.LOGIN_REDIRECT_URL # Default redirect URL

                # Use resolve_url to handle named URLs or paths correctly
                # This prevents errors if redirect_to is already a path like '/'
                # or if it's a URL name like 'store:book_list'
                return redirect(resolve_url(redirect_to))
                # --- End of Updated Logic ---

            else:
                # Invalid login - Add an error message to the form or context if desired
                # print("Invalid login attempt") # For debugging
                pass # Fall through to re-render the form
    else: # GET request
        form = AuthenticationForm()

    # Get 'next' for the template context (for the hidden input)
    next_url = request.GET.get('next', '')
    context = {'form': form, 'next': next_url}
    return render(request, 'store/login.html', context)

# @login_required # Optional: Make logout only accessible if logged in
def logout_view(request):
    """Logs the user out."""
    logout(request)
    # Redirect to the location specified in settings.LOGOUT_REDIRECT_URL
    return redirect('store:login') # Or redirect('store:book_list')