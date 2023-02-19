from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Product
from .models import Purchase
from .forms import PurchaseForm


# View for the user profile page, requiring a user to be logged in
@login_required
def profile(request):
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'purchases': purchases})


# View for the user registration page
def register(request):
    if request.method == 'POST':
        # The form has been submitted
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user and log them in
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    # Render the register template with the form
    return render(request, 'accounts/register.html', {'form': form})


# View for the user login page
def login_view(request):
    if request.method == 'POST':
        # The form has been submitted
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Get the user and log them in
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    # Render the login template with the form
    return render(request, 'accounts/login.html', {'form': form})


# View for the user logout page
def logout_view(request):
    if request.method == 'POST':
        # The user has confirmed logout
        logout(request)
        return redirect('login')
    else:
        # Render the logout confirmation template
        return render(request, 'accounts/confirm_logout.html')


# View for the home page, requiring a user to be logged in
@login_required
def home_page_view(request):
    return render(request, 'homepage/home.html')


# View for the product listing page
def products_view(request):
    # Get all the products
    product_list = Product.objects.all()
    # Paginate the products, showing 10 per page
    paginator = Paginator(product_list, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    # Render the products template with the products data
    return render(request, 'homepage/products.html', {'products': products})


def product_detail(request, product_id):
    # Get the product with the specified id, or return a 404 error if it doesn't exist
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        # The form has been submitted
        form = PurchaseForm(request.POST)
        if form.is_valid():
            # Check if there is enough quantity
            quantity = form.cleaned_data['quantity']
            if product.quantity < quantity:
                # Return an error message if there isn't enough quantity
                return render(request, 'homepage/product_detail.html', {'product': product, 'form': form, 'error_message': 'Sorry, we have none left'})
            # Update the quantity of the product
            product.quantity -= quantity
            product.save()
            # Create a new Purchase object
            purchase = Purchase(user=request.user,
                                product=product, quantity_purchased=quantity)
            purchase.save()
            # Redirect the user to the success page
            return redirect('purchase_success', product_id=product_id)
    else:
        form = PurchaseForm()
    return render(request, 'homepage/product_detail.html', {'product': product, 'form': form})


@login_required
def purchase_success(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    purchase = Purchase.objects.get(product=product, user=request.user)
    quantity_purchased = purchase.quantity_purchased
    return render(request, 'homepage/purchase_success.html', {'product': product, 'quantity_purchased': quantity_purchased})
