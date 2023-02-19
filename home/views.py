from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Product
from .models import Purchase
from .forms import PurchaseForm


@login_required
def profile(request):
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'purchases': purchases})


def register(request):
    # If the request method is POST, process the form data
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # If the form is valid, save the user's data and log the user in
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    # If the request method is POST, process the form data
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        # If the form is valid, log the user in
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return render(request, 'accounts/confirm_logout.html')


@login_required
def home_page_view(request):
    return render(request, 'homepage/home.html')


def products_view(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'homepage/products.html', {'products': products})


def product_detail(request, product_id):
    # Get the product with the given id
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'homepage/product_detail.html', {'product': product})


def product_detail(request, product_id):
    # Get the product with the given id
    product = get_object_or_404(Product, pk=product_id)
    

    if request.method == 'POST':
        # The form has been submitted
        form = PurchaseForm(request.POST)
        if form.is_valid():
            # Check if there is enough quantity
            quantity = form.cleaned_data['quantity']
            if product.quantity < quantity:
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
    # Get the product with the given id
    product = get_object_or_404(Product, pk=product_id)

    # Get the purchase with the given product_id and user
    purchase = Purchase.objects.get(product=product, user=request.user)

    # Get the quantity_purchased from the purchase object
    quantity_purchased = purchase.quantity_purchased

    return render(request, 'homepage/purchase_success.html', {'product': product, 'quantity_purchased': quantity_purchased})

