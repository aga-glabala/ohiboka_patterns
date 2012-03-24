'''
Created on Mar 20, 2012

@author: agnis
'''
import Image as pil
import time
from bracelet.models import Bracelet, Photo

def scale(f, inputdir, output):
	"""
	f- filename
	input - name of input directory
	output - name of output directory
	"""
	im = pil.open(inputdir+f)
	w,h=im.size
	if w>h:
		im.thumbnail((126,(126*h)/w), pil.ANTIALIAS)
	else:
		im.thumbnail(((w*126)/h,126), pil.ANTIALIAS)
	im.save(output+f)

def handle_uploaded_file(f, bracelet_id, user):
	name = str(int(time.time()*1000)) + "-"+str(bracelet_id)+str(f)[str(f).rfind("."):]
	photo = Photo(user = user, name = name, accepted = False, bracelet = Bracelet.objects.get(id=bracelet_id))
	photo.save()
	
	destination = open('static/images/'+name, 'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()
	scale(name, 'static/images/', 'static/bracelet_thumbs/')