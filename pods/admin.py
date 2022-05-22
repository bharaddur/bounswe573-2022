from django.contrib import admin
#from .models import Subject, Pod, Module
from .models import Pod, Module, Discussion, Comment

#@admin.register(Subject)
#class SubjectAdmin(admin.ModelAdmin):
#    list_display = ['title', 'slug']
#    prepopulated_fields = {'slug': ('title',)}
class ModuleInline(admin.StackedInline):
    model = Module

class DiscussionInline(admin.TabularInline):
    model = Discussion

class CommentInline(admin.TabularInline):
    model = Discussion

admin.site.register(Comment)

@admin.register(Pod)
class PodAdmin(admin.ModelAdmin):

    list_display = ['title', 'created', 'get_tags']

    def get_tags(self, obj):
        return ", ".join(o for o in obj.tags.names())

    list_filter = ['created']
    
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline, DiscussionInline]