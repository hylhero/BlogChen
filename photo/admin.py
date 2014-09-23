from django.contrib import admin

from models import BingWallPaper, PhotoWall
# Register your models here.
class BingWPAdmin(admin.ModelAdmin):
    list_display        = ('title','imgdate','imgurl','desc1','query1','desc2','query2','desc3','query3','desc4','query4','qiniuimgurl')
    search_field        = ('imgdate',)
    list_per_page       = 10

class PhotoWallAdmin(admin.ModelAdmin):
    list_display        = ('imgtype','created','imgurl')
    search_field        = ('imgtype')
    list_per_page       = 10


admin.site.register(BingWallPaper, BingWPAdmin)
admin.site.register(PhotoWall, PhotoWallAdmin)