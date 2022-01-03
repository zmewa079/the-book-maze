from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
class Book: 
  def __init__(self, title, author, description):
    self.title = title
    self.author = author
    self.description = description


def home(request):
  return HttpResponse('<h1>Welcome to The Book Maze</h1>')

def about(request):
  return render(request, 'about.html')