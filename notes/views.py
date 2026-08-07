from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Note
from .forms import NoteForm


@login_required
def note_list(request):
    notes = Note.objects.all()
    context = {"notes": notes}
    return render(request, "notes/note_list.html", context)


@login_required
def note_create(request):
    form = NoteForm(request.POST or None)
    if form.is_valid():
        note = form.save(commit=False)
        note.author = request.user
        note.save()
        messages.success(request, "Note created successfully.")
        return redirect("note_list")
    return render(request, "notes/note_form.html", {"form": form})


@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, id=pk)
    if note.author != request.user and not request.user.is_superuser:
        messages.error(request, "You are not allowed to edit this note.")
        return redirect("note_list")
    form = NoteForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save()
        messages.success(request, "Note updated successfully.")
        return redirect("note_list")
    return render(request, "notes/note_form.html", {"form": form})


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, id=pk)
    if note.author != request.user and not request.user.is_superuser:
        messages.error(request, "You are not allowed to delete this note.")
        return redirect("note_list")
    if request.method == "POST":
        note.delete()
        messages.success(request, "Note deleted.")
        return redirect("note_list")
    return render(request, "notes/note_confirm_delete.html", {"note": note})


@login_required
def dashboard_note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            messages.success(request, "Note added successfully!")
        else:
            messages.error(request, "Please correct the errors below.")
        return redirect('dashboard')
    return redirect('dashboard')
