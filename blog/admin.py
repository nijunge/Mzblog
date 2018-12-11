from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Banner)
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(FriendLink)
admin.site.register(Comment)