from django import forms
from .models import ProductModel,DonationModel,AdoptionRequest,seller_list,Profile,sellerProfile,Address
from django.contrib.auth.models import User




class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['name', 'email', 'phone', 'address','message']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'message': forms.Textarea(attrs={'rows': 4}),
        }



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['building_name', 'area', 'city', 'district', 'PIN', 'default']

    # Optional: Customize widget styling if needed
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    building_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    area = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    PIN = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    default = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture'] 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = sellerProfile
        fields = ['sellerprofile_picture']

class sellerform(forms.ModelForm):  
    class Meta:
        model = seller_list
        fields = ['seller_username', 'seller_password', 'seller_email']
        labels = {
            'seller_username': '',
            'seller_email':'',
            'seller_password':'',
        }

        widgets = { 
            'seller_username': forms.TextInput(attrs={ 'class': 'form-control mb-4','placeholder': 'userName' }),
            'seller_email': forms.EmailInput(attrs={ 'class': 'form-control mb-4','placeholder': 'email'}),
            'seller_password': forms.PasswordInput(attrs={ 'class': 'form-control mb-4','placeholder': 'Phone' }),
        } 




from django import forms
from .models import ProductModel

class ProductListForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('cat', 'Cat'),
        ('dog', 'Dog'),
        ('bird', 'Bird'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select category'
        }),
        label="Category"
    )

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Gender"
    )

    is_vaccinated = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="Vaccinated"
    )

    class Meta:
        model = ProductModel
        fields = ('product_name', 'price', 'category', 'breed', 'age', 'gender', 'color', 'is_vaccinated', 'details', 'product_photos')

        widgets = {
            'details': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add product details here...',
                'rows': 3
            }),
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add product name here...'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add product price here...'
            }),
            'breed': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter pet breed...'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter pet age...'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter pet color...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_photos'].widget = forms.FileInput(attrs={
            'class': 'custom-file-input',
            'onchange': 'previewImage(event)',  
            'style': 'display: none;'  
        })


class DonationForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('cat', 'Cat'),
        ('dog', 'Dog'),
        ('bird', 'Bird'),
    ]

    pet_category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select category'
        }),
        label="Category"
    )

    class Meta:
        model = DonationModel
        fields = ('pet_details', 'pet_photos', 'pet_name', 'reason', 'pet_category', 'pet_breed', 'pet_age', 'pet_gender', 'pet_color', 'vaccinated')

        widgets = {
            'pet_details': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add product details here...',
                'rows': 3
            }),
            'pet_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add product name here...'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add reason here...',
                'rows': 3
            }),
            'pet_breed': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter pet breed...'
            }),
            'pet_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter pet age...'
            }),
            'pet_color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter pet color...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pet_photos'].widget = forms.FileInput(attrs={
            'class': 'custom-file-input',
            'onchange': 'previewImage(event)',  
              
        })




