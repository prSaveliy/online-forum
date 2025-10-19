from django import forms

from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': "Leave a comment...",
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'block w-full pl-3 pr-24 py-2 text-sm text-gray-400 border border-gray-600 rounded-lg bg-gray-800/50 placeholder-gray-400 transition-all duration-200 hover:shadow-md hover:shadow-gray-500/50 focus:ring-1 focus:ring-gray-500/50 focus:outline-none',
                'placeholder': "Leave a comment...",
                'rows': 4,
            })
        }

class SharePostForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'block w-full pl-3 pr-24 py-2 text-sm text-gray-400 border border-gray-600 rounded-lg bg-gray-800/50 placeholder-gray-400 transition-all duration-200 hover:shadow-md hover:shadow-gray-500/50 focus:ring-1 focus:ring-gray-500/50 focus:outline-none',
            'placeholder': "email@email.com",
        })
    )
    to = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'block w-full pl-3 pr-24 py-2 text-sm text-gray-400 border border-gray-600 rounded-lg bg-gray-800/50 placeholder-gray-400 transition-all duration-200 hover:shadow-md hover:shadow-gray-500/50 focus:ring-1 focus:ring-gray-500/50 focus:outline-none',
            'placeholder': "email@email.com",
        })
    )
    comment = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'block w-full mt-2 pl-3 pr-24 py-2 text-sm text-gray-400 border border-gray-600 rounded-lg bg-gray-800/50 placeholder-gray-400 transition-all duration-200 hover:shadow-md hover:shadow-gray-500/50 focus:ring-1 focus:ring-gray-500/50 focus:outline-none',
            'placeholder': "Leave a comment...",
            'rows': 6,
        })
    )

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'block w-full mt-2 pl-3 pr-24 py-2 text-sm text-gray-400 border border-gray-600 rounded-lg bg-gray-800/50 placeholder-gray-400 transition-all duration-200 hover:shadow-md hover:shadow-gray-500/50 focus:ring-1 focus:ring-gray-500/50 focus:outline-none',
                    'placeholder': "Title"
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'block w-full mt-2 pl-3 pr-24 py-2 text-sm text-gray-400 border border-gray-600 rounded-lg bg-gray-800/50 placeholder-gray-400 transition-all duration-200 hover:shadow-md hover:shadow-gray-500/50 focus:ring-1 focus:ring-gray-500/50 focus:outline-none',
                    'placeholder': "Content text",
                    'rows': 6
                }
            ),
            'tags': forms.TextInput(
                attrs={
                    'class': 'block w-full mt-2 pl-3 pr-24 py-2 text-sm text-gray-400 border border-gray-600 rounded-lg bg-gray-800/50 placeholder-gray-400 transition-all duration-200 hover:shadow-md hover:shadow-gray-500/50 focus:ring-1 focus:ring-gray-500/50 focus:outline-none',
                    'placeholder': "Add comma-separated tags (optional)"
                }
            ),
        }