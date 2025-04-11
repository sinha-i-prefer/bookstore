# bookstore_project/store/models.py

from django.db import models

class Book(models.Model):
    """
    Represents a book in the bookstore.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True) # Optional description
    price = models.DecimalField(max_digits=6, decimal_places=2)
    publication_date = models.DateField(blank=True, null=True) # Optional publication date
    # Consider adding an image field later:
    # image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    def __str__(self):
        """String representation of the Book model."""
        return f"{self.title} by {self.author}"

    class Meta:
        ordering = ['title'] # Default ordering for queries