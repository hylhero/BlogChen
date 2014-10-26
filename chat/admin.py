from django.contrib import admin
from chat.models import ChatModel


class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'time', 'msg', 'ip')
    search_field = ('ip',)

admin.site.register(ChatModel, ChatAdmin)
