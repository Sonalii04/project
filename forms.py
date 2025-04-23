
from django import forms
from django.forms import inlineformset_factory
from .models import Quiz, Question, Answer

class QuestionForm(forms.ModelForm):
    quiz = forms.ModelChoiceField(
        queryset=Quiz.objects.select_related('category'),
        label="Select Quiz (Subject)",
        help_text="Choose which quiz/subject this question belongs to."
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        label="Question Text"
    )

    class Meta:
        model = Question
        fields = ['quiz', 'text']

# Create an inline formset: 4 blank answer forms per question
AnswerFormSet = inlineformset_factory(
    Question,
    Answer,
    fields=('text', 'is_correct'),
    extra=4,
    widgets={
        'text': forms.TextInput(attrs={'class': 'form-control'}),
        'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'})
    },
    labels={
        'text': 'Answer Text',
        'is_correct': 'Correct?'
    }
)
from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter new subject name'
            })
        }
        labels = {
            'name': 'Subject Name'
        }
