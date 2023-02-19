from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from home import views  # Import the views module from the current directory
from home.views import home_page_view, product_detail, purchase_success

app_name = 'home'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('home/', home_page_view, name='home'),
    path('products/', views.products_view, name='products'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('purchase_success/<int:product_id>/',
         views.purchase_success, name='purchase_success'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
