from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
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
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.in
    # Let the CreateView do its job as usual
    return super().form_valid(form)

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

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('books_index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)