"""
Views for the Sticky Notes app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm


def home(request):
    """
    Display all sticky notes.
    """
    notes = Note.objects.all().order_by('-updated_at')
    return render(request, 'stickynotes/home.html', {'notes': notes})


def add_note(request):
    """
    Handle creation of a new note using the NoteForm.
    """
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NoteForm()
    return render(request, 'stickynotes/add_note.html', {'form': form})


def edit_note(request, note_id):
    """
    Edit an existing note using the NoteForm.
    """
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NoteForm(instance=note)
    return render(request, 'stickynotes/edit_note.html', {'form': form, 'note': note})


def delete_note(request, note_id):
    """
    Delete a selected note.
    """
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        note.delete()
        return redirect('home')
    return render(request, 'stickynotes/delete_note.html', {'note': note})
