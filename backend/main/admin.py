from django.contrib import admin
from .models import User as TelegramUser, FileId, Download, Keyword


admin.site.register(TelegramUser)
admin.site.register(FileId)
admin.site.register(Download)
admin.site.register(Keyword)