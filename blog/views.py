import markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views import View

from .forms import PostForm
from .models import Post, Column
from comment.models import Comment
from comment.forms import CommentForm


# Create your views here.
# 视图函数
def post_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')
    post_list = Post.objects.all()
    if search:
        post_list = post_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search=''

    if column is not None and column.isdigit():
        post_list = post_list.filter(column=column)

    if tag and tag!='None':
        post_list = post_list.filter(tags__name__in=[tag])
    if order == 'total_views':
        post_list = post_list.order_by('-total_views')
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/list.html', {'posts': posts, 'order': order,
                                              'search':search, 'column':column,'tag':tag,})


def post_detail(request, id):
    # post = Post.objects.get(id=id)
    post = get_object_or_404(Post, id=id)
    post.total_views += 1
    post.save(update_fields=['total_views'])
    comments = Comment.objects.filter(post=id)
    comment_form = CommentForm()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    post.body = md.convert(post.body)
    return render(request, 'blog/detail.html',
                  {'post': post, 'comments': comments,
                   'comment_form':comment_form,'toc': md.toc})


# 用户登录检查
@login_required(login_url='/userprofile/login/')
def post_create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_post.column = Column.objects.get(id=request.POST['column'])
            new_post.save()
            post_form.save_m2m()
            return redirect('blog:post_list')
        else:
            HttpResponse('表单内容有误，请重新填写')
    else:
        post_form = PostForm()
        columns = Column.objects.all()
        return render(request, 'blog/create.html', context={'post_form': post_form, 'columns': columns})


@login_required(login_url='/userprofile/login/')
def post_safe_delete(request, post_id):
    user = Post.objects.get(id=post_id).author
    if request.user != user:
        return HttpResponse('你没有权限删除此用户的博客')
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.delete()
        return redirect('blog:post_list')
    else:
        return HttpResponse('仅允许POST请求')


@login_required(login_url='/userprofile/login/')
def post_modified(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user != post.author:
        return HttpResponse('你没有权限修改此用户的博客')
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            post.title = request.POST['title']
            post.body = request.POST['body']
            if request.POST['column'] != 'none':
                post.column = Column.objects.get(id=request.POST['column'])
            else:
                post.column = None
            if request.FILES.get('avatar'):
                post.avatar = request.FILES.get('avatar')
            post.tags.set(*request.POST.get('tags').split(','), clear=True)

            post.save()
            return redirect('blog:post_detail', post_id)
        else:
            return HttpResponse('表单内容有误，请重新填写！')
    else:
        post_form = PostForm()
        columns = Column.objects.all()
        return render(request, 'blog/modified.html', {'post': post, 'post_form': post_form,
                    'columns': columns, 'tags':','.join([x for x in post.tags.names()]),})

class IncreaseLikesViews(View):
    def post(self,request,*args,**kwargs):
        post= Post.objects.get(id=kwargs.get('id'))
        post.likes+=1
        post.save()
        return HttpResponse('success')