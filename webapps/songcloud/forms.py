from django.forms import widgets
from django.contrib.auth.models import User
from django import forms
from songcloud.models import *
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length = 50, label='First Name',widget = widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'id': 'inputFirstName'}))
    last_name = forms.CharField(max_length = 50, label='Last Name', widget = widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'id': 'inputLastName'}))

    username = forms.CharField(max_length = 20, label='Username', widget = widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'id': 'inputUsername'}))
    email = forms.EmailField(max_length = 50, label='Email', widget = widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'id': 'inputEmail'}))
    password1 = forms.CharField(max_length = 200,
                                label='Password',
                                widget = widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'inputPassword'}))
    password2 = forms.CharField(max_length = 200,
                                label='Confirm password',
                                widget = widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'id': 'confirmPassword'}))


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegisterForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username

    #Customizes from validation for the email field
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already taken.")
        return email

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20, label='Username',
                               widget = widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'id': 'inputUsername'}))
    password = forms.CharField(max_length = 50,
                               label='Password',
                               widget = widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'inputPassword'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not User.objects.filter(username__exact=username):
            raise forms.ValidationError("This username does not exist. Please register first.")

        return username


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         exclude = ('owner', 'follow')
#         widgets = {'picture': forms.FileInput() }
#
#     first_name = forms.CharField(max_length=50, label='First Name',
#                                      widget=widgets.TextInput(attrs={'class': 'form-control'}))
#     last_name = forms.CharField(max_length=50, label='Last Name',
#                                     widget=widgets.TextInput(attrs={'class': 'form-control'}))
#     age = forms.CharField(max_length=50, label='Age',
#                                  widget=widgets.TextInput(attrs={'class': 'form-control'}))
#     bio = forms.CharField(max_length=420, label='Short bio',
#                                  widget=widgets.TextInput(attrs={'class': 'form-control'}))

class CustomPasswordResetForm(PasswordResetForm):

    def clean_email(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email):
            raise forms.ValidationError('invalid email !')
        return email


class RealRoomForm(forms.Form):
    room_name = forms.CharField(max_length=50)
    location = forms.CharField(max_length=400)
    playlist = forms.ChoiceField()
    introduction = forms.CharField(max_length=420)


class VirtualRoomForm(forms.Form):
    room_name = forms.CharField(max_length=50)
    style_tag = forms.ChoiceField()
    playlist_settings = forms.IntegerField()
    default_playlist = forms.ChoiceField()
    room_mode = forms.IntegerField()
    member_number = forms.IntegerField()
    introduction = forms.CharField(max_length=420)

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        exclude = ('owner','songs', 'date')
        widgets = {'photo': forms.FileInput(),
                   'description': forms.Textarea(attrs={'cols': 40, 'rows': 10}),}


class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    tag = forms.CharField(max_length=100)
    bio = forms.CharField(max_length=420)
    picture = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super(EditProfileForm, self).clean()
        return cleaned_data