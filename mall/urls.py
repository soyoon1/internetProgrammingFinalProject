from django.urls import path
from . import views

urlpatterns = [ # IP주소/mall/
    path('',views.ItemList.as_view()),
    path('<int:pk>/', views.ItemDetail.as_view()),     # item 관련 pk
    path('<int:pk>/new_comment/', views.new_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),              # comment 관련 pk
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('create_item/', views.ItemCreate.as_view()),
    path('update_item/<int:pk>/', views.ItemUpdate.as_view()),
    path('category/<str:slug>/', views.category_page),         # 괄호 안에 첫 번째가 url이고 두번째가 처리할 함수 호출 # IP주소/blog/category/slug
    path('tag/<str:slug>/', views.tag_page),     # IP주소/blog/tag/slug
    path('manufacturer/<int:pk>/', views.manufacturer_page),
    path('search/<str:q>/',views.ItemSearch.as_view()),
    path('my_page/', views.my_page),  #마이페이지에 대한 내용.
    path('add_cart/<int:pk>/', views.add_cart),
    path('remove/<int:pk>/', views.cart_remove),
    path('full_remove/<int:pk>/', views.full_remove),

    #path('cart_detail/', views.cart_detail),

    #path('', views.index),  # IP주소/blog
    #path('<int:pk>/', views.single_post_page)
]