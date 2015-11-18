#coding: utf-8
from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):

	class Meta:
		model = Category
		fields = ['name','description',]