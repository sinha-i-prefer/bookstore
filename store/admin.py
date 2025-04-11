# bookstore_project/store/admin.py

# bookstore_project/store/admin.py

from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Book model.
    """
    # These options customize how the Book model appears in the admin list view
    list_display = ('title', 'author', 'price', 'publication_date') 
    
    # Adds filters to the right sidebar in the admin list view
    list_filter = ('author', 'publication_date') 
    
    # Adds a search bar at the top of the admin list view
    search_fields = ('title', 'author', 'description') 

# REMOVED the following line as it's redundant with the @admin.register decorator:
# admin.site.register(Book)