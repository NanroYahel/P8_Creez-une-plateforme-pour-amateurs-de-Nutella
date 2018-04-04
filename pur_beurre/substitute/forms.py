from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label="Nom d'utilisateur", max_length=30)
	password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class SignInForm(forms.Form):
	username = forms.CharField(label="Nom d'utilisateur", max_length=30)
	email = forms.EmailField(label="E-mail")	
	password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
	confirm_password = forms.CharField(label="Confirmer mot de passe", widget=forms.PasswordInput)