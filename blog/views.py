from django.shortcuts import render, HttpResponse, redirect
from .models import Post, BlogComment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.templatetags import extras
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
BLOGPOST_PER_PAGE = 2

def blogHome(request):
    allpost = Post.objects.all()

    # Pagination
    page = request.GET.get('page', 1)
    blog_post_paginator = Paginator(allpost, BLOGPOST_PER_PAGE)
    try:
        blog_posts = blog_post_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_post_paginator.page(BLOGPOST_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_post_paginator.page(blog_post_paginator.num_pages)
    context = {'allpost':blog_posts}
    return render(request, 'blog/blogHome.html',context)

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    username = request.user
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    
    context = {'post':post, 'comments':comments, 'username':username, 'replyDict':replyDict}
    return render(request, 'blog/blogPost.html',context)

@login_required()
def addPost(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        author = request.user
        slug = title.replace(" ", "") + "-blog"
        # Check errorneous inputs  
        posts = Post.objects.all()
        for post in posts:
            if title == post.title:
                 messages.error(request,"Title must be unique.")
                 return render(request,"blog/addPost.html")

        mypost = Post(title=title, content=content, author=author, slug=slug)
        mypost.save()
        messages.success(request, "Your blog has been posted successfully.")
        return redirect("/")
    else:
        return render(request,"blog/addPost.html")

@login_required()
def editPost(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        sno = request.POST['number']
        post = Post.objects.get(sno=sno)
        if post.author == request.user:
            mypost = Post.objects.filter(sno=sno).update(title=title, content=content)
            messages.success(request, "Your blog has been updated successfully.")
            return redirect(f"/blog/{post.slug}")
        else:
            messages.error(request, "You are not authorize to edit this blog.")
            redirect(f"/blog/{post.slug}")
    return render(request,'blog/editBlog.html',{'post':post})

@login_required()
def deletePost(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    messages.success(request,"Your post has been deleted successfully.")
    return redirect("blogHome")

# API to post comment
@login_required()
def postComment(request):
    if request.method == 'POST':
        comment = request.POST["comment"]
        user = request.user
        postsno = request.POST["postsno"]
        parentSno = request.POST["parentSno"]
        post = Post.objects.get(sno=postsno)
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully.")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully.")


    return redirect(f"/blog/{post.slug}")

@login_required()
def deleteComment(request, pk):
    comment = BlogComment.objects.get(sno=pk)
    post = Post.objects.get(sno=comment.post.sno)
    comment.delete()
    messages.success(request,"Your Comment has been deleted successfully.")
    return redirect(f"/blog/{post.slug}")

@login_required()
def editComment(request):
    if request.method == "POST":
        comment = request.POST['comment']
        commentsno = request.POST['commentsno']
        postsno = request.POST['postsno']
        post = Post.objects.get(sno=postsno)
        usercomment = BlogComment.objects.get(sno=commentsno)
        if usercomment.user == request.user:
            mycomment = BlogComment.objects.filter(sno=commentsno).update(comment=comment)
            messages.success(request, "Your comment has been updated successfully.")
            return redirect(f"/blog/{post.slug}")
        else:
            messages.error(request, "You are not authorize to edit this comment.")
            return redirect(f"/blog/{post.slug}")

        return redirect(f"/blog/{post.slug}")