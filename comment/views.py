from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from blog.models import Post
from .models import Comment
from notifications.signals import notify
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.

@login_required(login_url='/userprofile/login/')
def post_comment(request,post_id,parent_comment_id=None):
    post=get_object_or_404(Post,id=post_id)
    if request.method=='POST':
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.user=request.user
            #二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                new_comment.parent_id = parent_comment.get_root().id
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                #给其它用户发送通知
                if not parent_comment.user.is_superuser and not parent_comment.user==request.user:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了你',
                        target=post,
                        action_object=new_comment,
                    )
                return JsonResponse({"code":"200 OK","new_comment_id":new_comment.id})

            new_comment.save()
            #给管理员发通知
            if not request.user.is_superuser:
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='回复了你',
                    target=post,
                    action_object=new_comment,
                )
            #添加锚点
            redirect_url = post.get_absolute_url()+'#comment_elem_'+str(new_comment.id)
            return redirect(redirect_url)#去寻找model自己的get_absolute 方法
        else:
            return HttpResponse('表单内容有误')
    elif request.method == 'GET':
        comment_form = CommentForm()
        return render(request, 'comment/reply.html',{'comment_form':comment_form, 'post_id':post_id,
                                                     'parent_comment_id':parent_comment_id})
    else:
        return HttpResponse('发表评论仅支持POST/GET请求')

