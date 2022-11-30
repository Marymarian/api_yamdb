from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets

from reviews.models import Categories, Comments, Genres, Reviews, Titles, Users
# from .permissions import 
from .serializers import CommentSerializer, ReviewSerializer



class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = 

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get("title_id"))

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = 

    def get_queryset(self):
        review = get_object_or_404(Reviews, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Reviews, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
