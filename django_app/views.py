from django.shortcuts import render
from django.views import View


class IndexView(View):
    ''' Class for the main page '''
    
    def get(self, request):
        ''' get handler '''
        return render(request, 'index.html')
