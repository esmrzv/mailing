from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog
from blog.services import get_blogs_from_cache


# Create your views here.
class BlogListView(ListView):
    model = Blog

    def get_object(self, queryset=None):
        super().get_object(queryset=queryset)
        return get_blogs_from_cache()


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object
