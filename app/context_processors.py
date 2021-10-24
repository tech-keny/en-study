from .models import Group, Level, Part, StudyTime

def common(request):
    level_data = Level.objects.all()
    group_data = Group.objects.all()
    part_data = Part.objects.all()
    study_time_data = StudyTime.objects.all()
    
    context = {
        'level_data': level_data,
        'group_data': group_data,
        'part_data': part_data,
        'study_time_data':study_time_data

    }
    return context
