from .models import Enrollment

def user_enrollments(request):
    """Dostarcza zapisane kursy usera do każdego szablonu."""
    if request.user.is_authenticated:
        enrollments = Enrollment.objects.filter(
            user=request.user, active=True
        ).select_related('course')
        return {'user_enrollments': enrollments}
    return {'user_enrollments': []}
