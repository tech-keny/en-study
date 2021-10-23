from .models import Group, Level

def common(request):
    level_data = Level.objects.all()
    group_data = Group.objects.all()
    
    context = {
        'level_data': level_data,
        'group_data': group_data,

    }
    return context
