from django.contrib.auth import logout, models
from django.contrib.auth.models import User
from django.core import exceptions
from django.http import request
from django.views.decorators.cache import cache_page
from .models import BlogModel, Comment
from django.contrib import messages
from django.db.models import Q
from django import forms
from django.forms.fields import ImageField
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DeleteView,DetailView
from .forms import BlogForm
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache


CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)

@cache_page(CACHE_TTL)    #for faster loading
def index(request):
    blogs=BlogModel.objects.prefetch_related('user').order_by('-created_at')
    context={'blog':blogs}
    return render(request,'blog/index.html',context)

def login(request):
    return render(request,'blog/login.html')

def register(request):
    return render(request,'blog/register.html')

def addBlog(request):
    if not request.user.is_authenticated:
        return render(request,'blog/login.html')
    context={'form':BlogForm }
    if request.method == 'POST':
        try:
            form=BlogForm(request.POST)
            title=request.POST.get('title')
            image=request.FILES['image']

            if form.is_valid():
                content=form.cleaned_data['content']

            blog_obj=BlogModel.objects.create(
                user=request.user,
                title=title,
                image=image,
                content=content
            )
            messages.info(request, "You have been successfully added blog")
            return redirect('blog:add-blog')
        except Exception as e:
            print(e)


    return render(request,'blog/add_blog.html',context)

def blogDetail(request,slug):
    if request.method == 'GET':
        if cache.get(slug):
            print("data coming From Cache")
            blog_obj=cache.get(slug)
            blogs = BlogModel.objects.prefetch_related('user').order_by('-created_at')
            comments=Comment.objects.filter(blog__slug=slug)
            context={
                    'object':blog_obj,
                    'blogs':blogs,
                    'comm':comments
                }
        else:
            print("Data Coming from DB")
            blog_obj=get_object_or_404(BlogModel,slug=slug)
            blogs = BlogModel.objects.prefetch_related('user').order_by('-created_at')
            comments=Comment.objects.filter(blog__slug=slug)
            print(comments)
            context={
                'object':blog_obj,
                'blogs':blogs,
                'comm':comments
            }
            cache.set(slug,blog_obj)
        
        return render(request,'blog/see-blog.html',context)
           
    if request.method == 'POST':
        try:
            name=request.POST.get('name')
            email=request.POST.get('email')
            comment=request.POST.get('comment')

            user_comm=Comment.objects.create(
                blog=BlogModel.objects.get(id=request.POST.get('blog_id')),
                name=name,
                email=email,
                body=comment
            )
            blog_obj=BlogModel.objects.get(id=request.POST.get('blog_id'))
            blogs = BlogModel.objects.prefetch_related('user').order_by('-created_at')
            comments=Comment.objects.filter(blog__slug = slug )
            context={
                'object':blog_obj,
                'blogs':blogs,
                'comm':comments
            }
            messages.info(request, "Your Comment has been added")
            return render(request,'blog/see-blog.html',context)

        except Exception as e:
            print(e)

@cache_page(CACHE_TTL)
def allBlogs(request):
    blogs = BlogModel.objects.prefetch_related('user').order_by('-created_at')
    return render(request,'blog/allblogs.html',{'blogs':blogs})

def myBlogs(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect('blog:login')
        blogs=BlogModel.objects.filter(user=request.user).order_by('-created_at')
        return render(request,'blog/allblogs.html',{'blogs':blogs,'msg':'myblog'})

def updateBlog(request,slug):
    try:
        blog_obj=BlogModel.objects.get(slug=slug)
        if blog_obj.user != request.user:
            return redirect('blog:home')
        initial_dict= {'content':blog_obj.content}
        form=BlogForm(initial=initial_dict)
        context={
            'form':form,
            'blog':blog_obj
        }
        if request.method == 'POST':
            form=BlogForm(request.POST)
            title=request.POST.get('title')
            image=request.FILES['image']
            if form.is_valid():
                content=form.cleaned_data['content']
        
            blog_obj.title= title
            print(title)
            blog_obj.image= image
            blog_obj.content=content
            blog_obj.save()
            
            return render(request,'blog/allblogs.html',context)

        return render(request,'blog/update-blog.html',context)
                
    except Exception as e:
        print(e)

def deleteBlog(request,id):
    if not request.user.is_authenticated:
        return redirect('blog:login')
    try:
        blog_obj=BlogModel.objects.get(id=id)
        if blog_obj.user != request.user:
            return redirect('blog:home')
        blog_obj.delete()
        return redirect('blog:my-blog')
    except Exception as e:
        print(e)
    
def contact(request):
    return render(request,'blog/contact-us.html')

def logout_user(request):
    logout(request)
    return redirect('blog:login')


def get_blog(query=None):
    if query:
        print("DATA COMING FROM DB")
        queries=query.split(" ")
        try:
            for q in queries:
                blog=BlogModel.objects.filter(
                    Q(title__icontains=q) |
                    Q(content__icontains=q)
                ).distinct()
        except Exception as e:
            print(e)
    else:
       blogs = BlogModel.objects.prefetch_related('user').order_by('-created_at')
    
    return blog


def get_search_data(request):
    if request.method=='GET':
        query=request.GET.get('q')
        if cache.get(query):
            print("DATA COMING FROM CACHE")
            srch_obj = cache.get(query)
        else:
            if query:
                srch_obj=get_blog(query)
                cache.set(query,srch_obj)
            else:
                srch_obj=get_blog()
    
        return render(request,'blog/search.html',{'blogs':srch_obj,'q':query})
       



