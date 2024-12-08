def is_admin(request):
    if request.user.is_authenticated:
        return {'is_admin': request.user.groups.filter(name='admin').exists()}
    return {'is_admin': False}

def is_staff(request):
    if request.user.is_authenticated:
        return {'is_staff': request.user.groups.filter(name='staff').exists()}
    return {'is_staff': False}

def is_customer(request):
    if request.user.is_authenticated:
        return {'is_customer': request.user.groups.filter(name='customer').exists()}
    return {'is_customer': False}
