from django import forms


class BlogPostForm(forms.Form):
    """Form for blog post."""

    title = forms.CharField(label="Blog post title", max_length=100)
    content = forms.CharField(widget=forms.Textarea)


class BlogPostCommentForm(forms.Form):
    """Form for leaving a blog post comment."""

    content = forms.CharField(
        label="Comment",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Leave a comment",
                "class": "comment-form-content",
                "rows": 2,
            }
        ),
    )
