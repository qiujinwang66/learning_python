from django.http import HttpResponse
from django.shortcuts import render
from navigation.models import Category
from navigation.models import Page

def index(request):
    # 查询数据库，获取目前存储的所有分类
    # 按点赞次数倒序排列分类
    # 获取前 5 个分类（如果分类数少于 5 个，那就获取全部）
    # 把分类列表放入 context_dict 字典
    # 稍后传给模板引擎
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    # 渲染响应，发给客户端
    return render(request, 'navigation/index.html', context_dict)


def about(request):
    return HttpResponse("龙腾测试！！！ <a href='/navigation/'>首页</a>")

def show_category(request, category_name_slug):
    # 创建上下文字典，稍后传给模板渲染引擎
    context_dict = {}
    try:
        # 能通过传入的分类别名找到对应的分类吗？
        # 如果找不到， .get() 方法抛出 DoesNotExist 异常
        # 因此 .get() 方法返回一个模型实例或抛出异常
        category = Category.objects.get(slug=category_name_slug)
        # 检索关联的所有网页
        # 注意， filter() 返回一个网页对象列表或空列表
        pages = Page.objects.filter(category=category)
        # 把得到的列表赋值给模板上下文中名为 pages 的键
        context_dict['pages'] = pages
        # 也把从数据库中获取的 category 对象添加到上下文字典中
        # 我们将在模板中通过这个变量确认分类是否存在
        context_dict['category'] = category
    except Category.DoesNotExist:
        # 没找到指定的分类时执行这里
        # 什么也不做
        # 模板会显示消息，指明分类不存在
        context_dict['category'] = None
        context_dict['pages'] = None
    # 渲染响应，返回给客户端
    return render(request, 'navigation/category.html', context_dict)
