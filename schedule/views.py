from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from datetime import date, datetime, timedelta

from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views import generic
import calendar

from django.views.generic import CreateView, ListView, DetailView

from schedule.forms import EventForm
from schedule.models import Event
from schedule.utils import Calendar


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


@method_decorator(staff_required, name="dispatch")
class CalendarView(ListView):
    model = Event
    template_name = "schedule/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get("month", None))

        # Instantiate our calendar class with today's year and date

        cal = Calendar(d.year, d.month)
        cal.setfirstweekday(6)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = html_cal
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


index = CalendarView.as_view()


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


@method_decorator(staff_required, name="dispatch")
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "crispy_form.html"
    extra_context = {"form_title": "새 일정"}
    success_url = reverse_lazy("schedule:calendar")

    def form_valid(self, form):
        new_event = form.save(commit=False)
        new_event.author = self.request.user
        new_event.save()

        messages.success(self.request, "새 일정이 등록 되었습니다.")
        return redirect(self.success_url)


event_new = EventCreateView.as_view()


@method_decorator(staff_required, name="dispatch")
class EventDetailView(DetailView):
    model = Event


event_detail = EventDetailView.as_view()


@login_required(login_url="accounts:login")
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user != event.author:
        messages.error(request, "수정권한이 없습니다.")
        return redirect("schedule:calendar")

    if request.method == "GET":
        form = EventForm(instance=event)
    else:
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "일정이 수정 되었습니다.")
            return redirect("schedule:calendar")

    return render(
        request, "crispy_form.html", {"form_title": "일정 수정", "form": form}
    )


@login_required(login_url="accounts:login")
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user != event.author:
        messages.error(request, "삭제권한이 없습니다.")
        return redirect("schedule:event_detail", pk=pk)
    event.delete()
    messages.success(request, "일정이 삭제 되었습니다.")
    return redirect("schedule:calendar")
