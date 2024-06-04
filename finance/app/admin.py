from django.contrib import admin
from app.models import Accounts, Comments


class DatabaseEntryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'date', 'no_of_pages')  # Display these fields in the admin list view

class Comment(admin.ModelAdmin):
    list_display = ('name', 'mobil', 'comment')


admin.site.register(Accounts, DatabaseEntryAdmin)
admin.site.register(Comments, Comment)


