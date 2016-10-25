from django.shortcuts import render, redirect
from .models import User, Quote, Favorite

# Create your views here.
def index(request):
    return render (request, 'quotes/index.html')

def register(request):
    if request.method == "POST":
        result = User.uManager.register(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=request.POST['password'], confirm=request.POST['confirm'], dob=request.POST['dob'])
        if result[0]:
            request.session['current_user_id'] = result[1].id
            request.session['errors'] = []
            return redirect('/quotes')
        else:
            request.session['errors'] = result[1]
            return redirect('/')
    else:
        return redirect ('/')

def login(request):
    if request.method == "POST":
        result = User.uManager.login(login_email=request.POST['login_email'], login_password=request.POST['login_password'])

        if result[0]:
            request.session['current_user_id'] = result[1][0].id
            request.session['errors'] = []
            return redirect('/quotes')
        else:
            request.session['errors'] = result[1]
            return redirect('/')
    else:
        return redirect ('/')

def dashboard(request):
    if request.session['current_user_id']:
        request.session['errors'] = []
        query = User.uManager.filter(id=request.session['current_user_id'])
        query2 = Quote.qManager.all()
        query3 = Favorite.objects.filter(user_id=request.session['current_user_id'])
        #to remove favorited quote from quotable quotes
        for x in query3:
            query2 = query2.exclude(id=x.quote.id)

        context = {
            'info' : query,
            'quotes' : query2,
            'favorites' : query3,
        }
        return render (request, 'quotes/dashboard.html', context)
    else:
        return redirect ('/')

def logout(request):
    request.session['current_user_id'] = ""
    request.session['errors'] = []
    request.session['contribute_errors'] = []
    return redirect('/')

def contribute(request):
    if request.method == "POST":
        result = Quote.qManager.add(author=request.POST['author'], message=request.POST['message'], user_id=request.session['current_user_id'])
        if result[0]:
            request.session['contribute_errors'] = []
            return redirect('/quotes')
        else:
            request.session['contribute_errors'] = result[1]
            return redirect('/quotes')
    else:
        return redirect ('/quotes')

def addfav(request, quote_id):
    Favorite.objects.create(user=User.uManager.get(id=request.session['current_user_id']), quote=Quote.qManager.get(id=quote_id))
    return redirect ('/quotes')

def removefav(request, quote_id):
    Favorite.objects.filter(user_id=User.uManager.get(id=request.session['current_user_id']), quote_id=quote_id).delete()
    return redirect ('/quotes')

def userpage(request, user_id):
    query = User.uManager.filter(id=user_id)
    query2 = Quote.qManager.filter(user_id=user_id)
    context = {
        'details' : query,
        'quotes' : query2,
        'count' : len(query2)
    }
    return render (request, 'quotes/userpage.html', context)
