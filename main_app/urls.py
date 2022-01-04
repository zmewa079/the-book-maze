from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('books/', views.books_index, name='books_index'),
  path('books/<int:book_id>/', views.books_detail, name='books_detail'),
  path('books/create/', views.BookCreate.as_view(), name='books_create'),
  path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='books_delete'),
  path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='books_update'),
  path('books/<int:book_id>/add_photo/', views.add_photo, name='add_photo'),  
]
