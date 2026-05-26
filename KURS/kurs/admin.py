from django.contrib import admin
from .models import Enrollment, Progress, Certificate


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display  = ('user', 'course', 'enrolled_at', 'completed', 'completed_at')
    list_filter   = ('course', 'completed')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('enrolled_at',)


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display  = ('user', 'chapter', 'visited_at', 'completed')
    list_filter   = ('chapter', 'completed')
    search_fields = ('user__username',)
    readonly_fields = ('visited_at',)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display  = ('user', 'enrollment', 'issued_at', 'certificate_id')
    search_fields = ('user__username', 'certificate_id')
    readonly_fields = ('issued_at', 'certificate_id')
