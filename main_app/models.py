from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
  title = models.CharField(max_length=100)
  author = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

def __str__(self):
    return self.name
    
  # Add this method
def get_absolute_url(self):
  return reverse('books_detail', kwargs={'book_id': self.id})

class Photo(models.Model):
  url = models.CharField(max_length=250)
  book = models.OneToOneField(Book, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for book_id: {self.book_id} @{self.url}"

