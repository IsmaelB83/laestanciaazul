# coding=utf-8
# Python imports
# Django imports
from django import forms
# Third party app imports
# Local app imports
from .models import UserProfile


class LoginForm(forms.ModelForm):
	user = forms.CharField(
		label='Username',
		required=True,
		max_length=20,
		widget=forms.TextInput(attrs={'placeholder': 'username',
		                              'autocomplete': 'off',
									  'class': 'form-control'}))
	password = forms.CharField(
		label='Password',
		required=True,
		max_length=100,
		widget=forms.PasswordInput(attrs={'placeholder': 'Password',
		                                  'autocomplete': 'off',
										  'class': 'form-control'}))
	

class MailForm(forms.Form):
	mail_name = forms.CharField(
		label='Nombre',
		required=True,
		max_length=20,
		widget=forms.TextInput(attrs={'placeholder': 'Nombre...',
		                              'autocomplete': 'on',
		                              'class': 'form-control input-lg _contact_input'})
	)
	mail_from = forms.EmailField(
		label='Mail',
		required=True,
		max_length=50,
		widget=forms.TextInput(attrs={'placeholder': 'E-Mail...',
		                              'autocomplete': 'on',
		                              'class': 'form-control input-lg _contact_input'})
	)
	mail_subj = forms.CharField(
		label='Asunto',
		required=True,
		max_length=50,
		widget=forms.TextInput(attrs={'placeholder': 'Asunto...',
		                              'autocomplete': 'on',
		                              'class': 'form-control input-lg _contact_input'})
	)
	mail_mess = forms.CharField(
		label='Mensaje',
		required=True,
		max_length=200,
		widget=forms.TextInput(attrs={'placeholder': 'Mensaje...',
		                              'autocomplete': 'off',
		                              'class': 'form-control input-lg _contact_input',
		                              'style': 'height:182px; resize:none;'})
	)


class ProfileForm(forms.ModelForm):
	user_id = forms.CharField(
		widget=forms.TextInput(attrs={
			'readonly': 'readonly',
			'placeholder': 'tu usuario...',
			'class': 'form-control'}),
		max_length=150
	)
	first_name = forms.CharField(
		widget=forms.TextInput(attrs={
			'placeholder': 'tu nombre...',
			'class': 'form-control'}),
			max_length=30)
	last_name = forms.CharField(
		widget=forms.TextInput(attrs={
			'placeholder': 'tu apellido...',
			'class': 'form-control'}),
		max_length=30,
		required=False
	)
	email = forms.EmailField(
		widget=forms.TextInput(attrs={
			'placeholder': 'tu e-mail...',
			'class': 'form-control'}),
		max_length=50,
	)
	country = forms.CharField(
		widget=forms.TextInput(attrs={
			'placeholder': 'país donde vives...',
			'class': 'form-control'}),
		max_length=20,
		required=False
	)
	location = forms.CharField(
		widget=forms.TextInput(attrs={
			'placeholder': 'ciudad donde vives...',
			'class': 'form-control'}),
		max_length=30,
		required=False
	)
	description = forms.CharField(
		widget=forms.TextInput(attrs={
			'placeholder': 'una frase que te describa...',
			'class': 'form-control'}),
		max_length=100,
		required=True
	)
	image = forms.ImageField(
		required=False
	)
	
	class Meta:
		model = UserProfile
		fields = ('user_id', 'first_name', 'last_name', 'email', 'country', 'location',
		          'description', 'introduction', 'image')
	
	# def clean(self):
	#     cleaned_data = super(ProfileForm, self).clean()
	#     description = cleaned_data.get('description')
	#     if not description:
	#         raise forms.ValidationError('You have a description!')
