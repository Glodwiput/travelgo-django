def is_admin(request):
    return{'is_admin':request.user.groups.filter(name='admim').exists()}
def is_staff(request):
    return{'is_staff':request.user.groups.filter(name='staff').exists()}
def is_customer(request):
    return{'is_customer':request.user.groups.filter(name='customer').exists()}