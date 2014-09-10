from django.contrib import admin
from attractions.models import Attraction
from attractions.models import Review

class AttractionAdmin(admin.ModelAdmin):
    def __str__(self):              # __unicode__ on Python 2
        return self.name

    list_display = ('id','name','category')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id','review_title','attraction')


admin.site.register(Attraction,AttractionAdmin)
admin.site.register(Review,ReviewAdmin)