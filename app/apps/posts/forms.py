from django import forms

from app.apps.posts.models import PostModel


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ["title", "text", "status"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title"}
            ),
            "text": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Content"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Title",
            "text": "Content",
            "status": "Status",
        }

    def clean_status(self):
        status = self.cleaned_data.get("status")
        if status not in ["draft", "published"]:
            self.add_error("status", "Invalid status.")
        return status
