from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post

# Create your views here.
class CommentNoticeListView(LoginRequiredMixin, ListView):
    context_object_name = 'notices'#上下文名称
    template_name = 'notice/list.html'#模板位置
    login_url = '/userprofile/login/'#路由重定向

    #未读通知的查询集
    def get_queryset(self):
        # print(self.request.user.notifications.unread())
        return self.request.user.notifications.unread()
class CommentNoticeUpdateView(View):
    def get(self,request):
        notice_id=request.GET.get('notice_id')
        if notice_id:
            post = Post.objects.get(id=request.GET.get('post_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(post)
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')
