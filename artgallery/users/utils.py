from django.db.models import Q
from .models import Profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate_profiles(request, profiles, results):

    page = request.GET.get('page')
    paginator = Paginator(profiles, results)
    
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    
    # represents the left button
    left_index = (int(page) - 4)
    if left_index < 1:
        left_index = 1
    
    # represents the right button
    right_index = (int(page) + 5)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return custom_range, profiles


def search_profiles(request):
    search_query = ''

    # checking to see if have a value in here, just in case
    # if we do, apply this filter
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    #checking if the current profile have these skills
    skills = Skill.objects.filter(name__icontains=search_query)

        # print('SEARCH:', search_query)

    # Searching through with OR using Q for 2 variables: name and short_intro
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
        )

    return profiles, search_query