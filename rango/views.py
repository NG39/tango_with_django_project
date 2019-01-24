from django.shortcuts import render
from rango.models import Category, Page
from django.http import HttpResponse
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
        context_dict['query'] = category.name
    except Category.DoesNotExist:

        context_dict['category'] = None
        context_dict['pages'] = None
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
            context_dict['query'] = query
            context_dict['result_list'] = result_list
    return render(request, 'rango/category.html', context_dict)




