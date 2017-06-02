try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except: 
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q
# Create your views here.
from comments.forms import CommentForm
from comments.models import Comment
from .forms import CareerForm
from .models import Career



def careers_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = CareerForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user = request.user
		instance.save()
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form,
	}
	return render(request, "career_form.html", context)

def careers_detail(request, slug = None):
	instance = get_object_or_404(Career, slug = slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.description)

	initial_data = {
		"content_type": instance.get_content_type,
		"object_id": instance.id 
	}

	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs =  Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(
									user = request.user,
									content_type = content_type,
									object_id = obj_id,
									content = content_data,
									parent = parent_obj,
								)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments

	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form": form,
	}
	return render(request, "career_detail.html", context)

def careers_list(request):
	today = timezone.now().date()
	queryset_list = Career.objects.active()
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Career.objects.all()

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query) 
				).distinct()

	paginator = Paginator(queryset_list, 4) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context = {
		"career_list": queryset,
		"title": "Career Paths",
		"today": today,
	}
	return render(request, "career_list.html", context)


def careers_update(request, slug = None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Career, slug = slug)
	form = CareerForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "Changes Successfully Saved")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form": form,
	}
	return render(request, "career_form.html", context)

def careers_delete(request, slug = None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Career, slug = slug)
	instance.delete()
	messages.success(request, "Successfully Deleted")
	return redirect("careers:list")
