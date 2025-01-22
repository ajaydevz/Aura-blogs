from django.shortcuts import render,get_object_or_404
from .models import *
from django.shortcuts import render,redirect
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# Create your views here.

@never_cache
def Index(request):

    post = Blog.objects.filter(is_active=True).order_by('-id')
    main_post = Blog.objects.filter(is_active=True, Main_post=True).order_by('-id')[:1]
    recent = Blog.objects.filter(is_active=True,section='Recent').order_by('-id')[:5]
    category = Category.objects.all()
    popular = Blog.objects.filter(is_active=True,section='Popular').order_by('-id')[0:5]
    trend = Blog.objects.filter(is_active=True,section='Trending').order_by('-id')[:5]


    context = {
        'post':post,
        'main_post':main_post,
        'recent':recent,
        'category':category,
        'popular':popular,
        'trend':trend

    }


    return render(request,'index.html',context)

def BlogDetail(request,slug):

    # post = Blog.objects.order_by('-id')
    category = Category.objects.all()
    post = get_object_or_404(Blog, blog_slug=slug)
    comments = Comment.objects.filter(blog_id=post.id).order_by('-date')
    popular = Blog.objects.filter(is_active=True,section='Popular').order_by('-id')[0:5]

    context = {
        # 'posts':post,
        'category':category,
        'post':post,
        'comments':comments,
        'popular':popular

    }

    return render(request,'blog_detail.html',context)

def CategoryView(request,slug):

    cat = Category.objects.all()
    blog_cat = Category.objects.filter(slug=slug)

    context = {
        'cat':cat,
        'active_category':slug,
        'blog_cat':blog_cat
    }

    return render(request,'category.html',context)

@login_required(login_url='/login/')
def blog_create(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        section = request.POST.get('section')
        status = request.POST.get('status')
        main_post = request.POST.get('main_post') == 'on'

        category = Category.objects.get(id=category_id)

        blog = Blog(
            title=title,
            author=request.user.username, 
            author_email=request.user.email,
            author_image=request.user.profile_image,
            image=image,
            content=content,
            category=category,
            section=section,
            status=status,
            Main_post=main_post,
        )
        blog.save()  

        # Add a success message
        messages.success(request, 'Blog created successfully!')
        return redirect('blog_create')
    
    categories = Category.objects.all() 
    return render(request, 'user/createblog.html', {'categories': categories})

@login_required(login_url='/login/')
def category_manage(request):
    # Handle adding a new category
    if request.method == 'POST':
        category_name = request.POST.get('name')
        category_slug = slugify(category_name)

        # Save the new category
        category = Category(name=category_name, slug=category_slug)
        category.save()

        messages.success(request, f'Category "{category_name}" has been added!')
        return redirect('category_manage')  # Redirect to the same page to avoid resubmission on refresh

    # Get all categories to display
    categories = Category.objects.all()

    return render(request, 'user/category_manage.html', {'categories': categories})

@login_required(login_url='/login/')
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, f'Category "{category.name}" has been deleted!')
    return redirect('category_manage') 


@login_required(login_url='/login/')
def blog_list(request):
    blogs = Blog.objects.filter(author=request.user.username)
    return render(request,'user/bloglist.html',{'blogs':blogs})


def Blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk)  # Fetch the blog post by primary key
    categories = Category.objects.all()   # Fetch all categories for the dropdown

    if request.method == 'POST':
        blog.title = request.POST.get('title')
        if 'image' in request.FILES:
            blog.image = request.FILES['image']
        blog.content = request.POST.get('content')
        category_id = request.POST.get('category')
        blog.category = get_object_or_404(Category, id=category_id)
        blog.section = request.POST.get('section')
        blog.status = request.POST.get('status')
        blog.Main_post = request.POST.get('main_post') == 'on'
        blog.save()

        # Add a success message
        messages.success(request, 'Blog updated successfully!')
        return redirect('blog_create')

    return render(request, 'user/updateblog.html', {'blog': blog, 'categories': categories})


def Blog_delete(request,blog_id):
    blog = get_object_or_404(Blog,id=blog_id)

    if request.method == 'POST':
        blog.delete()
        messages.success(request,'succefully deleted')
        return redirect('blog_list')
    return render(request,'user/bloglist.html')


def add_comment(request,slug):

    if request.method == 'POST':
        post = get_object_or_404(Blog, blog_slug=slug)
        comment_text = request.POST.get('InputComment')
        parent_id = request.POST.get('parent_id')
        parent_comment = None

        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)

        Comment.objects.create(
            post=post,
            name=request.user.username,
            comment=comment_text,
            parent=parent_comment
        )
        return redirect('blog_detail', slug=post.blog_slug)
    
    return render(request,'user/blog_detail.html')
    



