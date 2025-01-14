from django.contrib import admin
from courses.models import Course, UserCourse, Tag, Prerequesite, Learning, Video

class TagAdmin(admin.TabularInline):
    model = Tag

class LearningAdmin(admin.TabularInline):
    model = Learning

class PrerequesiteAdmin(admin.TabularInline):
    model = Prerequesite

class VideoAdmin(admin.TabularInline):
    model = Video

class CourseAdmin(admin.ModelAdmin):
    inlines = [TagAdmin, LearningAdmin, PrerequesiteAdmin, VideoAdmin]

admin.site.register(Course, CourseAdmin)
admin.site.register(Video)
admin.site.register(UserCourse)


