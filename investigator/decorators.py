from functools import wraps
from django.shortcuts import get_object_or_404, redirect, HttpResponse
from .models import Case

def investigator_case_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        case = get_object_or_404(Case, pk=kwargs.get('pk'))
        # Check if the logged-in user is associated with the case
        if not case.investigator.user == request.user:
            return HttpResponse('Unauthorized Page')  # Redirect to unauthorized page or any other appropriate page
        return view_func(request, *args, **kwargs)
    return wrapper





def anonymous_required(view_func):
    """
    Decorator that redirects logged-in users away from the login page.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')  # Redirect to the index page or any other appropriate page
        return view_func(request, *args, **kwargs)
    return wrapper
