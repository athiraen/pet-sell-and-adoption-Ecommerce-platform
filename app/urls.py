from django.urls import path
from .import views
from .views import MyView,Deleteview,EditAddressView,DeleteAddressView,DonationView,Deletedonationview


urlpatterns = [
    path('', views.index, name='index'),   
    path('selleraccount/', views.selleraccount, name='selleraccount'), 
    path('account/', views.account, name='account'), 
    path('sign_up', views.sign_up, name='sign_up'),
    path('log_in', views.log_in, name='log_in'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('myaccount/',views.myaccount,name='myaccount'),
    path('profile/edit/', views.edit_profile, name='edit_profile'), 
    path('sellerprofile/', views.sellerprofile_view, name='sellerprofile'),
    path('sellerprofile/edit/', views.edit_sellerprofile, name='edit_sellerprofile'), 
    path('product', views.product, name='product'),
    path('addproduct/', MyView.as_view(), name='addproduct'),
    path('edit/<int:pk>/', MyView.as_view(), name='edit_data'),
    path('delete/<int:pk>/', Deleteview.as_view(), name='delete_data'), 
    path('adddonation/', DonationView.as_view(), name='adddonation'),  
    path('edit_donation/<int:pk>/', DonationView.as_view(), name='edit_donation'),
    path('delete_donation/<int:pk>/', Deletedonationview.as_view(), name='delete_donation'), 
    path('adoption', views.adoption, name='adoption'),
    path('adoption/<int:product_id>/', views.adoption_details, name='adoption_details'),
    path('cat_view/', views.cat_view, name='cat_view'),
    path('dog_view/', views.dog_view, name='dog_view'),
    path('bird_view/', views.bird_view, name='bird_view'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('cat_products_view/', views.cat_products_view, name='cat_products_view'),
    path('dog_products_view/', views.dog_products_view, name='dog_products_view'),
    path('bird_products_view/', views.bird_products_view, name='bird_products_view'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('cart/', views.view_cart, name='view_cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/<int:product_id>', views.add_wishlist, name='add_wishlist'),
    path('remove_from_wishlist/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add/', views.add_address, name='add_address'),
    path('list/', views.address_list, name='address_list'),
    path('edit_address/<int:pk>/', EditAddressView.as_view(), name='edit_address'),
    path('delete_address/<int:pk>/', DeleteAddressView.as_view(), name='delete_address'),
    path('adoption_request/<int:donation_id>/', views.adoption_request, name='adoption_request'),
    path('create/', views.order_create, name='order_create'),
    path('order_success/', views.order_success, name='order_success'),
    path('order-history/', views.order_history, name='order_history'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('seller-orders/', views.seller_orders, name='seller_orders'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('search/', views.search_products, name='search_products'),
    path('seller-adoption-requests/', views.seller_adoption_requests, name='seller_adoption_requests'),
    path('request_history/', views.request_history, name='request_history'),
    path('update_order_statusre/<int:request_id>/', views.update_order_statusre, name="update_order_statusre"),
    


    
] 

