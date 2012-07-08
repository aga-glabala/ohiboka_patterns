'''
Created on Mar 20, 2012

@author: agnis
'''
import Image as pil
import time
from bracelet.models import Bracelet, Photo
from settings import MEDIA_ROOT

THUMBNAIL_WIDTH = 260
THUMBNAIL_HEIGHT = 100

def scale(f, inputdir, output):
	"""
	f- filename
	input - name of input directory
	output - name of output directory
	"""
	im = pil.open(inputdir + f)
	w, h = im.size
	if w > THUMBNAIL_WIDTH and h > THUMBNAIL_HEIGHT:
		im = im.resize((THUMBNAIL_WIDTH, int(THUMBNAIL_WIDTH / (w * 1.0 / h))))
		w, h = im.size
	thumb = pil.new(mode = "RGB", size = (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), color = "#fff")
	left = (THUMBNAIL_WIDTH - w) / 2
	top = (THUMBNAIL_HEIGHT - h) / 2
	thumb.paste(im, (left, top))
	thumb.save(output + f)

def handle_uploaded_file(f, bracelet_id, user):
	name = str(int(time.time() * 1000)) + "-" + str(bracelet_id) + str(f)[str(f).rfind("."):]
	photo = Photo(user = user, name = name, accepted = False, bracelet = Bracelet.objects.get(id = bracelet_id))
	photo.save()

	destination = open(MEDIA_ROOT + 'images/' + name, 'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()
	scale(name, MEDIA_ROOT + 'images/', MEDIA_ROOT + 'bracelet_thumbs/')
