from django.db import models
from django.contrib.auth.models import User

# Create your models here.
Brand = {
    ('mac', 'MAC'),
    ('emelie', 'Emelie'),
    ('miss rose', 'Miss Rose'),
    ('benefit', 'Benefit'),

}
SubCategory_Choices = (
    # ('foundation', 'Foundation'),
    # ('lips', 'Lips'),
    # ('eyes', 'Eyes'),
    # ('face', 'Face'),
    # ('blenders', 'Blenders'),
    # ('hair spray', 'Hair Spray'),
    # ('brushes', 'Brushes'),
    ('men', 'men'),
    ('women', 'women'),
)
Category_Choices = (
    # ('waterproof foundation', 'WaterProof Foundation'),
    # ('glossy lipsticks', 'Glossy Lipsticks'),
    ('shirts', 'shirts'),
    ('trousers', 'trousers'),
    ('shoes', 'shoes'),
    ('bags', 'bags'),
    ('pent', 'pent'),
    ('short', 'short'),
)
Label_Choices = (
    ('null', 'Null'),
    ('new', 'New'),
    ('off', 'Off'),
    ('top', 'Top'),
)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=500)
    label = models.CharField(max_length=8, choices=Label_Choices, default='null')
    shortdescription = models.TextField(max_length=5000, blank=True)
    longdescription = models.TextField(max_length=5000, blank=True)
    category = models.CharField(max_length=20, choices=Category_Choices, default='shirts')
    subcategory = models.CharField(max_length=50, choices=SubCategory_Choices, default='men')
    price = models.IntegerField(default=0)
    imagefront = models.ImageField(upload_to="product/", blank=True)
    imageback = models.ImageField(upload_to="product/", blank=True)
    imageother1 = models.ImageField(upload_to="product/", blank=True)
    imageother2 = models.ImageField(upload_to="product/", blank=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    address = models.CharField(max_length=300, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    phone = models.PositiveBigIntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Review(models.Model):
    products = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    desription = models.CharField(max_length=300, null=True)
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.rating
