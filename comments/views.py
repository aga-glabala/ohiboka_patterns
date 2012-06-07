'''
Created on Mar 29, 2012

@author: agnis
'''
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
from django.contrib.comments.views.comments import post_comment
def pattern_comments(request, bracelet_id):
	return render_to_response('bracelet/tabs/comments.html', {'bracelet_id':bracelet_id}, RequestContext(request))

def pattern_comments_posted(request):
	return HttpResponse("1")

def pattern_comments_post(request):
	r = post_comment(request)
	if type(r).__name__ == "CommentPostBadRequest":
		return HttpResponse("0")
	return r