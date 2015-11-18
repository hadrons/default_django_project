#coding: utf-8
from django.core.urlresolvers import reverse as r, reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView

from .models import Category
from .forms import CategoryForm


class CategoryConfig(object):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('categories:categories_list')

class CategoryListView(CategoryConfig, ListView):
    template_name = 'categories/list.html'
    context_object_name = 'categories'

class CategoryCreateView(CategoryConfig, CreateView):
    template_name = 'categories/category_create.html'
    
class CategoryUpdateView(CategoryConfig, UpdateView):
    template_name = 'categories/category_update.html'
