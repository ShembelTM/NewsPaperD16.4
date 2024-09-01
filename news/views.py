from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from datetime import datetime
from .filters import PostFilter
from .forms import NewsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .models import Appointment
from django.views import View
from django.template.loader import render_to_string


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'appointment/make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        html_content = render_to_string(
            'appointment/appointment_created.html',
            {
                'appointment': appointment,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            body=appointment.message,
            from_email='filyanov.0_0.yura@mail.ru',
            to=['filyanov.yura@mail.ru'],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return redirect('appointment_created')


class PostsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class NewsFilter(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'search_news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',
                           'news.change_post',
                           'news.delete_post',)
    form_class = NewsForm
    model = Post
    template_name = 'edit_news.html'
    success_url = reverse_lazy('news_list')
    raise_exception = True

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'
        post.save()
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',
                           'news.change_post',
                           'news.delete_post',)
    form_class = NewsForm
    model = Post
    template_name = 'edit_news.html'
    success_url = reverse_lazy('news_list')
    raise_exception = True

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'article'
        post.save()
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.add_post',
                           'news.change_post',
                           'news.delete_post',)
    form_class = NewsForm
    model = Post
    template_name = 'edit_news.html'
    success_url = reverse_lazy('news_list')
    raise_exception = True


class NewsDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.add_post',
                           'news.change_post',
                           'news.delete_post',)
    form_class = NewsForm
    model = Post
    template_name = 'delete_news.html'
    success_url = reverse_lazy('news_list')
    raise_exception = True


class PostsDetail(DetailView):
    model = Post
    template_name = 'news1.html'
    context_object_name = 'news1'


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id = self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['is_subscriber'] = self.request.user in self.postCategory.subscribers.all()
        context['postCategory'] = self.postCategory
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    postCategory = Category.objects.get(id=pk)
    postCategory.subscribers.add(user)

    message = "Вы успешно подписались на рассылку новостей категории"

    return render(request, 'subscribe.html', {'postCategory': postCategory, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    postCategory = Category.objects.get(id=pk)
    postCategory.subscribers.remove(user)

    message = 'Вы отписались от рассылки'

    return render(request, 'subscribe.html', {'postCategory': postCategory, 'message': message})