from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DiscussionThread, Comment
from .forms import ThreadForm, CommentForm

def thread_list(request):
    threads = DiscussionThread.objects.order_by('-created_at')
    return render(request, 'community/thread_list.html', {'threads': threads})

@login_required
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = ThreadForm()
    return render(request, 'community/create_thread.html', {'form': form})

def thread_detail(request, pk):
    thread = get_object_or_404(DiscussionThread, pk=pk)
    comments = thread.comments.order_by('created_at')
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = request.user
            if request.user.role in ['officer', 'dept_admin', 'city_admin', 'super_admin']:
                comment.is_official_response = True
            comment.save()
            return redirect('thread_detail', pk=pk)
    else:
        form = CommentForm()
    
    return render(request, 'community/thread_detail.html', {'thread': thread, 'comments': comments, 'form': form})
