from django.contrib import admin
from AutoApp.models import Publisher,Author,Book

class AuthorAdmin(admin.ModelAdmin):
	list_display = ("first_name","last_name","email")
	search_fields = ("first_name","last_name")
	ordering = ("first_name",)
	fields = ("first_name",)

class BookAdmin(admin.ModelAdmin):
	list_display = ("title","publisher","publication_date")
	list_filter = ("publication_date",)
	date_hierarchy = "publication_date"
	filter_horizontal = ("authors",)

admin.site.register(Publisher)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Book,BookAdmin)
