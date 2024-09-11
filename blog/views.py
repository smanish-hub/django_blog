from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# Create your views here.


def home(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',context)


class PostListView(ListView):
    model= Post
    template_name='blog/home.html' #<app>/<model_name>_<view_type>.html
    context_object_name='posts'    #this is used for passing the context in the template

    ordering='-date_posted'        #the '-' prefix before the column name by which ordering is to be done denotes DESC order 
    paginate_by=3                  #it means only two object of Post will be displayed per page

class UserPostListView(ListView):
    model= Post
    template_name='blog/user_blogs.html'
    context_object_name='posts'    
     
    paginate_by=3 

    #overwriting the classmethod get_queryset
    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content']

    #to save the prevent the intergity error we are setting the instance of author by overriding form_valid method

    def form_valid(self,form):
        form.instance.author=self.request.user #assigning the intance with current logged in user
        return super().form_valid(form)        #overiding the parent class with the new instace

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content']


    def form_valid(self,form):
        form.instance.author=self.request.user #assigning the intance with current logged in user
        return super().form_valid(form)        #overiding the parent class with the new instace

    #to check weather the user is same or not while updating the blog
    def test_func(self):
        post=self.get_object()  #it will get the object of the Post model

        if self.request.user ==  post.author:   #using that object we are verfying the user and author are same or not
            return True
        return False        #if not same 403 Forbidden error will be returned

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):

    model=Post
    success_url='/' #on click of yes it will take you to the home page
    
    #to check weather the user is same or not while updating the blog
    def test_func(self):
        post=self.get_object()  #it will get the object of the Post model

        if self.request.user ==  post.author:   #using that object we are verfying the user and author are same or not
            return True
        return False        #if not same 403 Forbidden error will be returned


def about(request):
    return render(request,'blog/about.html',{'title':'About'})
