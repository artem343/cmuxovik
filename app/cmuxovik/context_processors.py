import datetime
from .models import Cmux


def number_of_unapproved(request):
    number = Cmux.objects.filter(is_approved=False).count()
    return {
        'number_of_unapproved': number
    }
