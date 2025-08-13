from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from memo.form import MemoForm
from memo.models import Memo


def staff_required(func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_staff:
            if request.META.get("HTTP_REFERER"):
                messages.error(request, "Staff이상 사용자만 접근이 가능합니다.")
                return redirect(request.META["HTTP_REFERER"])
            else:
                messages.error(request, "Staff이상 사용자만 접근이 가능합니다.")
                return redirect(reverse_lazy("core:root"))
        return func(request, *args, **kwargs)

    return wrap


@staff_required
def index(request):
    memo_qs = Memo.objects.all()
    memo_on_going = memo_qs.filter(status=True)
    memo_finished = memo_qs.filter(status=False)
    page = request.GET.get("page", "1")

    paginator = Paginator(memo_qs, 6)
    page_obj = paginator.get_page(page)

    context = {
        "memo_list": page_obj,
        "memo_on_going": memo_on_going,
        "memo_finished": memo_finished,
        "memo_count": memo_qs.count(),
    }

    return render(request, "memo/index.html", context)


@staff_required
def index_status(request, status):
    # memo_status = get_object_or_404(Memo, status=status)
    path = request.path
    memo = Memo.objects.filter(status=status)
    memo_qs = Memo.objects.all()
    memo_on_going = memo_qs.filter(status=True)
    memo_finished = memo_qs.filter(status=False)
    page = request.GET.get("page", "1")

    paginator = Paginator(memo, 6)
    page_obj = paginator.get_page(page)

    context = {
        "memo_list": page_obj,
        "memo_on_going": memo_on_going,
        "memo_finished": memo_finished,
        "memo_count": memo_qs.count(),
        "path": path,
    }

    return render(request, "memo/index.html", context)


@method_decorator(staff_required, name="dispatch")
class MemoCreateView(LoginRequiredMixin, CreateView):
    model = Memo
    form_class = MemoForm
    template_name = "crispy_form.html"
    extra_context = {"form_title": "새 메모"}
    success_url = reverse_lazy("memo:index")

    def form_valid(self, form):
        new_memo = form.save(commit=False)
        new_memo.author = self.request.user
        new_memo.save()

        response = super().form_valid(form)

        messages.success(self.request, "새 메모가 작성 되었습니다.")
        return redirect(self.get_success_url())


memo_new = MemoCreateView.as_view()


@login_required(login_url="accounts:login")
def memo_edit(request, pk):
    memo = get_object_or_404(Memo, pk=pk)

    if request.user != memo.author:
        if request.META.get("HTTP_REFERER"):
            messages.error(request, "수정권한이 없습니다.")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "수정권한이 없습니다.")
            return redirect("core:root")

    if request.method == "GET":
        form = MemoForm(instance=memo)
    else:
        form = MemoForm(data=request.POST, files=request.FILES, instance=memo)
        if form.is_valid():
            form.save()
            messages.success(request, "메모가 수정 되었습니다.")
            return redirect("memo:index")

    return render(
        request,
        template_name="crispy_form.html",
        context={"form_title": "메모 수정", "form": form},
    )


@login_required(login_url="accounts:login")
def memo_delete(request, pk):
    memo = get_object_or_404(Memo, pk=pk)

    if request.user != memo.author:
        if request.META.get("HTTP_REFERER"):
            messages.error(request, "삭제권한이 없습니다.")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "삭제권한이 없습니다.")
            return redirect("core:root")

    memo.delete()
    messages.success(request, "메모가 삭제 되었습니다.")
    return redirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="accounts:login")
def memo_change_status(request, pk):
    memo = get_object_or_404(Memo, pk=pk)

    if request.user != memo.author:
        messages.error(request, "수정권한이 없습니다.")
        return redirect(request.META.get("HTTP_REFERER"))

    if memo.status:
        memo.status = False
        memo.save()
        messages.success(request, "메모 상태가 변경 되었습니다.")
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        memo.status = True
        memo.save()
        messages.success(request, "메모 상태가 변경 되었습니다.")
        return redirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="accounts:login")
def memo_like(request, pk):
    if request.user.is_authenticated:
        memo = get_object_or_404(Memo, pk=pk)

        if memo.like_users.filter(pk=request.user.pk).exists():
            memo.like_users.remove(request.user)
        else:
            memo.like_users.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    return redirect("accounts:login")
