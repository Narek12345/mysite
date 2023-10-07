from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from .forms import EmailPostForm, CommentForm
from .models import Post, Comment


def post_list(request):
	post_list = Post.published.all()
	# Pagination with 3 posts per page.
	paginator = Paginator(post_list, 3)
	page_number = request.GET.get('page', 1)
	try:
		posts = paginator.page(page_number)
	except PageNotAnInteger:
		# If PageNotAnInteger is not an integer, then output the first page.
		posts = paginator.page(1)
	except EmptyPage:
		# If EmptyPage is out of range, then output the last page.
		posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day)
	return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
	# Extract post by id.
	post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
	sent = False

	if request.method == 'POST':
		# The form has been submitted for processing.
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# The form fields were successfully validated.
			cd = form.cleaned_data
			# Send an email.
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = f'{cd["name"]} recommends you read {post.title}'
			message = f'Read {post.title} at {post_url}\n\n{cd["name"]} comments: {cd["comments"]}'
			send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to']])
			sent = True
	else:
		form = EmailPostForm()
	return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
	post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
	comment = None
	# Comment sent.
	form = CommentForm(data=request.POST)
	if form.is_valid():
		# Create a Comment class object without storing it in the db.
		comment = form.save(commit=False)
		# Assign post to comment.
		comment.post = post
		# Save comment in db.
		comment.save()
	return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})