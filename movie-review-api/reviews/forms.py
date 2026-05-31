from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating', 'directing_rating', 'story_rating', 'visual_rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '리뷰 제목'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '내용을 입력하세요'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'directing_rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'story_rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'visual_rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }