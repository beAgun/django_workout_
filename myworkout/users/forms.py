from datetime import datetime
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин или E-mail',
                               widget=forms.TextInput(attrs={'id': "floatingInput",
                                                             'placeholder': "name@example.com",
                                                             'class': 'form-control',
                                                             'type': 'text'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'type': 'password'}))

    #username.label_classes = ("floatingInput",)
    # class Meta:
    #     model = get_user_model()
    #     fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'id': "floatingInput",
                                                             'placeholder': "login",
                                                             'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'type': "password",
                                                                  'id': "floatingPassword",
                                                                  'placeholder': "Password",
                                                                  'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'id': "floatingInput",
                                             'placeholder': "name@example.com",
                                             'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password1'] != cd['password2']:
    #         raise ValidationError('no match')
    #     return cd['password1']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким E-mail уже существует.')
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин', disabled=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='E-mail', disabled=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    this_year = datetime.today().year
    date_birth = forms.DateField(label='Дата рождения',
                                 widget=forms.SelectDateWidget(
                                     years=tuple(range(this_year-100, this_year-5)),
                                    attrs={'class': 'form-control',
                                           'style': 'width: auto; display: inline;'})
                                 )


    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'photo', 'date_birth', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'photo': 'Фото',
            'date_birth': 'Дата рождения',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'type': 'file', 'class': 'form-control', 'id': "formFile"}),
            'date_birth': forms.TextInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                                                 'class': 'form-control'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Новый пароль',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Подтверждение пароля',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))