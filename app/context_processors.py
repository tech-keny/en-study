from .models import Level

def common(request):
    level_data = Level.objects.all()
    
    context = {
        'level_data': level_data,

    }
    return context
