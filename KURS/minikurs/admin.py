from django.contrib import admin
from .models import Course, Lesson, Enrollment, LessonProgress

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display  = ['title', 'slug', 'order']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display  = ['title', 'course', 'slug', 'order', 'published', 'duration']
    list_filter   = ['course', 'published']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'enrolled_at', 'active']
    list_filter  = ['course', 'active']

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'completed', 'visited_at']
    list_filter  = ['completed', 'lesson__course']
