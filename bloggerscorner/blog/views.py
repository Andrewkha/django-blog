from django.shortcuts import render
from django.views import generic

from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.shortcuts import get_object_or_404

# Create your views here.


def index(request):
    context = {
        'message': 'hello'
    }
    return render(request, 'index.html', context)


class PostListView(generic.ListView):
    model = Post
    paginate_by = 5
    template_name = 'blog/post/post_list.html'


class PostDetailView(generic.DeleteView):
    model = Post
    template_name = 'blog/post/post_detail.html'


class AuthorDetailView(generic.DeleteView):
    model = User
    template_name = 'blog/author/author_detail.html'


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['description']

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(CommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        #Add logged-in user as author of comment
        form.instance.author = self.request.user
        #Associate comment with blog based on passed id
        form.instance.blog=get_object_or_404(Post, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(CommentCreate, self).form_valid(form)

    def get_success_url(self):
        """
        After posting comment return to associated blog.
        """
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})