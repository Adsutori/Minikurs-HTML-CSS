from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    slug        = models.SlugField(unique=True)
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon        = models.CharField(max_length=10, default='📖')
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_lessons(self):
        return self.lessons.filter(published=True).order_by('order')


class Lesson(models.Model):
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    slug        = models.SlugField()
    title       = models.CharField(max_length=200)
    description = models.CharField(max_length=300, blank=True)
    template    = models.CharField(max_length=200)
    order       = models.PositiveIntegerField(default=0)
    published   = models.BooleanField(default=True)
    duration    = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['order']
        unique_together = ['course', 'slug']

    def __str__(self):
        return f"{self.course.title} — {self.title}"


class Enrollment(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} → {self.course.title}"

    def progress_percent(self):
        total = self.course.get_lessons().count()
        if total == 0:
            return 0
        done = LessonProgress.objects.filter(
            user=self.user,
            lesson__course=self.course,
            completed=True
        ).count()
        return round((done / total) * 100)

    def completed_count(self):
        return LessonProgress.objects.filter(
            user=self.user,
            lesson__course=self.course,
            completed=True
        ).count()

    @property
    def is_completed(self):
        total = self.course.get_lessons().count()
        if total == 0:
            return False
        return self.completed_count() >= total


class LessonProgress(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson       = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    completed    = models.BooleanField(default=False)
    visited_at   = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'lesson']

    def __str__(self):
        return f"{self.user.username} — {self.lesson.title} ({'✅' if self.completed else '👁️'})"
