from django.db import models
from django.contrib.auth import get_user_model

# Get the user model from the Django auth app
User = get_user_model()


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField()

    # String representation of product name
    def __str__(self):
        return self.name


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity_purchased = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)

    # unique together constraint for the user and product fields
    class Meta:
        unique_together = ('user', 'product')
    
    # String representation of a purchase
    def __str__(self):
        return f"{self.user.username} purchased {self.product.name} on {self.date}"

    # Method to get the total price of a purchase
    def get_total_price(self):
        return self.product.price * self.quantity_purchased

