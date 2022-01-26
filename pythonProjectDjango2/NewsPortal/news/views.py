from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import Post
from datetime import datetime
from .forms import NewsForm
from django.shortcuts import render
from .filters import NewsFilter, DateFilter, DateTimeFromToRangeFilter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator


# class PostsList(ListView):
#     model = Post
#     template_name = 'news1.html'
#     context_object_name = 'Posts'
#     queryset = Post.objects.order_by('-dateCreation')
#     # queryset = Post.objects.all().order_by('postCategory')
#
#     # def get_queryset(self):
#         # return Post.objects.filter(author=self.request.user).order_by('rating').reverse()
#         # return Post.objects.filter(author=self.request.postCategory).order_by('rating')
#
#         # return Post.objects.all().order_by('postCategory')[0]
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['time_now'] = datetime.utcnow()
#         context['value1'] = None
#         return context


class NewsList(ListView):
    model = Post
    template_name = 'news1.html'
    context_object_name = 'Posts'
    ordering = ['-dateCreation']
    paginate_by = 5

    def get_filter(self):
        return NewsFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        # context['date_filter'] = DateFilter(self.request.GET, queryset=self.get_queryset())

        # context['posts'] = Post.objects.all()
        # context['form'] = NewsForm()

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)
    #     return {
    #         **super().get_context_data(*args, **kwargs),
    #         'filter': self.get_filter(),
    #     }
    #


class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'Posts'
    ordering = ['-dateCreation']
    paginate_by = 5

    def get_filter(self):
        return NewsFilter(self.request.GET, queryset=super().get_queryset())
        # and DateFilter(self.request.GET, queryset=self.get_queryset())

        # def news_list(request):
        #     f = NewsFilter(request.GET, queryset=Post.objects.all())
        #     return render(request, 'news/news_search.html', {'filter': f})

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        # context['date_filter'] = DateFilter(self.request.GET, queryset=self.get_queryset())
        return context
        # context['posts'] = Post.objects.all()
        # context['form'] = NewsForm()


#
#     # def get_context_data(self, *args, **kwargs):
#     #     return {
#     #         **super().get_context_data(*args, **kwargs),
#     #         'filter': self.get_filter(),
# #     #     }
# class DateFilter(DateFilter):
#     model = Post
#     template_name = 'news2.html'
#
#     def get_filter(self):
#         return DateFilter(self.request.GET, queryset=super().get_queryset())


class NewsDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()


class NewsCreateView(CreateView):
    template_name = 'news_create.html'
    form_class = NewsForm


# дженерик для редактирования объекта
# @method_decorator(login_required, name='dispatch')


class NewsUpdateView(UpdateView):
    template_name = 'news_create.html'
    form_class = NewsForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class AddNews(PermissionRequiredMixin, NewsCreateView):
    permission_required = ('news.add_post',)


class ChangeNews(PermissionRequiredMixin, NewsUpdateView):
    permission_required = ('news.change_post',)


class DeleteNews(PermissionRequiredMixin, NewsDeleteView):
    permission_required = ('news.delete_post',)



# class PostsDetail(DetailView):
#     model = Post
#     template_name = 'sample_app/news2.html'
#     context_object_name = 'Post'
#     queryset = Post.objects.order_by('-dateCreation')
#
#
#    def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['time_now'] = datetime.utcnow()
#         context['value1'] = None
#         return context
