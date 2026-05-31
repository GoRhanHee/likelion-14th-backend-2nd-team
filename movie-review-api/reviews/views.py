from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action 
from rest_framework.response import Response  
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewListSerializer, ReviewDetailSerializer
from .permissions import IsOwnerOrReadOnly

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from movies.models import Movie

class ReviewViewSet(viewsets.ModelViewSet):
    """
    영화 리뷰 CRUD API
    
    - list: 전체 리뷰 목록 (페이지네이션)
    - create: 리뷰 작성 (로그인 필요)
    - retrieve: 리뷰 상세 조회
    - update/partial_update: 리뷰 수정 (작성자만)
    - destroy: 리뷰 삭제 (작성자만)
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['movie', 'user', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_serializer_class(self):
        # 👈 'best' 액션일 때도 목록용 시리얼라이저(ReviewListSerializer)를 쓰도록 추가합니다.
        if self.action in ['list', 'my', 'best']:  
            return ReviewListSerializer
        return ReviewDetailSerializer

    def get_queryset(self):
        return Review.objects.select_related('user', 'movie').annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my(self, request):
        """내가 작성한 리뷰 목록"""
        queryset = self.get_queryset().filter(user=request.user)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def best(self, request):
        """좋아요 많은 순으로 인기 리뷰 TOP 5 (로그인 불필요)"""
        queryset = self.get_queryset().order_by('-like_count')[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@login_required
def review_create(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
    return redirect('movie_detail', pk=movie_id)    