from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pic/', default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    

class seller_list(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    seller_username = models.CharField(max_length=100, unique=True)  
    seller_email = models.EmailField(max_length=50, unique=True) 
    seller_password = models.CharField(max_length=100)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.seller_username
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    description = models.TextField(blank=True, null=True)  

    def __str__(self):
        return self.name

# class ProductModel(models.Model):
#     details = models.TextField()
#     product_name = models.CharField(max_length=255)  
#     price = models.FloatField(default=0.0)
#     product_photos = models.ImageField(upload_to='product_photos/', blank=True, null=True)
#     category = models.CharField(
#         max_length=50,
#         choices=[('cat', 'Cat'), ('dog', 'Dog'), ('bird', 'Bird')],
#         default='cat'  # Default value here
#     ) 
#     seller = models.ForeignKey(seller_list, on_delete=models.CASCADE, related_name='products', null=True, blank=True)

#     def __str__(self):
#         return self.product_name



class ProductModel(models.Model):
    details = models.TextField()
    product_name = models.CharField(max_length=255)  
    price = models.FloatField(default=0.0)
    breed = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10,default='male', choices=[('Male', 'Male'), ('Female', 'Female')])
    is_vaccinated = models.BooleanField(default=False)
    color = models.CharField(max_length=50, null=True, blank=True)
    product_photos = models.ImageField(upload_to='product_photos/', blank=True, null=True)
    images = models.ImageField(upload_to='product_imagess/', blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(
        max_length=50,
        choices=[('cat', 'Cat'), ('dog', 'Dog'), ('bird', 'Bird')],
        default=''  
    ) 
    seller = models.ForeignKey(seller_list, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    product_status = models.CharField(
        max_length=50,
        choices=[
            ('Stock In', 'Stock In'),
            ('Stock Out', 'Stock Out'),
        ],
        default='Stock In'
    )
    
    def discount_amount(self):
        return self.price - self.discounted_price

    def __str__(self):
        return self.product_name
    
 

class sellerProfile(models.Model):
    sellers = models.OneToOneField(seller_list, on_delete=models.CASCADE)
    sellerprofile_picture = models.ImageField(upload_to='sellerprofile_pic/', default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sellers.seller_username} Profile'


class PetCategory(models.Model):
    petname = models.CharField(max_length=100, unique=True)  
    pet_description = models.TextField(blank=True, null=True)  

    def __str__(self):
        return self.petname
    
class DonationModel(models.Model):
    pet_details = models.TextField()
    reason = models.TextField()  
    pet_name = models.CharField(max_length=255)  
    pet_photos = models.ImageField(upload_to='pet_photos/', blank=True, null=True)
    pet_category = models.CharField(
        max_length=50,
        choices=[('cat', 'Cat'), ('dog', 'Dog'), ('bird', 'Bird')],
        default=''  
    ) 
    pet_breed = models.CharField(max_length=100, null=True, blank=True)
    pet_age = models.IntegerField(null=True, blank=True)
    pet_gender = models.CharField(max_length=10,default='male', choices=[('Male', 'Male'), ('Female', 'Female')])
    vaccinated = models.BooleanField(default=False)
    pet_color = models.CharField(max_length=50, null=True, blank=True)
    seller = models.ForeignKey('seller_list', on_delete=models.CASCADE, related_name='donation', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pet_name
    
class CartItem(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.product_name}'
    
class wishlistitem(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.product_name}'



    
STATE_CHOICES = [
    ('Alappuzha', 'Alappuzha'),
    ('Ernakulam', 'Ernakulam'),
    ('Idukki', 'Idukki'),
    ('Kanoor', 'Knoor'),
    ('Kasargod', 'Kasargod'),
    ('Kollam', 'Kollam'),
    ('Kottayam', 'Kottayam'),
    ('Kozhikod', 'Kozhikod'),
    ('Malappuram', 'Malappuram'),
    ('Palakkad', 'Palakkad'),
    ('Pathanamthitta', 'Pathanamthitta'),
    ('Trisure', 'Trisure'),
    ('Thiruvananthapuram', 'Thiruvananthapuram'),
    ('Vayanad', 'Vayanad'),
]



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    building_name = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100,null=False, default='Unknown')
    district = models.CharField(max_length=100, choices=STATE_CHOICES, null=True, blank=True)
    PIN = models.CharField(max_length=100)
    default = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, default="1234567890")


    def __str__(self):
        return self.user.username



class AdoptionRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey(seller_list, on_delete=models.CASCADE, related_name="received_requests",null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    pet_name = models.CharField(max_length=100,default='no name')
    donation = models.ForeignKey(DonationModel, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'),('Delivered','Delivered')],
        default='Pending'
    )
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.pet_name} - {self.status}"
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    seller = models.ForeignKey(seller_list, on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    status = models.CharField(
        max_length=50,
        choices=[
            ('Order Processing', 'Order Processing'),
            ('confirm', 'Confirm'),
            ('Cancelled', 'Cancelled'),
            ('Delivered','Delivered')
        ],
        default='Order Processing'
    )
    cancellation_date = models.DateField(null=True, blank=True)
    refund_date = models.DateField(null=True, blank=True)
    order_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    def get_cart_items(self):
        return CartItem.objects.filter(user=self.user)
    def cancel_order(self):
        self.status = 'Cancelled'
        self.save()



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    seller = models.ForeignKey(seller_list, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Each user has one cart
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    # def total_price(self):
    #     """Calculate total price of items in the cart."""
    #     total = sum(item.product.price * item.quantity for item in self.cart_items.all())
    #     return total

    # def clear_cart(self):
    #     """Clear all items in the cart."""
    #     self.cart_items.all().delete()

    # def add_item(self, product, quantity=1):
    #     """Add a product to the cart."""
    #     cart_item, created = CartItem.objects.get_or_create(
    #         cart=self, product=product, defaults={'quantity': quantity}
    #     )
    #     if not created:
    #         cart_item.quantity += quantity  # If item already in cart, increase quantity
    #         cart_item.save()

    # def remove_item(self, product):
    #     """Remove a product from the cart."""
    #     CartItem.objects.filter(cart=self, product=product).delete()

