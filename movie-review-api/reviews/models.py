from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):

    TAG_CHOICES = [
        ('mind_blown', '🤯 반전 대박'),
        ('popcorn', '🍿 가볍게 보기 좋음'),
        ('tear_jerk', '😭 눈물 버튼'),
        ('masterpiece', '✨ 인생 명작'),
        ('time_killer', '⏱️ 시간 순삭'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    story_rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    directing_rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    visual_rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    movie_tag = models.CharField(max_length=20, choices=TAG_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.nickname} - {self.movie.title}"