from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action  
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer

class MovieViewSet(viewsets.ModelViewSet):
    """
    영화 정보 CRUD API
    
    - list: 전체 영화 목록 조회 (페이지네이션)
    - create: 영화 등록 (관리자 전용)
    - retrieve: 영화 상세 조회
    - update/partial_update: 영화 정보 수정 (관리자 전용)
    - destroy: 영화 삭제 (관리자 전용)
    """
    queryset = Movie.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'release_year']
    search_fields = ['title', 'director']
    ordering_fields = ['release_year', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        return MovieDetailSerializer

    def get_queryset(self):
        qs = Movie.objects.all()
        if self.action in ['list', 'popular']: 
            qs = qs.annotate(
                average_rating=Avg('reviews__rating'),
                review_count=Count('reviews')
            )
        return qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'popular']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """리뷰 많은 순으로 인기 영화 TOP 10"""
        movies = self.get_queryset().order_by('-review_count')[:10]
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)