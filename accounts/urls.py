from django.urls import path
from  .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),  
    path('user-profile/', views.show_profile, name='profile'),  
    path('update-profile/', views.update_profile, name='update_profile'),
    path('forgot-password/', views.Forgot_password, name='forgot_password'),  


    path('dash-home',views.Dash_home,name='dash_home'),
    path('manage-blog',views.Manage_blog,name='manage_blogs'),
    path('manage-user/',views.Manage_users,name='manage_users'),
    path('block/<int:blog_id>/<str:action>/', views.Block_blog, name='block_blog'),
    path('block/<int:user_id>/', views.block_user, name="block_user"),
    path('admin-logout/',views.admin_Logout,name='admin_logout'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
