from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



def index(request):
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list,'pages': page_list}
	return render(request, 'rango/index.html', context=context_dict)
	#return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>")
	
def about(request):
	return render(request, 'rango/about.html')

def show_category(request, category_name_slug):

    context_dict = {}

    

    try:


        category = Category.objects.get(slug=category_name_slug)


        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages

        context_dict['category'] = category


    except Category.DoesNotExist:

        context_dict['category'] = None

        context_dict['pages'] = None



    context_dict['query'] = category.name


    result_list = []

    if request.method == 'POST':

        query = request.POST['query'].strip()

        if query:

            # Run our Webhose function to get the results list!

            result_list = run_query(query)

            context_dict['query'] = query

    context_dict['result_list'] = result_list


    return render(request, 'rango/category.html', context_dict)

    


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

    

    
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
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)
	
	
def register(request):

	registered = False

	if request.method == 'POST':

		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():

			user = user_form.save()

			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()

			registered = True
		else:

			print(user_form.errors, profile_form.errors)
	else:

		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request,
			'rango/register.html',
			{'user_form': user_form,
			'profile_form': profile_form,
			'registered': registered})
			
			
			
def user_login(request):
	error = None
	if request.method == 'POST':

		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:

			if user.is_active:

				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:

				error = "Your Rango account is disabled."
		else:

			print("Invalid login details: {0}, {1}".format(username, password))
			error = "Invalid login details supplied."

	else:

		return render(request, 'rango/login.html', {'error': error})
		
		
def some_view(request):
	if not request.user.is_authenticated():
		return HttpResponse("You are logged in.")
	else:
		return HttpResponse("You are not logged in.")
		
@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text!")
	
	
@login_required
def user_logout(request):
# Since we know the user is logged in, we can now just log them out.
	logout(request)
# Take the user back to the homepage.
	return HttpResponseRedirect(reverse('index'))