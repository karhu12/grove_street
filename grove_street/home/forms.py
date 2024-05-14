from django import forms


class BlogPostForm(forms.Form):
    """Form for blog post."""

    title = forms.CharField(label="Blog post title", max_length=100)
    content = forms.CharField(widget=forms.Textarea)
