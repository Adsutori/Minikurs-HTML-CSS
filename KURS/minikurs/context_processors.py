from .models import Enrollment

def user_enrollments(request):
    if request.user.is_authenticated:
        enrollments = Enrollment.objects.filter(
            user=request.user, active=True
        ).select_related('course').order_by('course__order')
        return {'user_enrollments': enrollments}
    return {'user_enrollments': []}
