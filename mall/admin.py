from django.contrib import admin
from .models import Item, Category, Tag, Manufacturer, Comment, Cart, CartItem
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.

admin.site.register(Item, MarkdownxModelAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Category,CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Tag,TagAdmin)

#class ManufacturerAdmin(admin.ModelAdmin):
 #   prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Manufacturer)#, ManufacturerAdmin)

admin.site.register(Comment)

admin.site.register(Cart)

admin.site.register(CartItem)



