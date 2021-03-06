from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Count, Q, F, When, Case
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

from datetime import datetime
import datetime
import json
from decimal import Decimal

from gallerywalls.models import Gallery, Gallery_variation, Room, Placement, Gallery_item

from artevenue.views import price_views, cart_views

def get_gallery_walls(request, gallery_id=None, category_id = None, page = None, room_name=None, placement_name=None, color=None):
	
	sortOrder = request.GET.get("sort")
	color = request.GET.get("color", "")	
	room_name = request.GET.get("room_name", "")
	placement_name = request.GET.get("placement_name", "")
	set_of = request.GET.get("set_of", "")

	ikeywords = request.GET.get('keywords', '')	
	keywords = ikeywords.split()
	keyword_filter = False # Turned on only if a keyword filter is present (through the AJAX call)

	if page is None or page == 0:
		page = 1 # default

	gallery_parent = Gallery_variation.objects.filter(is_parent = True, gallery__is_published = True)
	total_galleries = gallery_parent.count()	

	gallery_variation = Gallery_variation.objects.filter(is_parent = False, gallery__is_published = True)

	filt_msg = ''
	if gallery_id:
		gallery_parent = gallery_parent.filter(gallery_id = gallery_id)
	if category_id:
		gallery_parent = gallery_parent.filter(gallery__stock_image_category_id = category_id)
	if room_name:
		gallery_parent = gallery_parent.filter(gallery__room__name = room_name)
		filt_msg = 'Showing ' + str(gallery_parent.count()) + ' gallery walls for ' + room_name
	if placement_name:
		gallery_parent = gallery_parent.filter(gallery__placement__name = placement_name)
		filt_msg = 'Showing ' + str(gallery_parent.count()) + ' gallery walls for ' + placement_name
	if color:
		gallery_parent = gallery_parent.filter(gallery__colors__icontains = color)
		filt_msg = 'Showing ' + str(gallery_parent.count()) + ' gallery walls in ' + color + ' colored theme'
	if set_of:
		gallery_parent = gallery_parent.filter(gallery__set_of__icontains = set_of)
		filt_msg = 'Showing ' + str(gallery_parent.count()) + ' gallery walls with set of ' + set_of + ' artworks'
	

	t_f = Q()
	f = Q()
	for w in keywords:
		if w == '':
			continue
		f = f | Q(key_words__icontains = w)
	t_f = t_f & f 

	gallery_parent = gallery_parent.filter( t_f )

	gallery_parent = gallery_parent.order_by('gallery__category_disp_priority', 'gallery_id')		
	gallery_filters = ['ROOM', 'PLACEMENT', 'COLORS', 'KEY_WORDS' ]

	rooms = Room.objects.all().values('name').distinct()	
	placements = Placement.objects.all().values('name').distinct()
	set_of = Gallery.objects.all().values('set_of').distinct()
	
	colors = ['Red', 'Orange',  'Yellow', 'Green', 'LightBlue', 'MediumPurple', 'Pink', 'Brown', 'black', 'White']
	key_words = Gallery.objects.all().values('colors').distinct()

	show = request.GET.get("show", "100")
	if show == None :
		show = 100
	
	if show == '100':
		perpage = 100 #default
		show = '100'
	else:
		if show == '500':
			perpage = 500
			show = '500'
		else:
			if show == '1000':
				perpage = 1000
				show = '1000'
			else:
				show = '100' # default
				perpage = 100
	

	paginator = Paginator(gallery_parent, perpage) 
	if not page:
		page = request.GET.get('page')
	
	galleries = paginator.get_page(page)			
	
	#=====================
	index = galleries.number - 1 
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = list(paginator.page_range)[start_index:end_index]
	#=====================

	template = "gallerywalls/gallery_walls_list.html"

	env = settings.EXEC_ENV
	
	return render(request, template, {
		'galleries':galleries, 'gallery_variation': gallery_variation,
		'sortOrder':sortOrder, 'rooms': rooms, 'placements': placements, 'set_of': set_of,
		'keywords':key_words, 'page':page, 'colors':colors,'env':env, 'filt_msg': filt_msg,
		'total_galleries': total_galleries} )


def gallery_wall_detail(request, gallery_id):

	gallery_parent = Gallery_variation.objects.get(gallery_id = gallery_id, is_parent = True)
	gallery_variations = Gallery_variation.objects.filter(gallery_id = gallery_id)
	gallery_items = Gallery_item.objects.filter(gallery_id = gallery_id, gallery_variation = gallery_parent)

	gallery_items_all = Gallery_item.objects.filter(gallery_id = gallery_id)
	prices = {}
	for v in gallery_variations:
		v_price = 0
		for i in gallery_items_all:
			if i.gallery_variation_id == v.id and i.gallery_id == v.gallery_id:
				i_price = get_variation_item_price(i.item_id)				
				v_price = v_price + i_price

		prices[v.id] = v_price
	
	return render(request, "gallerywalls/gallery_wall_detail.html", {
		'gal':gallery_parent, 'gallery_variations': gallery_variations,
		'gallery_items': gallery_items, 'prices': prices})

@csrf_exempt
def gallery_wall_detail_items(request):
	gallery_id = request.GET.get('gallery_id', '')
	gallery_variation_id = request.GET.get('gallery_variation_id', '')
	gallery_items = Gallery_item.objects.filter(gallery_id = gallery_id, gallery_variation_id = gallery_variation_id)

	
	return render(request, "gallerywalls/gallery_wall_detail_items.html", {'gallery_items': gallery_items})

@csrf_exempt	
def get_gallery_variation_and_price(request):

	item_price = 0
	img_height = 0
	img_width = 0
	stretch_id = 0
	image_price = 0
	moulding_price = 0
	acrylic_price = 0
	mount_price = 0
	stretch_price = 0
	board_price = 0
	
	msg = ""
	
	# Get prod items data.
	gallery_id = int(request.POST.get('gallery_id', '0'))
	gallery_variation_id = int(request.POST.get('gallery_variation_id', '0'))
	exclude_items = request.POST.getlist('exclude_items[]')

	gallery_items = Gallery_item.objects.filter(gallery_id = gallery_id, 
		gallery_variation_id = gallery_variation_id)
	
	if exclude_items:
		gallery_items = gallery_items.exclude(product_id__in = exclude_items)
		
	gallery_items = gallery_items.values(
			'item_id', 'gallery_id', 'gallery_variation_id', 'product_id', 'product_name', 'product_type_id',
			'moulding_id', 'moulding__name', 'moulding__width_inches', 'print_medium_id', 'mount_id',
			'mount__name', 'mount__color', 'mount_size', 'board_id', 'acrylic_id', 'stretch_id', 'image_width', 
			'image_height', 'moulding__width_inner_inches')

	gallery_variation_price = 0	
	for gal_item in gallery_items:
		item_price = get_variation_item_price(gal_item['item_id'])
		gallery_variation_price = gallery_variation_price + item_price

	return JsonResponse({"msg":msg, "gallery_variation_price": gallery_variation_price, 'gallery_items': list(gallery_items)})	

@csrf_exempt	
def get_variation_item_price(item_id):

	gal_item = Gallery_item.objects.filter(item_id = item_id).first()	
	item_price = 0
	
	if gal_item:
		#####################################
		#         Get the item price
		#####################################
		price = price_views.get_prod_price(gal_item.product_id,
				prod_type=gal_item.product_type_id,
				image_width=gal_item.image_width, 
				image_height=gal_item.image_height,
				print_medium_id = gal_item.print_medium_id,
				acrylic_id = gal_item.acrylic_id,
				moulding_id = gal_item.moulding_id,
				mount_size = gal_item.mount_size,
				mount_id = gal_item.mount_id,
				board_id = gal_item.board_id,
				stretch_id = gal_item.stretch_id)
		total_price = price['item_price']
		item_price = price['item_price']
		msg = price['msg']
		cash_disc = price['cash_disc']
		percent_disc = price['percent_disc']
		item_unit_price = price['item_unit_price']
		disc_amt = price['disc_amt']
		disc_applied = price['disc_applied']
		promotion_id = price['promotion_id']
		#####################################
		# END::::    Get the item price
		#####################################	

		#item_price = round(item_price, -1)
		item_price = Decimal(round(float(item_price),-1))

	return item_price

@csrf_exempt
def add_gallery_wall_to_cart(request):
	msg = ''

	gallery_id = int(request.POST.get('gallery_id', '0'))
	gallery_variation_id = int(request.POST.get('gallery_variation_id', '0'))
	exclude_items = request.POST.getlist('exclude_items[]')

	gallery_items = Gallery_item.objects.filter(gallery_id = gallery_id, 
		gallery_variation_id = gallery_variation_id)
	
	if exclude_items:
		gallery_items = gallery_items.exclude(product_id__in = exclude_items)
	
	total_cart_qty = 0
	for i in gallery_items:
		#from django.http import HttpRequest
		#req = HttpRequest()
		#req.method = 'POST'
		sqin = i.image_width * i.image_height;
		print_medium_size = sqin
		acrylic_size = sqin
		stretch_size = sqin
		
		request.POST = {'prod_id':i.product_id, 'qty':1, 'moulding_id': i.moulding_id,
							'width':i.image_width, 'height': i.image_height,
							'moulding_size' : i.moulding_size,
							'print_medium_id':i.print_medium_id, 'print_medium_size': print_medium_size, 
							'mount_id':i.mount_id, 'mount_size': i.mount_size,
							'mount_w_left' : 0, 'mount_w_right': 0, 
							'mount_w_top': 0, 'mount_w_bottom' : 0, 
							'acrylic_id': i.acrylic_id, 'acrylic_size':sqin,
							'board_id': i.board_id, 'board_size': sqin, 'stretch_id': i.stretch_id,
							'stretch_size': sqin, 
							'total_price': 0, 'image_width': i.image_width, 'image_height': i.image_height,
							'discount':0, 'promotion_id':None, 'disc_amt':0,
							'item_unit_price':0, 'prod_type': i.product_type_id
		}
		
		resp = cart_views.add_to_cart_new(request)
		result = json.loads(resp.content)	
		if 'status' in result:
			status = result['status']
		else:
			status = ''
		
		if 'cart_qty' in result:
			total_cart_qty = total_cart_qty + result['cart_qty']
			msg = 'SUCCESS'

	return JsonResponse({'status': status, 'msg': msg, 'cart_qty': total_cart_qty})