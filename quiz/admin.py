from django.contrib import admin

# Register your models here.

from .models import Quiz, Question, Choice


# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('category',)}
#     list_display = ['category', 'slug']


admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
