from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .forms import ProfileUpdateForm,ProductListForm,ProfileForm,DonationForm,AddressForm,AdoptionRequestForm
from django.views.generic.edit import DeleteView,UpdateView
from django.urls import reverse
from .models import seller_list,ProductModel,Profile,sellerProfile,DonationModel,CartItem,wishlistitem,Address,AdoptionRequest,Order,OrderItem
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from .models import ProductModel 



def index(request):
    notifications = AdoptionRequest.objects.filter(status="pending")  
    return render(request, 'index.html', {'notifications': notifications})

# sing up,log in and profile of users

def sign_up(request): 
    if request.method == 'POST':
        f_name=request.POST['Fname']
        u_name=request.POST['Uname']
        email=request.POST['email']
        password1=request.POST['password']
        password2=request.POST['cpassword']
        profile_picture = request.FILES.get('profile_picture')

        if password1==password2:
            if User.objects.filter(username=u_name).exists():
                messages.info(request,"username alredy exist")
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email alredy exist")
                return redirect('sign_up')

            else:
                user=User.objects.create_user(first_name=f_name,username=u_name,email=email,password=password1)
                user.save()
                Profile.objects.create(user=user, profile_picture=profile_picture)
                return redirect('log_in')
            
        else:
            messages.info(request,"password are not matching") 
            return render(request,'sign_up.html')
    else:
        return render(request,'sign_up.html')
    

def log_in(request):
    if request.method=="POST":
        u_name=request.POST['Uname']
        password1=request.POST['password']
        user=auth.authenticate(username=u_name,password=password1)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,'invalid username or password')
            return redirect('log_in')
    else:
        return render(request,'log_in.html')
    
def logout(request):
    auth.logout(request)
    return redirect('index')

def myaccount(request):
    return render(request,"my-account.html")


def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)  
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')  
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, "profile.html", {"form": form, "profile": profile})


def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        if username != user.username and User.objects.filter(username=username).exists():
            messages.info(request,"username alredy exist")
            return redirect('edit_profile')
        if email != user.email and User.objects.filter(email=email).exists():
            messages.info(request,"email alredy exist")
            return redirect('edit_profile')
        user.first_name = request.POST['first_name']
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()

        profile = user.profile  
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()

        messages.success(request, 'Your profile has been updated!')
        return redirect('profile')  
    



    profile = request.user.profile
    return render(request, 'edit_profile.html', {'profile': profile})

        

# sing up,log in and profile of seller

def selleraccount(request):
    return render(request,"seller_accound.html")


def account(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            user_name = request.POST.get('usern')
            e_mail = request.POST.get('em_ail')
            passw = request.POST.get('passwd')
            sellerprofile_picture = request.FILES.get('sellerprofile_picture')

            if seller_list.objects.filter(seller_username=user_name).exists():
                messages.error(request, "Username already taken.")
                return redirect('account') 
            if seller_list.objects.filter(seller_email=e_mail).exists():
                messages.error(request, "Email already taken.")
                return redirect('account') 

            sellers = seller_list(seller_username=user_name, seller_password=passw, seller_email=e_mail)
            sellers.save()


            sellerProfile.objects.create(sellers=sellers, sellerprofile_picture=sellerprofile_picture)
            messages.success(request, "Seller registered successfully!")
            return redirect('account')

        if 'login' in request.POST:
            user_name = request.POST.get('usern')
            passw = request.POST.get('passwd')


            try:
                sellers = seller_list.objects.get(seller_username=user_name)
                if sellers.seller_password == passw:
                    request.session['seller_id'] = sellers.id 
                    return redirect('index')
                else:
                    messages.error(request, "Invalid username or password.")
            except seller_list.DoesNotExist:
                messages.error(request, "Seller not found.")

    return render(request, "acut.html")



def sellerprofile_view(request):
    seller_id = request.session.get('seller_id')
    if not seller_id:
        messages.error(request, "No seller information found.")
        return redirect('login') 

    try:
        seller = seller_list.objects.get(id=seller_id)
    except seller_list.DoesNotExist:
        messages.error(request, "Seller not found.")
        return redirect('login')  

    sprofile, created = sellerProfile.objects.get_or_create(sellers=seller)

    if request.method == 'POST':

        seller.seller_username = request.POST.get('username', seller.seller_username)
        seller.seller_email = request.POST.get('email', seller.seller_email)
        seller.save()


        form = ProfileForm(request.POST, request.FILES, instance=sprofile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('sellerprofile')
    else:
        form = ProfileForm(instance=sprofile)

    return render(request, "seller_profile.html", {"profile": sprofile, "seller": seller})




def edit_sellerprofile(request):
    seller_id = request.session.get('seller_id')
    seller = seller_list.objects.get(id=seller_id)
    sprofile = sellerProfile.objects.get(sellers=seller)

    if request.method == 'POST':

        seller_username = request.POST['username']
        seller_email = request.POST['email']
        if seller_username != seller.seller_username and seller_list.objects.filter(seller_username=seller_username).exists():
            messages.info(request,"username alredy exist")
            return redirect('edit_sellerprofile')
        if seller_email != seller.seller_email and seller_list.objects.filter(seller_email=seller_email).exists():
            messages.info(request,"email alredy exist")
            return redirect('edit_sellerprofile')


        seller.seller_username = request.POST.get('username', seller.seller_username)
        seller.seller_email = request.POST.get('email', seller.seller_email)
        seller.save()

        form = ProfileForm(request.POST, request.FILES, instance=sprofile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('sellerprofile')
    else:
        form = ProfileForm(instance=sprofile)

    return render(request, 'edit_sellerprofile.html', {'form': form, 'profile': sprofile, 'seller': seller})


# product details

def product(request):
    products = ProductModel.objects.all
    return render(request, 'product.html', {'products': products})

def product_details(request, product_id):
    if not request.user.is_authenticated:
        return redirect('log_in')

    product = get_object_or_404(ProductModel, id=product_id)
    seller = product.seller


    context = {
        'product': product,
        'seller': seller,
    }
    return render(request, 'product_details.html', context)

def cat_products_view(request):
    cat_products = ProductModel.objects.filter(category='cat') 
    return render(request, 'cat_product.html', {'cat_products': cat_products})

def dog_products_view(request):
    dog_products = ProductModel.objects.filter(category='dog')  
    return render(request, 'dog_product.html', {'dog_products': dog_products})

def bird_products_view(request):
    bird_products = ProductModel.objects.filter(category='bird')  
    return render(request, 'bird_product.html', {'bird_products': bird_products})

def search_products(request):
    query = request.GET.get('q', '')
 
    category_order = {'cat': 1, 'dog': 2, 'bird': 3}
    

    products = ProductModel.objects.filter(
        Q(product_name__icontains=query) | Q(details__icontains=query) | Q(category__icontains=query)
    ).order_by('category')

    data = []
    for product in products:
        data.append({
            'name': product.product_name,
            'price': product.price,
            'image_url': product.product_photos.url if product.product_photos else '',
            'detail_url': f"/product/{product.id}/",  # Adjust this to match your URL structure
            'category_priority': category_order.get(product.category, 999)  # Assign priority
        })

    # Sort the results based on category priority
    data.sort(key=lambda x: x['category_priority'])

    return JsonResponse({'products': data})

class MyView(View):
    def get(self, request, pk=None):
        # Get the seller ID from the session
        seller_id = request.session.get('seller_id')
        if not seller_id:
            return render(request, 'error.html', {'error': 'No seller information found in session.'})

        # Fetch the logged-in seller
        try:
            seller = seller_list.objects.get(id=seller_id)
        except seller_list.DoesNotExist:
            return render(request, 'error.html', {'error': 'Invalid seller ID.'})

        # Filter products corresponding to the logged-in seller
        data = ProductModel.objects.filter(seller=seller)

        # Edit mode if pk is provided, otherwise add mode
        if pk:
            instance_edited = get_object_or_404(ProductModel, pk=pk, seller=seller)  # Ensure product belongs to seller
            form = ProductListForm(instance=instance_edited)
        else:
            form = ProductListForm()

        return render(request, 'add_product.html', {'form': form, 'data': data})

    def post(self, request, pk=None):
        # Get the seller ID from the session
        seller_id = request.session.get('seller_id')
        if not seller_id:
            return render(request, 'error.html', {'error': 'No seller information found in session.'})

        # Fetch the logged-in seller
        try:
            seller = seller_list.objects.get(id=seller_id)
        except seller_list.DoesNotExist:
            return render(request, 'error.html', {'error': 'Invalid seller ID.'})

        # Handle form submission for editing or adding
        if pk:
            instance = get_object_or_404(ProductModel, pk=pk, seller=seller)
            form = ProductListForm(request.POST, request.FILES, instance=instance)
        else:
            form = ProductListForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = seller  # Assign the current seller to the product
            product.save()
            return redirect('addproduct')  # Redirect after success

        # Reload with errors if form is invalid
        data = ProductModel.objects.filter(seller=seller)
        return render(request, 'add_product.html', {'form': form, 'data': data})


class Deleteview(View):
    def get(self, request, pk):
        instance = get_object_or_404(ProductModel, pk=pk)
        instance.delete()
        return redirect('addproduct')



# donation and adoption


def adoption(request):
    products = DonationModel.objects.all
    return render(request, 'adoption.html', {'products': products})

def adoption_details(request, product_id):
    if not request.user.is_authenticated:
        return redirect('log_in')
    # Fetch the product based on the provided product ID
    product = get_object_or_404(DonationModel, id=product_id)

    # Fetch related products based on category (optional)
    # related_products = ProductModel.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        # 'related_products': related_products,  # For the "Related Products" section
    }
    return render(request, 'adoption_details.html', context)

def cat_view(request):
    cat_product = DonationModel.objects.filter(pet_category='cat') 
    return render(request, 'cat.html', {'cat_products': cat_product})

def dog_view(request):
    dog_product = DonationModel.objects.filter(pet_category='dog')  
    return render(request, 'dog.html', {'dog_products': dog_product})

def bird_view(request):
    bird_product = DonationModel.objects.filter(pet_category='bird')  
    return render(request, 'bird.html', {'bird_products': bird_product})

class DonationView(View):
    def get(self, request, pk=None):
        # Get the seller ID from the session
        seller_id = request.session.get('seller_id')
        if not seller_id:
            return render(request, 'error.html', {'error': 'No seller information found in session.'})

        # Fetch the logged-in seller
        try:
            seller = seller_list.objects.get(id=seller_id)
        except seller_list.DoesNotExist:
            return render(request, 'error.html', {'error': 'Invalid seller ID.'})

        # Filter products corresponding to the logged-in seller
        data = DonationModel.objects.filter(seller=seller)

        # Edit mode if pk is provided, otherwise add mode
        if pk:
            instance_edit = get_object_or_404(DonationModel, pk=pk, seller=seller)  # Ensure product belongs to seller
            forms = DonationForm(instance=instance_edit)
        else:
            forms = DonationForm()

        return render(request, 'add_donation.html', {'form': forms, 'data': data})

    def post(self, request, pk=None):
        # Get the seller ID from the session
        seller_id = request.session.get('seller_id')
        if not seller_id:
            return render(request, 'error.html', {'error': 'No seller information found in session.'})

        # Fetch the logged-in seller
        try:
            seller = seller_list.objects.get(id=seller_id)
        except seller_list.DoesNotExist:
            return render(request, 'error.html', {'error': 'Invalid seller ID.'})

        # Handle form submission for editing or adding
        if pk:
            instances = get_object_or_404(DonationModel, pk=pk, seller=seller)
            forms = DonationForm(request.POST, request.FILES, instance=instances)
        else:
            forms = DonationForm(request.POST, request.FILES)

        if forms.is_valid():
            product = forms.save(commit=False)
            product.seller = seller  # Assign the current seller to the product
            product.save()
            return redirect('adddonation')  # Redirect after success

        # Reload with errors if form is invalid
        data = DonationModel.objects.filter(seller=seller)
        return render(request, 'add_donation.html', {'form': forms, 'data': data})
    
class Deletedonationview(View):
    def get(self, request, pk):
        instances = get_object_or_404(DonationModel, pk=pk)
        instances.delete()
        return redirect('adddonation')



def adoption_request(request, donation_id):
    if not request.user.is_authenticated:
        return redirect('log_in')

    products = get_object_or_404(DonationModel, id=donation_id)
    
    if request.method == "POST":
        if AdoptionRequest.objects.filter(donation=products, user=request.user).exists():
            messages.error(request, "You have already requested adoption for this pet.")
            return redirect('request_history')  # Redirect to request history page

        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.user = request.user  
            adoption_request.donation = products  
            adoption_request.save()

            messages.success(request, "Your adoption request has been submitted successfully!")
            return redirect('request_history')  # Redirect to avoid duplicate submission

    else:
        form = AdoptionRequestForm(initial={
            'name': request.user.first_name,  
            'email': request.user.email,  
        })

    user_requests = AdoptionRequest.objects.filter(user=request.user)

    return render(request, 'adoption_request.html', {
        'form': form,
        'requests': user_requests,
        'donation': products
    })


def seller_adoption_requests(request):
    # Get the current logged-in seller
    seller_id = request.session.get('seller_id')

    seller = seller_list.objects.get(id=seller_id)
    status_filter = request.GET.get('status', '')  # Get selected status from the request

    # Get all seller's adoption requests
    adoption_requests = AdoptionRequest.objects.filter(donation__seller=seller)

    # Apply status filter if selected
    if status_filter:
        adoption_requests = adoption_requests.filter(status=status_filter)

    return render(request, 'seller_adoptionre.html', {
        'adoption_requests': adoption_requests,
        'status_filter': status_filter
    })


def request_history(request):
    requests = AdoptionRequest.objects.filter(user=request.user) 
    status_filter = request.GET.get('status', '')  # Get selected status from the request

    if status_filter:  # Apply status filter if selected
        requests = requests.filter(status=status_filter)
    return render(request, 'request_history.html', {'requests': requests, 'status_filter': 'status_filter'})

def update_order_statusre(request, request_id):
    # Fetch the order and ensure the seller is authorized
    requests = get_object_or_404(AdoptionRequest, id=request_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            requests.status = new_status
            requests.save()
            return redirect('seller_adoption_requests')  # Redirect to seller's orders page

    return render(request, 'update_statusre.html', {'requests': requests})

# cart

def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('log_in')

    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})



def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('log_in')
    
    product = ProductModel.objects.get(id=product_id)
    if product.product_status == 'Stock Out':
        messages.error(request, "This product is out of stock.")
        return redirect('product_details', product_id=product_id)
    # Check if the product is already in the cart
    if CartItem.objects.filter(product=product, user=request.user).exists():
        messages.error(request, "This product is already in your cart.")
        return redirect('view_cart')

    # If not, add the product to the cart
    cart_item = CartItem.objects.create(product=product, user=request.user, quantity=1)
    cart_item.save()
    messages.success(request, "Product added to cart successfully.")
    return redirect('view_cart')



def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')

# wishlist

def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('log_in')

    wishlist_items = wishlistitem.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items, })

def add_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect('log_in')
    
    product = ProductModel.objects.get(id=product_id)
    # Check if the product is already in the cart
    if wishlistitem.objects.filter(product=product, user=request.user).exists():
        messages.error(request, "This product is already in your wishlist.")
        return redirect('wishlist')

    # If not, add the product to the cart
    wishlist_items = wishlistitem.objects.create(product=product, user=request.user, quantity=1)
    wishlist_items.save()
    messages.success(request, "Product added to wishlist successfully.")
    return redirect('wishlist')

def remove_from_wishlist(request, item_id):
    wishlist_items = get_object_or_404(wishlistitem, id=item_id, user=request.user)
    wishlist_items.delete()
    return redirect('wishlist')

# address

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user 
            address.save()
            return redirect('address_list')  
    else:
        form = AddressForm()

    return render(request, 'add_address.html', {'form': form})

def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'address_list.html', {'addresses': addresses})

class EditAddressView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'edit_address.html'

    def get_success_url(self):
        return reverse('address_list')

    def get_object(self, queryset=None):
        # Ensure the user can only edit their own addresses
        return get_object_or_404(Address, id=self.kwargs['pk'], user=self.request.user)
    
class DeleteAddressView(DeleteView):
    model = Address
    template_name = 'delete_address.html'

    def get_success_url(self):
        return reverse('address_list')

    def get_object(self, queryset=None):
        # Ensure the user can only delete their own addresses
        return get_object_or_404(Address, id=self.kwargs['pk'], user=self.request.user)
    
# order place

def order_create(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    addresses = Address.objects.filter(user=user)
    for item in cart_items:
        if item.product.product_status == 'Stock Out':
            messages.error(request, "Product is out of stock remove it.")
            return redirect('view_cart')

    if request.method == 'POST':
        address_id = request.POST.get('address')
        address = Address.objects.get(id=address_id)

        seller = cart_items.first().product.seller 
        
        # Create an order
        order = Order.objects.create(user=user, address=address, total_price=total_price, seller=seller)
        
        # Add items to order and clear the cart
        for item in cart_items:
            product = item.product
            product.product_status = 'Stock Out'
            product.save()
            OrderItem.objects.create(
        order=order,
        product=item.product,  # Use the product field instead of item
        price=item.product.price,
        quantity=item.quantity,
        seller=seller
    )
        cart_items.delete()  # Clear the cart
        
        return redirect('order_success')  # Redirect to a success page
    
    return render(request, 'create.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'addresses': addresses,
    })
    


def order_success(request):
    return render(request, 'order_success.html')

def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    address = Address.objects.filter(user=request.user).first() 
    status_filter = request.GET.get('status', '')  # Get selected status from the request

    if status_filter:  # Apply status filter if selected
        orders = orders.filter(status=status_filter)
    return render(request, 'order_history.html', {'orders': orders, 'address': address, 'status_filter': 'status_filter'})


  
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status not in ['Cancelled', 'Refund Completed']:
        order.cancel_order()
        order_items = OrderItem.objects.filter(order=order)
        for order_item in order_items:
            product = order_item.product
            product.product_status = 'Stock In'
            product.save()
        messages.success(request, "Order canceled successfully!")
    else:
        messages.error(request, "This order cannot be canceled.")
    return redirect('order_history')



def seller_orders(request):

    seller_id = request.session.get('seller_id')

    seller = seller_list.objects.get(id=seller_id)
    status_filter = request.GET.get('status', '')  # Get selected status from the request

    orders = Order.objects.filter(seller=seller)  # Get all seller's orders

    if status_filter:  # Apply status filter if selected
        orders = orders.filter(status=status_filter)
  
    address = Order.objects.filter(seller=seller).select_related('user__address')


    return render(request, 'seller_order.html', {'orders': orders, 'status_filter': status_filter,'address': address})

def update_order_status(request, order_id):
    # Fetch the order and ensure the seller is authorized
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            order.status = new_status
            order.save()
            return redirect('seller_orders')  # Redirect to seller's orders page

    return render(request, 'update_status.html', {'order': order})






# import stripe
# from django.conf import settings
# from django.shortcuts import render
# from django.http import JsonResponse

# stripe.api_key = settings.STRIPE_SECRET_KEY

# def payment_view(request):
#     if request.method == "POST":
#         payment_method = request.POST.get("payment_method")
#         if payment_method == "credit_card":
#             card_number = request.POST.get("card_number")
#             expiry_date = request.POST.get("expiry_date")
#             cvv = request.POST.get("cvv")
            
#             try:
#                 # Create a payment intent
#                 intent = stripe.PaymentIntent.create(
#                     amount=1000,  # Amount in smallest currency unit (e.g., cents for USD)
#                     currency="usd",
#                     payment_method_types=["card"],
#                 )
#                 return JsonResponse({"client_secret": intent.client_secret})
#             except stripe.error.StripeError as e:
#                 return JsonResponse({"error": str(e)}, status=400)

#     return render(request, "create.html")













# class MyView(View):
#     def get(self, request, pk=None):
#         seller_id = request.session.get('seller_id')
#         seller = seller_list.objects.get(id=seller_id)
#         sproduct = product.objects.get(sellers=seller)
#         if pk is not None:  # Edit mode
#             instance_edited = get_object_or_404(ProductModel, pk=pk)
#             form = ProductListForm(instance=instance_edited)
#         else:  # Add mode
#             form = ProductListForm()

#         data = ProductModel.objects.all()  # Fetch all products to display
#         return render(request, 'add_product.html', {'form': form, 'data': data})

#     def post(self, request, pk=None):
#         if pk:  # Editing an existing product
#             instance = get_object_or_404(ProductModel, pk=pk)
#             form = ProductListForm(request.POST, request.FILES, instance=instance)
#         else:  # Adding a new product
#             form = ProductListForm(request.POST, request.FILES)

#         if form.is_valid():
#             product = form.save()
#             return redirect('addproduct')  # Redirect to the addproduct URL

#         # Reload with errors if form is invalid
#         data = ProductModel.objects.all()
#         return render(request, 'add_product.html', {'form': form, 'data': data})


    









# class MyView(View):
#     def get(self, request, pk=None):
#         # Get the seller ID from the session
#         seller_id = request.session.get('seller_id')
#         if not seller_id:
#             return render(request, 'error.html', {'error': 'No seller information found in session.'})

#         # Fetch the logged-in seller
#         try:
#             seller = seller_list.objects.get(id=seller_id)
#         except seller_list.DoesNotExist:
#             return render(request, 'error.html', {'error': 'Invalid seller ID.'})

#         # Filter products corresponding to the logged-in seller
#         data = ProductModel.objects.filter(seller=seller)

#         # Edit mode if pk is provided, otherwise add mode
#         if pk:
#             instance_edited = get_object_or_404(ProductModel, pk=pk, seller=seller)  # Ensure product belongs to seller
#             form = ProductListForm(instance=instance_edited)
#         else:
#             form = ProductListForm()

#         return render(request, 'add_product.html', {'form': form, 'data': data})

#     def post(self, request, pk=None):
#         # Get the seller ID from the session
#         seller_id = request.session.get('seller_id')
#         if not seller_id:
#             return render(request, 'error.html', {'error': 'No seller information found in session.'})

#         try:
#             seller = seller_list.objects.get(id=seller_id)
#         except seller_list.DoesNotExist:
#             return render(request, 'error.html', {'error': 'Invalid seller ID.'})

#         # Fetch all products for the seller
#         data = ProductModel.objects.filter(seller=seller)

#         # If editing an existing product
#         if pk:
#             instance = get_object_or_404(ProductModel, pk=pk, seller=seller)
#             form = ProductListForm(request.POST, request.FILES, instance=instance)
#         else:
#             form = ProductListForm(request.POST, request.FILES)

#         if form.is_valid():
#             product = form.save(commit=False)
#             product.seller = seller  # Set the seller
#             product.save()  # Save the product

#             # Handle saving multiple images if available
#             if 'images' in request.FILES:
#                 images = request.FILES.getlist('images')

#                 # Check the number of images selected
#                 if len(images) > 3:
#                     form.add_error('images', 'You can upload a maximum of 3 images.')
#                     return render(request, 'add_product.html', {'form': form, 'data': data})

#                 # Save each image to the ProductImage model
#                 for image in images:
#                     ProductModel.objects.create( images=image)

#             return redirect('addproduct')  # Redirect to the add product page or a success page

#         # If form is not valid, render the same page with the form errors
#         return render(request, 'add_product.html', {'form': form, 'data': data})






