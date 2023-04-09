from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Item, Category, Tag, Manufacturer, Comment, Cart, CartItem
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

class ItemList(ListView):
    model = Item
    ordering = 'pk'
    paginate_by = 6 # 페이지네이션

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemList, self).get_context_data()
        context['categories'] = Category.objects.all()                                   # 카테고리부분
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['manufacturers'] = Manufacturer.objects.all()
        return context

class ItemSearch(ItemList): # ListView 상속, item_list, item_list.html
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        item_list = Item.objects.filter(
            Q(name__contains=q)
        ).distinct()
        return item_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search : {q} ({self.get_queryset().count()})'
        return context


class ItemDetail(DetailView):
    model = Item

    def get_context_data(self, **kwargs):     # 카테고리부분
        context = super(ItemDetail, self).get_context_data()    # 슈퍼 해당되는 내용 ItemDetail임을 명심하자
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['manufacturers'] = Manufacturer.objects.all()
        context['comment_form'] = CommentForm
        return context

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        item_list = Item.objects.filter(category=None)                     # 카테고리부분
    else:
        category = Category.objects.get(slug=slug)
        item_list = Item.objects.filter(category=category)
    return render(request, 'mall/item_list.html', {
        'category' : category,                                        # 템플릿이 사용하는 변수는 따옴표 안에 있음 :은 =과 같은 역할
        'item_list' : item_list,
        'categories' : Category.objects.all(),
        'no_category_item_count' : Item.objects.filter(category=None).count,
        'manufacturers' : Manufacturer.objects.all()
    })


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    item_list = tag.item_set.all()
    return render(request, 'mall/item_list.html', {
        'tag' : tag,
        'item_list': item_list,
        'categories': Category.objects.all(),
        'no_category_item_count': Item.objects.filter(category=None).count,
        'manufacturers': Manufacturer.objects.all()
    })

def manufacturer_page(request, pk): #, slug):
    manufacturer = Manufacturer.objects.get(pk=pk)
    item_list = Item.objects.filter(manufacturer=manufacturer)
    return render(request, 'mall/item_list.html', {
        'manufacturer': manufacturer,  # 템플릿이 사용하는 변수는 따옴표 안에 있음 :은 =과 같은 역할
        'item_list': item_list,
        'manufacturers': Manufacturer.objects.all(),
        'categories': Category.objects.all(),
        'no_category_item_count': Item.objects.filter(category=None).count,
    })

def my_page(request, total=0, counter=0, cart_items =None):
    comment_list = Comment.objects.filter(author=request.user)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.item.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'mall/my_page.html', {
        'manufacturers': Manufacturer.objects.all(),
        'categories': Category.objects.all(),
        'no_category_item_count': Item.objects.filter(category=None).count,
        'comment_list': comment_list,
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
    })

def new_comment(request, pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.item = item
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else: # GET
            return redirect(item.get_absolute_url())
    else:
        raise PermissionDenied

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    # CreateView, UpdateView, form을 사용하면
    # 템플릿 모델명_form : comment_form

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CommentUpdate, self).get_context_data()
        context['categories'] = Category.objects.all()                                   # 카테고리부분 사이드바 내용 위해 추가해줌.
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['manufacturers'] = Manufacturer.objects.all()
        return context


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    item = comment.item
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(item.get_absolute_url())
    else:
        PermissionDenied


class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['name','hook_text', 'description', 'image','price', 'manufacturer','category','countryOfOrigin']  # , 'tags'
    # 템플릿 item_form

    template_name = 'mall/item_update_form.html' # 클래스에서도 직접적으로 템플릿을 부를 수 있다.

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
            return super(ItemUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(ItemUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)  # 태그 기존에 있는 거 가져오든지 아님 새로 만드는 행동함.
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)  # 슬러그까지 추가해서 저장.
                    tag.save()
                self.object.tags.add(tag)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()                # string 배열들로 만들고 하나의 string으로 만듦.
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tags_str_list)      # 다 합쳐서 각각을 ;으로 구분하게 만듦.
        context['categories'] = Category.objects.all()                                   # 카테고리부분 사이드바 내용 위해 추가해줌.
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['manufacturers'] = Manufacturer.objects.all()
        return context

class ItemCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Item
    fields = ['name', 'hook_text', 'description', 'image', 'price', 'manufacturer', 'category', 'countryOfOrigin'] # , 'tags' 태그 구분 딜리미터 , ; 만 씀.
    # 템플릿 item_form
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            response = super(ItemCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str') # POST 우리가 쓰고 있는 모델명이 아니라 사용자가 request할 떄 URL없이 비교적 긴 데이터 전달할 때 쓰는 전달 방식
            if tags_str :
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',',';')
                tags_list = tags_str.split(';')
                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)       # 태그 기존에 있는 거 가져오든지 아님 새로 만드는 행동함.
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode = True)               # 슬러그까지 추가해서 저장.
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/mall/')

    # 템플릿 : 모델명_form.html
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemCreate, self).get_context_data()
        context['categories'] = Category.objects.all()                                   # 카테고리부분 사이드바 내용 위해 추가해줌.
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['manufacturers'] = Manufacturer.objects.all()
        return context

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, pk):
    item = Item.objects.get(id=pk)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(item=item, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            item = item,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
    return redirect('/mall/my_page/')

def cart_remove(request, pk):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    item = get_object_or_404(Item, id=pk)
    cart_item = CartItem.objects.get(item=item, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('/mall/my_page/')

def full_remove(request, pk):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    item = get_object_or_404(Item, id=pk)
    cart_item = CartItem.objects.get(item=item, cart=cart)
    cart_item.delete()
    return redirect('/mall/my_page/')

