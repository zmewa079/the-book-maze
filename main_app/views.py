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
  return HttpResponse('<h1>Welcome to The Book Maze</h1>')

def about(request):
  return render(request, 'about.html')

def books_index(request):
  return render(request, 'books/index.html', { 'books': books })