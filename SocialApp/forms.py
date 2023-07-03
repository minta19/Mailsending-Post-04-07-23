from django import forms
from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Post,Profile

User=get_user_model()

class UserLoginForm(forms.Form):
    template_pack = 'bootstrap5'
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

    def clean(self,*args,**kwargs):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password') 
        
        if username and password:
            user=authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError('THIS USER DOES NOT EXIST')
            if not user.check_password(password):
                raise forms.ValidationError('THE PASSWORD IS INCORRECT')
        return super(UserLoginForm,self).clean(*args,**kwargs) 
    
class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField(label='Email Address')
    email2=forms.EmailField(label='confirm email')
    First_name=forms.CharField(label='First Name',max_length=255)
    Last_name=forms.CharField(label="Last Name",max_length=255)
        

    class Meta(UserCreationForm.Meta):
        model=User
        fields=['username','email','email2','First_name','Last_name']
    
    def clean(self,*args,**kwargs):
        email=self.cleaned_data.get('email')
        email2=self.cleaned_data.get('email2')

        if email != email2:
            raise forms.ValidationError('Emails must match')
        email_qs=User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email is already registered")
        return super(UserRegistrationForm,self).clean(*args,**kwargs)
    
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['First_name']
        user.last_name = self.cleaned_data['Last_name']
        
    
        if commit:
            user.save()
        return user

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['Picture']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dob', 'Gender', 'Bio', 'website', 'Place']

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'image_or_video']