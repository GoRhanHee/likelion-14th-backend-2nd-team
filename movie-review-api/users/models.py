from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    커스텀 User 모델
    Django 기본 User를 확장해서 추가 필드를 넣을 수 있어요.
    """
    nickname = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='닉네임'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='자기소개'
    )
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        verbose_name='프로필 이미지'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='가입일'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일'
    )

    class Meta:
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'

    def __str__(self):
        return self.username
    