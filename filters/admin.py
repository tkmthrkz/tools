from django.contrib import admin

from .models import Filter, Option

# Register your models here.
class OptionInline(admin.TabularInline):
    model = Option
    extra = 3 #予備の入力フォーム数

class FilterAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ('filter_name', 'filter_explain')
    list_filter = ['filter_name']
    search_fields = ['filter_name']

admin.site.register(Filter, FilterAdmin)