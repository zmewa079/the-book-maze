from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
class Book: 
  def __init__(self, title, author, description):
    self.title = title
    self.author = author
    self.description = description

books = [
  Book('The Kite Runner', 'Khaled Hoesseini', 'A story about two boys and how a certain event during their childhood shape the different men they grow up to be.'),
  Book('Pride and Prejudice', 'Jane Austen', 'novel')
]

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def books_index(request):
  books = Book.objects.all()
  return render(request, 'books/index.html', { 'books': books })

def books_detail(request, cat_id):
  book = Book.objects.get(id=book_id)
  return render(request, 'books/detail.html', { 'book': book })