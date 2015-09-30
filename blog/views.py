from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required

# Create your views here.

"""
def post_list(request):
    posts = Post.objects.all  # .filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
"""


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class ListView(generic.ListView):
    # template_name = 'blog/post_list.html'
    # context_object_name = 'post_list'

    queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')


class DraftView(LoginRequiredMixin, generic.ListView):
    # template_name = 'blog/post_list.html'
    # context_object_name = 'post_list'

    queryset = Post.objects.filter(published_date__isnull=True).order_by('created_date')

    """
    def get_queryset(self):
        # Return the published posts.
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    """

"""
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
"""


class DetailView(generic.DetailView):
    model = Post


class PublishView(LoginRequiredMixin, generic.DetailView):
    model = Post

    def get_object(self):
        # Call the superclass
        object = super(PublishView, self).get_object()
        # Record the last accessed date
        object.published_date = timezone.now()
        object.save()
        # Return the object
        return object

"""
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # return redirect('blog.views.post_detail', pk=post.pk)
            return HttpResponseRedirect(reverse('blog:post_detail', args=(post.pk,)))
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
"""


class NewView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # return redirect('blog.views.post_detail', pk=post.pk)
            return HttpResponseRedirect(reverse('blog:post_detail', args=(post.pk,)))


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return HttpResponseRedirect(reverse('blog:post_detail', args=(post.pk,)))
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('blog:post_detail', args=(post.pk,)))
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail', pk=post_pk)
