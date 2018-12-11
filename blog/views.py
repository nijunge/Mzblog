from django.shortcuts import render
from .models import *
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import View
from django.db.models import Q
from django.shortcuts import redirect
# Create your views here.


def index(request):
    banners = Banner.objects.all()
    categorys = Category.objects.all()
    articles = Article.objects.order_by('-pub_time').all()
    top_articles = Article.objects.filter(top=True).all()
    friendlinks = FriendLink.objects.all()
    comments_all = Comment.objects.order_by('-create_time').all()
    count = Article.objects.count()
    #过滤
    articel_ids = []#装文章id
    comments = []#装评论id
    for comment in comments_all:
        if comment.article.id not in articel_ids:
            articel_ids.append(comment.article.id)
            comments.append(comment)

    return render(request,'index.html',locals())

def list(request,cid=-1,tid=-1):
    if cid != -1:
        try:
            categoey = Category.objects.get(pk=cid)
            articles = categoey.article_set.all()
        except Category.DoesNotExist:
            return render(request,'404.html')
    elif tid != -1:
        try:
            tag = Tags.objects.get(pk=tid)
            articles = tag.article_set.all()
        except Category.DoesNotExist:
            return render(request,'404.html')
    else:#列表点击
        articles = Article.objects.order_by('-pub_time').all()
    tags = Tags.objects.all()
    comments_all = Comment.objects.order_by('-create_time').all()
    #取页码
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    #分页
    p = Paginator(articles,per_page=1,request=request)
    # 取当前页的数据 返回一个Page对象
    article_list = p.page(page)

    # 过滤
    articel_ids = []  # 装文章id
    comments = []  # 装评论id
    for comment in comments_all:
        if comment.article.id not in articel_ids:
            articel_ids.append(comment.article.id)
            comments.append(comment)
    ctx = {
        'article_list': article_list,
        'tags': tags,
        'comments':comments
    }

    return render(request,'list.html',ctx)

def show(request,id):
    try:
        article = Article.objects.get(pk=id)
        article.read_num += 1
        article.save()
        #把文章所对应的标签取出来
        tags = article.tags.all()
        #去除标签所对应的文章
        recommends = []#相关推荐的文章
        for tag in tags:
            recommends.extend(tag.article_set.all())
        recommends = set(recommends)
        #评论
        comments_list = article.comment_set.order_by('-create_time').all()
        count = Article.objects.count()
    except Exception as e:
        return render(request,'404.html')
    #最新评论文章
    comments_all = Comment.objects.order_by('-create_time').all()

    # 过滤
    articel_ids = []  # 装文章id
    comments = []  # 装评论id
    for comment in comments_all:
        if comment.article.id not in articel_ids:
            articel_ids.append(comment.article.id)
            comments.append(comment)

    return render(request,'show.html',locals())

#实现搜素----基于类的视图
class Search(View):
    def get(self,request):
        kw = request.GET.get('kw')
        # Article.objects.filter(title__icontains=kw).filter(title__contains=kw)#并且关系
        search_list = Article.objects.filter(Q(title__icontains=kw)|Q(content__icontains=kw))#或者关系
        # 取页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 分页
        p = Paginator(search_list, per_page=1, request=request)
        # 取当前页的数据 返回一个Page对象
        article_list = p.page(page)
        tags = Tags.objects.all()
        comments_all = Comment.objects.order_by('-create_time').all()
        # 过滤
        articel_ids = []  # 装文章id
        comments = []  # 装评论id
        for comment in comments_all:
            if comment.article.id not in articel_ids:
                articel_ids.append(comment.article.id)
                comments.append(comment)
        return render(request,'list.html',locals())

    def post(self,request):
        pass

class CommentArticle(View):
    def post(self,request,id):
        comment_content = request.POST.get('comment_content')
        comment = Comment()
        comment.content = comment_content
        comment.article = Article.objects.get(id=id)
        comment.user = request.user
        comment.save()
        return redirect('/blog/' + id)