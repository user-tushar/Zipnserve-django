from django import forms
from .models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={ 
        'placeholder': 'Enter Your Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Your Password'
    }))

    # that's how we can give css to any of Django:forms attributes.
    # we have to do just give all the forms input tags class's and id's and apply them on the django-forms tags .
    # confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
    #     'placeholder': 'Confirm Password',
    #     'class': 'font-control',
    # })) just like this  ... A class who have font-control name .. who is containing css propertis will applied on this confirm-password input tag also.

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
       
        #* Another Method to apply a same css class on all the input fields .
        
    def clean(self):
       cleaned_data = super(RegistrationForm, self).clean()
       password = cleaned_data.get('password')
       confirm_password = cleaned_data.get('confirm_password')

       if password != confirm_password:
           raise forms.ValidationError(
               "Password does not match!"
           )
       
    def __init__(self, *args, **kwargs):
        super (RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder']='Enter First Name ' # --> this will apply the css on this specific input field  on this form. in signup page .
        self.fields['last_name'].widget.attrs['placeholder']='Enter Last Name ' 
        self.fields['phone_number'].widget.attrs['placeholder']='Enter Phone Number ' 
        self.fields['email'].widget.attrs['placeholder']='Enter Email Address ' 

        # for field in self.fields:
        #     self.fields[field].widget.attrs['class']='form-control' # --> this will apply same form-control css class on all the input field present on this form with the help of loop.

    
       

class UserForm(forms.ModelForm):
    class Meta:
        model  = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs): # this is to give css properties to the my profile page form fields ..
        super (UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control' # --> this will apply same form-control css class on all the input field present on this form with the help of loop.



class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address1', 'address2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs): # this is to give css properties to the my profile page form fields ..
        super (UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control' # --> this will apply same form-control css class on all the input field present on this form with the help of loop.


    