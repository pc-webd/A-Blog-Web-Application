from django.urls import path,include
from .views import *


app_name='blog'

urlpatterns=[
    path('',index,name='home'),
    path('login/',login,name='login'),
    path('logout/',logout_user,name='logout'),
    path('register/',register,name='register'),
    path('addblog/',addBlog,name='add-blog'),
    path('all-blogs/',allBlogs,name='all-blogs'),
    path('my-blogs/',myBlogs,name='my-blog'),
    path('update-blog/<slug>',updateBlog,name='updateBlog'),
    path('delete-blog/<id>',deleteBlog,name='deleteBlog'),
    path('blog/<slug>',blogDetail,name='detail'),
    path('contact/',contact,name='contact'),
    path('search/',get_search_data,name='search')
]