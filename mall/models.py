from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os
import uuid

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)   # BEST, 시즌 한정, 한정 재고
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):  # IP주소/mall/tag/slug
        return f'/mall/tag/{self.slug}/'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 밀크, 다크, 화이트
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):                             # 카테고리부분
        return f'/mall/category/{self.slug}'

    class Meta:                                               # 카테고리부분
        verbose_name_plural = 'Categories'

class Manufacturer(models.Model):
    name = models.CharField(max_length=30)              # 허쉬, 기라델리...
    CEO = models.CharField(max_length=20)
    address = models.CharField(max_length=80)
    contact_number = models.CharField(max_length=20)
    logo_image = models.ImageField(upload_to='mall/images/', blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/mall/manufacturer/{self.pk}/'

class Item(models.Model):
    name = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    description = MarkdownxField()
    image = models.ImageField(upload_to='item/item_images/%Y/%m/%d/', blank=True)
    price = models.PositiveIntegerField()
    manufacturer = models.ForeignKey(Manufacturer, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
    countryOfOrigin = models.CharField(max_length=30)

    def __str__(self):
        return f'[{self.pk}] {self.name} - {self.price}'

    def get_absolute_url(self):
        return f'/mall/{self.pk}/'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'

    def get_description_markdown(self):
        return markdown(self.description)

class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # 왜 다대일 관계인지 다시 생각해보기.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.item.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'

class Cart(models.Model):
    cart_id= models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return str(self.cart_id)

class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    def sub_total(self):
        return self.item.price * self.quantity

    def __str__(self):
        return str(self.item)
