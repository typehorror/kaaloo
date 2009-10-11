from datetime import date, timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _

from common.shortcuts import render_response

from timer.models import TimeRecord
from timer.forms import CloseTimeRecordForm, OpenTimeRecordForm, CustomTimeForm, TimeRecordTitleForm


def paginate(records, page):
    paginator = Paginator(records, 10)

    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        records = paginator.page(page)
    except (EmptyPage, InvalidPage):
        records = paginator.page(paginator.num_pages)
    return records
    

@login_required
def time_records_view(request):
    time_records = paginate(TimeRecord.objects.get_time_records(request), 
                            int(request.GET.get('page', '1')))

    context = {'current':'times',
               'content_title': _('All times records'),
               'time_records': time_records}
    return render_response(request,'timer/time_records.html', context)

@login_required
def today_time_records_view(request):
    kw_filter = { 'start_date__gte': date.today()}
    time_records = paginate(TimeRecord.objects.get_time_records(request).filter(**kw_filter), 
                            int(request.GET.get('page', '1')))
    context = {'current':'times',
               'content_title': _('Today times records'),
               'time_records': time_records}
    return render_response(request,'timer/time_records.html', context)

@login_required
def last_week_time_records_view(request):
    kw_filter = {'start_date__gte': date.today() - timedelta(days=7)}
    time_records = paginate(TimeRecord.objects.get_time_records(request).filter(**kw_filter), 
                            int(request.GET.get('page', '1')))
    context = {'current':'times',
               'content_title': _('Last week times records'),
               'time_records': time_records}
    return render_response(request,'timer/time_records.html', context)

@login_required
def yesterday_time_records_view(request):
    kw_filter = { 'start_date__gte': date.today() - timedelta(days=1),
                  'start_date__lt': date.today()}

    time_records = paginate(TimeRecord.objects.get_time_records(request).filter(**kw_filter), 
                            int(request.GET.get('page', '1')))
    context = {'current':'times',
               'content_title':  _('Yesterday records'),
               'time_records': time_records}
    return render_response(request,'timer/time_records.html', context)

@login_required
def add_time_record_view(request):
    context = {'current':'times'}
    if request.POST:
        form = CustomTimeForm(request.POST)
        if form.is_valid():
            time_record = form.save(commit=False)
            time_record.user = request.user
            time_record.stop_date = datetime.today() + form.cleaned_data['time']
            time_record.save()
            context['added'] = True
            context['form'] = CustomTimeForm()
        else:
            context['form'] = form
    else:
        context['form'] = CustomTimeForm()
    return render_response(request,'timer/add_time_view.html', context)

def stop_timer(request):
    time_record = TimeRecord.objects.get_time_record(request)
    if time_record:
        time_record.stop_date = datetime.now()
        time_record.save()
        return render_to_response('timer_item.html', {'time_record': time_record})
    else:
        raise Http404

def start_timer(request):
    time_record = TimeRecord.objects.get_time_record(request, auto_create=True)
    return HttpResponse('{seconds:%d, id:%d}' % (time_record.seconds,time_record.id), mimetype='text/javascript')

def delete_timer(request, id):
    time_record = TimeRecord.objects.get_time_record(request, id=int(id))
    if time_record:
        time_record.delete()
        return HttpResponse('{result:true}', mimetype='text/javascript')
    else:
        return HttpResponse('{result:false}', mimetype='text/javascript')

def set_time_record(request, id):
    time_record = TimeRecord.objects.get_time_record(request, id=int(id))
    
    if not time_record:
        raise Http404

    if request.POST:
        if not time_record:
            raise Http404
        if time_record.stop_date:
            form = CloseTimeRecordForm(request.POST, instance=time_record)
        else:
            form = OpenTimeRecordForm(request.POST, instance=time_record)
        if form.is_valid():
            form.save()
            return render_to_response('timer_item.html', {'time_record':time_record})
        return render_to_response('timer/timer_item_form.html', {'form': form, 'time_record':time_record})
    else:
        if time_record.stop_date:
            form = CloseTimeRecordForm(instance=time_record)
        else:
            form = OpenTimeRecordForm(instance=time_record)
        return render_to_response('timer/timer_item_form.html', {'form': form, 'time_record':time_record})

@login_required
def set_actual_time_record_title(request):
    """
    Set the actual opened time record title.
    """
    time_record = TimeRecord.objects.get_time_record(request)
    if request.POST:
        form = TimeRecordTitleForm(request.POST, instance=time_record, prefix="task")
        if form.is_valid():
            time_record = form.save()
            return HttpResponse(time_record.title, mimetype="text/plain")
    raise Http404
