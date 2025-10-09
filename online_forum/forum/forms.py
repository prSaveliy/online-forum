from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']
        labels = {
            'name': "Fill in your name...",
            'body': "Leave a comment...",
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 '
                         'border border-gray-300 focus:ring-blue-500 rounded-lg focus:border-blue-500 '
                         'dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 '
                         'dark:text-white dark:focus:ring-blue-500',
                'placeholder': "Fill in your name...",
            }),
            'body': forms.Textarea(attrs={
                'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg '
                         'border border-gray-300 focus:ring-blue-500 focus:border-blue-500 '
                         'dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 '
                         'dark:text-white dark:focus:ring-blue-500',
                'placeholder': "Leave a comment...",
                'rows': 4,
            })
        }

class SharePostForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 '
                     'border border-gray-300 focus:ring-blue-500 rounded-lg     focus:border-blue-500 '
                     'dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 '
                     'dark:text-white dark:focus:ring-blue-500',
            'placeholder': "Fill in your name...",
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 '
                     'border border-gray-300 focus:ring-blue-500 rounded-lg     focus:border-blue-500 '
                     'dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 '
                     'dark:text-white dark:focus:ring-blue-500 mb-4',
            'placeholder': "youremail@gmail.com",
        })
    )
    to = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 '
                     'border border-gray-300 focus:ring-blue-500 rounded-lg     focus:border-blue-500 '
                     'dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 '
                     'dark:text-white dark:focus:ring-blue-500',
            'placeholder': "youremail@gmail.com",
        })
    )
    comment = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 '
                     'border border-gray-300 focus:ring-blue-500 rounded-lg     focus:border-blue-500 '
                     'dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 '
                     'dark:text-white dark:focus:ring-blue-500',
            'placeholder': "Write your comment here...",
            'rows': 6,
        })
    )