from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    """Form for creating and editing notes."""
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter note title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your note here...',
                'rows': 4
            })
        }
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NoteForm
from .models import Note

def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        # Form is invalid → re-render with errors
        return render(request, "stickynotes/add_note.html", {"form": form})

    form = NoteForm()
    return render(request, "stickynotes/add_note.html", {"form": form})


def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("home")
        # Invalid → show errors
        return render(request, "stickynotes/edit_note.html", {"form": form})

    form = NoteForm(instance=note)
    return render(request, "stickynotes/edit_note.html", {"form": form})
