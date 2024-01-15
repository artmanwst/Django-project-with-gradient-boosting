from django.views.generic import ListView, TemplateView
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from .forms import WriterForm
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic import View
from django.shortcuts import render, get_object_or_404



class PostSearchResultsView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        object_list = Post.objects.filter(title__icontains=query)
        return render(request, self.template_name, {'object_list': object_list, 'query': query})


def get_post_by_title(request, title):
    post = get_object_or_404(Post, title=title)
    return render(request, 'post_detail.html', {'post': post})




class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})


class UserProfileView(DetailView):
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'user_data'  
    def get_object(self):
        return self.request.user


def redirect_to_user_profile(request):
    return redirect('user_profile')


def registration(request):
    if request.method =='POST':
        form = WriterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'user_profile.html')
    else:
        form = UserCreationForm()
    return render(request, 'your_template.html', {'form': form})


def login_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('user_profile')
    pass


from django.views.generic import ListView
from .models import Post


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = WriterForm()
        context['login_form'] = CustomAuthenticationForm()
        return context


class AboutPageView(TemplateView):
    template_name = 'about.html'


class ImputPageView(TemplateView):
    template_name = 'imput.html'
