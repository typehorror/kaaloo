from timer.models import TimeRecord
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from datetime import datetime

from timer.forms import CloseTimeRecordForm, OpenTimeRecordForm

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
