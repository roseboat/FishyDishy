# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from rango.models import Category
from rango.models import Page

from rango.models import Fish

from rango.models import Recipe
from rango.models import Review
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm, RecipeForm
from  django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime

# Create your views here.
def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine.

    request.session.set_test_cookie()
    # this queries Category model to retrieve top five cate
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    recipe_list = Recipe.objects.order_by('-avgRating')[:5]
    
    context_dict = {'categories': category_list, 'pages': page_list, 'recipes': recipe_list}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    # Obtain our respnse object early so we can add cookie information
    response = render(request, 'rango/index.html', context=context_dict)

    # call the helper function to handle the cookies
    # Return response back to the user, updating any cookies that need changed
    return response

    # return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>")


def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    context_dict = {'boldmessage': "The king of cats"}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render (request,'rango/about.html', context=context_dict)
    # return HttpResponse("Rango says here is the about page!<br/> <a href='/rango/'>Index</a>")
    #return render(request, 'rango/about.html', context=context_dict)
    return response

def fish_finder(request):

    fish_list = Fish.objects.order_by('name')[:5]
    context_dict = {'fishList': fish_list}
    
    response = render (request,'rango/fish_finder.html', context=context_dict)
    
    
    return response

def fish_map(request):

    response = render (request,'rango/fish_map.html')
    return response

def show_category(request, category_name_slug):
    #create a context dictionary which we can pass to template rendering engine
    context_dict= {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        #Retrieve all of the assosicated pages.
        #Note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        #adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary
        # well use this in the template to verify that the categories exists
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didnt find the specified category.
        # Dont do anything
        # the templates will display the "no category' message
        context_dict['category'] = None
        context_dict['pages'] = None

        # Go render the response and return it to the client
    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    # HTTP POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # provided valid form?
        if form.is_valid():
            # save new cate to DB
            form.save(commit=True)
            # could give a confirmation message
            # but recent category is added on index page
            # and direct user back to index page
            return index(request)
        else:
            print(form.errors)

    return  render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
         category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
         category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
             if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
             else:
                print(form.errors)

    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict,)

@login_required
def add_recipe(request):
    form = RecipeForm()

    # HTTP POST
    if request.method == 'POST':
        form = RecipeForm(request.POST)

        # provided valid form?
        if form.is_valid():
            # save new cate to DB
            form.save(commit=True)
            # could give a confirmation message
            # but recent category is added on index page
            # and direct user back to index page
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_recipe.html', {'form': form})





"""def register(request):
    # A boolean value for telling the template whether the registration
    # was successful. Set to false initially. code changes value to true
    # when registration succeeds.
    registered = False

    # If its a HTTP POST, we interested in processing form data
    if request.method == 'POST':
        # Attempt to grab info from the raw form information
        # Note that we make use of both Userform and UserProfileForm
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid then..
        if user_form.is_valid() and profile_form.is_valid():
            # Save the users form data to database
            user = user_form.save()

            # now hash password with set_password metthod
            # Once hashed, we can update the user object
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance
            # Since we need to set the user attribute ourselves
            # we set commit=False. This delays saving the model
            # until we ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile pic?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful
            registered = True
        else:
            # invalid form or forms- mistakes or something else?
            # print problems to terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on context.
    return render (request,
                   'rango/register.html',
                   {'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered})"""


"""def user_login(request):
    # if the request is a HTTP POST, try to pull out the relevant information
    if request.method == 'POST':
        # Gather the username and password provided by the user
        # This information is obtained from the login form
        # We use request.POST.get('<variable>') as opposed
        # to request.POST{'<variable>'}, because the
        # request.POST.get('<varibale>') returns None if the
        # value does not exist, while the second one will raise
        # a KeyError exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Djanjos machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is
        user = authenticate(username=username, password=password)

        # if we have a User object, the detials are correct.
        # If None, no user with mathcing credentials was found.
        if user:
            # is the account active? it could have been disabled
            if user.is_active:
                # If the account is valid and active, we can log the user in
                # We'll send the user back to the homepage
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in
                return HttpResponse("Your Rango account is disabled.")
        else:
            # bad login details were provided. So we cant log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenerio would most likely be a HTTP GET.
    else:
        # No contect variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})"""

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

"""# Use the login_required decorator to ensure only those logged in can
# access the view
@login_required
def user_logout(request):
    # Since we know the user is loggin in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage
    return HttpResponseRedirect(reverse('index'))"""

# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# Updated the function definition
def visitor_cookie_handler(request):
    # Get the number of visits to the site.
    # we use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesnt exist, then the default value of 1 is used.
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    # If its been more than a day since the last visit...
    if(datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:

        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits
