from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.core.mail import send_mail
from Chong_site.form import ContactForm


def home(request):
    try:
        return render(request,'chongsite/home.html')
    except:
        raise Http404

def picture(request):
    try:
        return render(request,'chongsite/picture.html')
    except:
        raise Http404

def projects(request):
    try:
        return render(request,'chongsite/project.html')
    except:
        raise Http404

def misc(request):
    try:
        return render(request,'chongsite/misc.html')
    except:
        raise Http404

def contact(request):
    data = {'sender': 'Name',
        'email': 'Email',
        'subject': 'Subject',
         }
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            #cd = form.cleaned_data
            #send_mail(cd['subject'],cd['message'],cd['sender'],[r'lichong_79@hotmail.com'], fail_silently=False)
            #form = ContactForm(data)
            thank_message='You message has been successfully sent. I will get back to you ASAP. Thank you!'
        else:
            thank_message=''
    else:
        form = ContactForm(initial=data) # An unbound form
        thank_message=''

    return render(request, 'chongsite/contact.html', {
        'form': form,'thank_message':thank_message,
    })

def bio(request):
    try:
        return render(request,'chongsite/bio.html')
    except:
        raise Http404

def portforlio(request):
    try:
        return render(request,'chongsite/portfolio.html')
    except:
        raise Http404