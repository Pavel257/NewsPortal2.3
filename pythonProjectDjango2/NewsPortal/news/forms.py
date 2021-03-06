from django.forms import ModelForm, BooleanField  # Импортируем true-false поле
from .models import Post


class NewsForm(ModelForm):
    check_box = BooleanField(label='Поставьте галочку')  # добавляем галочку, или же true-false поле

    class Meta:
        model = Post
        fields = ['author', 'categoryType', 'postCategory', 'title', 'text', 'check_box']