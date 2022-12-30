from django.contrib import admin
from .models import Post, Group, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "group",)
    list_filter = ("pub_date", "group", )
    search_fields = ("author", )


class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", )
    search_fields = ("title", )


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "text")


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)