from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

# home_page = None

def home_page(request):
    # return HttpResponse('<html><title>To-Do lists</title></html>')
    # return HttpResponse()
    if request.method == 'POST':
        return HttpResponse(request.POST['item_text'])
    return render(request, 'home.html', {
        'new_item_text': request.POST.get('item_text',''),
    })
