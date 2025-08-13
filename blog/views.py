from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView

from blog.form import PostForm, CommentForm, ReplyForm
from blog.models import Post, Comment, Reply, Category


def index(request):
    blog_qs = Post.objects.all()
    blog_count = blog_qs.count()
    page = request.GET.get("page", "1")
    category_list = Category.objects.all()

    paginator = Paginator(blog_qs, 5)
    page_obj = paginator.get_page(page)

    context = {
        "blog_list": page_obj,
        "category_list": category_list,
        "blog_count": blog_count,
    }

    return render(request, "blog/index.html", context)


def category_view(request, category_name):
    path = request.path
    category = get_object_or_404(Category, category_name=category_name)
    category_posts = Post.objects.filter(category=category)
    category_list = Category.objects.all()
    blog_count = Post.objects.all().count()
    page = request.GET.get("page", "1")

    paginator = Paginator(category_posts, 5)
    page_obj = paginator.get_page(page)

    context = {
        "category_name": category_name,
        "blog_list": page_obj,
        "category_list": category_list,
        "path": path,
        "blog_count": blog_count,
    }

    return render(request, "blog/index.html", context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "crispy_form.html"
    extra_context = {"form_title": "새 블로그"}

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.author = self.request.user
        new_post.save()

        response = super().form_valid(form)
        messages.success(self.request, "새 블로그가 포스팅 되었습니다.")
        return redirect(self.get_success_url())


post_new = PostCreateView.as_view()


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        # 이전 글
        previous_post = (
            Post.objects.filter(created_at__lt=post.created_at)
            .order_by("-created_at")
            .first()
        )
        # 다음 글
        next_post = (
            Post.objects.filter(created_at__gt=post.created_at)
            .order_by("created_at")
            .first()
        )

        context["previous_post"] = previous_post
        context["next_post"] = next_post

        return context


post_detail = PostDetailView.as_view()


@login_required(login_url="accounts:login")
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        messages.error(request, "수정권한이 없습니다.")
        return redirect("blog:post_detail", pk=pk)

    if request.method == "GET":
        form = PostForm(instance=post)
    else:
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            saved_post = form.save()
            messages.success(request, "블로그가 수정 되었습니다.")
            return redirect(saved_post)

    return render(
        request,
        template_name="crispy_form.html",
        context={"form_title": "블로그 수정", "form": form},
    )


# CBV로 작성된 블로그 수정 view -> FBV로 변경 (수정권한 확인)
# class PostUpdateView(LoginRequiredMixin, UpdateView):
#     model = Post
#     form_class = PostForm
#     template_name = "crispy_form.html"
#     extra_context = {"form_title": "블로그 수정"}
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         qs = qs.filter(author=self.request.user)
#         return qs
#
#
# post_edit = PostUpdateView.as_view()


@login_required(login_url="accounts:login")
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        messages.error(request, "삭제권한이 없습니다.")
        return redirect("blog:post_detail", pk=pk)
    post.delete()
    messages.success(request, "블로그가 삭제 되었습니다.")
    return redirect("blog:index")


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        blog_pk = self.kwargs["blog_pk"]
        self.blog = get_object_or_404(Post, pk=blog_pk)  # noqa
        return super().dispatch(request, *args, **kwargs)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["request"] = self.request
    #     return kwargs

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.target = self.blog
        comment.save()

        response = super().form_valid(form)
        messages.success(self.request, "새 댓글이 작성 되었습니다.")
        return redirect(self.get_success_url() + "#end")

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.kwargs["blog_pk"]})


comment_new = CommentCreateView.as_view()


@login_required(login_url="accounts:login")
def comment_edit(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.user != comment.author:
        messages.error(request, "수정권한이 없습니다.")
        return redirect("blog:post_detail", pk=comment.target.pk)

    if request.method == "GET":
        form = CommentForm(instance=comment)
    else:
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.updated_at = timezone.now()
            comment.save()
            messages.success(request, "댓글이 수정 되었습니다.")
            return redirect(
                reverse("blog:post_detail", kwargs={"pk": comment.target.pk})
                + "#comment"
                + str(comment.pk)
            )

    return render(
        request,
        template_name="crispy_form.html",
        context={"form_title": "댓글 수정", "form": form},
    )


@login_required(login_url="accounts:login")
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.user != comment.author:
        messages.error(request, "삭제권한이 없습니다.")
        return redirect("blog:post_detail", pk=comment.target.pk)
    comment.delete()
    messages.success(request, "댓글이 삭제 되었습니다.")
    return redirect("blog:post_detail", pk=comment.target.pk)


class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = "crispy_form.html"
    extra_context = {"form_title": "새 대댓글"}

    def dispatch(self, request, *args, **kwargs):
        comment_pk = self.kwargs["comment_pk"]
        self.comment = get_object_or_404(Comment, pk=comment_pk)  # noqa
        # self.blog = self.comment.target
        return super().dispatch(request, *args, **kwargs)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["request"] = self.request
    #     return kwargs

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.author = self.request.user
        reply.target_comment = self.comment
        reply.save()

        response = super().form_valid(form)
        messages.success(self.request, "새 대댓글이 작성 되었습니다.")
        return redirect(self.get_success_url() + "#comment" + str(self.comment.pk))

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.comment.target.pk})


reply_new = ReplyCreateView.as_view()


@login_required(login_url="accounts:login")
def reply_edit(request, reply_pk):
    reply = get_object_or_404(Reply, pk=reply_pk)

    if request.user != reply.author:
        messages.error(request, "수정권한이 없습니다.")
        return redirect("blog:post_detail", pk=reply.target_comment.target.pk)

    if request.method == "GET":
        form = ReplyForm(instance=reply)
    else:
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.updated_at = timezone.now()
            reply.save()
            messages.success(request, "댓글이 수정 되었습니다.")
            return redirect(
                reverse(
                    "blog:post_detail", kwargs={"pk": reply.target_comment.target.pk}
                )
                + "#reply"
                + str(reply.pk)
            )

    return render(
        request,
        template_name="crispy_form.html",
        context={"form_title": "대댓글 수정", "form": form},
    )


@login_required(login_url="accounts:login")
def reply_delete(request, reply_pk):
    reply = get_object_or_404(Reply, pk=reply_pk)

    if request.user != reply.author:
        messages.error(request, "삭제권한이 없습니다.")
        return redirect("blog:post_detail", pk=reply.target_comment.target.pk)
    reply.delete()
    messages.success(request, "댓글이 삭제 되었습니다.")
    return redirect("blog:post_detail", pk=reply.target_comment.target.pk)


@login_required(login_url="accounts:login")
def post_like(request, pk):
    if request.user.is_authenticated:
        blog = get_object_or_404(Post, pk=pk)

        if blog.like_users.filter(pk=request.user.pk).exists():
            blog.like_users.remove(request.user)
        else:
            blog.like_users.add(request.user)
        return redirect("blog:post_detail", pk=pk)
    return redirect("accounts:login")


@login_required(login_url="accounts:login")
def comment_like(request, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)

        if comment.like_users.filter(pk=request.user.pk).exists():
            comment.like_users.remove(request.user)
        else:
            comment.like_users.add(request.user)
        return redirect(
            reverse("blog:post_detail", kwargs={"pk": comment.target.pk})
            + "#comment"
            + str(comment.pk)
        )
    return redirect("accounts:login")


@login_required(login_url="accounts:login")
def reply_like(request, reply_pk):
    if request.user.is_authenticated:
        reply = get_object_or_404(Reply, pk=reply_pk)

        if reply.like_users.filter(pk=request.user.pk).exists():
            reply.like_users.remove(request.user)
        else:
            reply.like_users.add(request.user)
        return redirect(
            reverse("blog:post_detail", kwargs={"pk": reply.target_comment.target.pk})
            + "#reply"
            + str(reply.pk)
        )
    return redirect("accounts:login")
