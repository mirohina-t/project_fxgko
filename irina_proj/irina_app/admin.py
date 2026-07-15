from django.contrib import admin
from irina_app.models import News, NewsImage, FederationInfo,  Starts, Treners, Sportsmens, StartsDetails, NewsImage, SportItem, SportGroups, StartsСategory


# admin.site.register(Post)
admin.site.register(News)
admin.site.register(NewsImage)
admin.site.register(FederationInfo)

admin.site.register(Starts)
admin.site.register(Treners)
admin.site.register(Sportsmens)
admin.site.register(SportItem)
admin.site.register(SportGroups)
admin.site.register(StartsDetails)
admin.site.register(StartsСategory)



# class NewsImageInline(admin.TabularInline):
#     model = NewsImage
#     extra = 3

# @admin.register(News)
# class NewsAdmin(admin.ModelAdmin):
#     inlines = [NewsImageInline]
#     list_display = ['title', 'author', 'publish_date']