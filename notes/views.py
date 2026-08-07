from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Note
from .forms import NoteForm


# 📌 Require login and assign author
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
        return redirect("note_list")
    return render(request, "notes/note_form.html", {"form": form})


@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, id=pk)
    form = NoteForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save()   
        return redirect("note_list")
    return render(request, "notes/note_form.html", {"form": form})


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, id=pk)
    if request.method == "POST":
        note.delete()
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