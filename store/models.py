import email
from operator import mod
from pyexpat import model
from statistics import mode
from unicodedata import category
from django.db import models
import django
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_categories():
        categories = Category.objects.all()
        return categories

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'images/products/')

    class Meta:
        db_table = 'products'

    @staticmethod
    def get_all_products():
        products = Product.objects.all()
        return products

    @staticmethod
    def filter_product_by_category_id(cat_id):
        if cat_id:
            return Product.objects.filter(category = cat_id)
        else:
            return Product.get_all_products()

    @staticmethod
    def get_products_by_ids(ids):
        return Product.objects.filter(id__in = ids)

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile_no = models.BigIntegerField()
    password = models.CharField(max_length=500)

    class Meta:
        db_table = 'customers'

class My_Orders(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=200)
    mobile_no = models.BigIntegerField()
    date = models.DateField(default=django.utils.timezone.now)

    class Meta:
        db_table = 'my_orders'

class Orders(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=200)
    mobile_no = models.BigIntegerField(null=True,blank=True)
    date = models.DateField(default=django.utils.timezone.now)
    status = models.CharField(max_length=10, default='Pending')
    
    class Meta:
        db_table = 'orders'

    @staticmethod
    def get_order_by_customer(customer_id):
        return Orders.objects.filter(customer = customer_id).order_by('-date')