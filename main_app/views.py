from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from .models import Book, Photo
from main_app import models
import uuid
import boto3
# Create your views here.

class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

def books_index(request):
  books = Book.objects.all()
  return render(request, 'books/index.html', { 'books': books })

def books_detail(request, book_id):
  book = Book.objects.get(id=book_id)
  return render(request, 'books/detail.html', { 'book': book })

class BookCreate(CreateView):
  model = Book
  fields = ['title', 'author', 'description']
  success_url = '/books/'

class BookUpdate(UpdateView):
  model = Book
  fields = '__all__'
  success_url = '/books/'

class BookDelete(DeleteView):
  model = Book
  success_url = '/books/'

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'jan-bookcollector'

def add_photo(request, book_id):
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, book_id=book_id)
      book_photo = Photo.objects.filter(book_id=book_id)
      if book_photo.first():
        book_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('books_detail', book_id=book_id)