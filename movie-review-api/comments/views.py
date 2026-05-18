from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Comment, Like
from .serializers import CommentSerializer
from reviews.models import Review
from reviews.permissions import IsOwnerOrReadOnly

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = Comment.objects.select_related('user', 'review')
        review_id = self.request.query_params.get('review')
        if review_id:
            qs = qs.filter(review_id=review_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        like, created = Like.objects.get_or_create(user=request.user, review=review)
        if not created:
            like.delete()
            return Response({'liked': False, 'like_count': review.likes.count()}, status=status.HTTP_200_OK)
        return Response({'liked': True, 'like_count': review.likes.count()}, status=status.HTTP_201_CREATED)