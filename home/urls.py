from django.urls import path
from  .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('home-page/',views.Index, name='home'),
    path('category/<str:slug>', views.CategoryView, name='category'),
    path('blog-detail/<str:slug>', views.BlogDetail, name='blog_detail'),

    path('create-blog', views.blog_create, name='blog_create'),
    path('categories/manage/', views.category_manage, name='category_manage'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),

    path('blog-list/', views.blog_list, name='blog_list'),
    path('blog-update/<int:pk>', views.Blog_update, name='blog_update'),
    path('blog-delete/<int:blog_id>', views.Blog_delete, name='blog_delete'),

    path('<slug:slug>/add-comment/', views.add_comment, name='add_comment'),



]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
