from artevenue.models import Product_view, Moulding, Moulding_image
from artevenue.models import Curated_collection, Mount
from artevenue.models import Amazon_data, Stock_image_stock_image_category
from django.conf import settings
from decimal import Decimal

from PIL import Image, ImageFilter, ImageFile
import requests
from .product_views import *
from .tax_views import *
from .price_views import *
from artevenue.views import *

import requests
from io import BytesIO

ImageFile.LOAD_TRUNCATED_IMAGES = True

def amazon_data():


	curated = Curated_collection.objects.all()
	createAmazonData(curated)


def createAmazonData(curated):
	
	cnt = 0
	for c in curated:
		cnt = cnt + 1

		prod = Product_view.objects.get(product_id = c.product_id)
		if not prod:
			print( "No roduct found: ID = " + str(c.product_id) )
			return
		
		if (cnt % 2) == 0:
			moulding_id = 18
			img_width = 12
			mount_size = 1
		else:
			moulding_id = 1   ## To be replaced with correct id
			img_width = 24
			mount_size = 2

		img_height = round(img_width / prod.aspect_ratio)
		moulding = Moulding.objects.get( moulding_id = moulding_id )
		moulding_name = ''
		if moulding:
			moulding_name = moulding.name

		mount = Mount.objects.get(pk=3)   ## Offwhite
		mount_color = ''
		if mount :
			mount_color = mount.color
		category = Stock_image_stock_image_category.objects.get(
			stock_image_id = c.product_id)
		category_id = category.stock_image_category_id
		quantity = 1
		
		#####################################
		#         Get the item price
		#####################################
		price = get_prod_price(c.product_id, 
				prod_type= prod.product_type_id,
				image_width=img_width, 
				image_height=img_height,
				print_medium_id = 'PAPER',
				acrylic_id = 1,
				moulding_id = moulding_id,
				mount_size = mount_size,
				mount_id = mount.mount_id,
				board_id = 1,
				stretch_id = 0)
		item_price = price['item_price']
		msg = price['msg']
		cash_disc = price['cash_disc']
		percent_disc = price['percent_disc']
		item_unit_price = price['item_unit_price']
		item_disc_amt = price['disc_amt']
		disc_applied = price['disc_applied']
		promotion_id = price['promotion_id']
		#####################################
		# END::::    Get the item price
		#####################################	
		
		#####################################
		# 	if item price not found, return
		#####################################	
		if item_unit_price == 0 or item_unit_price is None:
			err_flg = True
			return( JsonResponse({'msg':'Price not avaiable for this image', 'cart_quantity':quantity}, safe=False) )
		##################################################
		# END:	if item price not found, don't add to cart
		##################################################

		
		
		########################################################
		#	Calculate sub total, tax for the item
		########################################################
		item_tax = 0
		item_sub_total = 0
		#### Get Tax
		taxes = get_taxes()
		if prod.product_type_id == 'STOCK-IMAGE':
			tax_rate = taxes['stock_image_tax_rate']
		if prod.product_type_id == 'ORIGINAL-ART':
			tax_rate = taxes['original_art_tax_rate']
		if prod.product_type_id == 'USER-IMAGE':
			tax_rate = taxes['user_image_tax_rate']
		if prod.product_type_id == 'STOCK-COLLAGE':
			tax_rate = taxes['stock_image_tax_rate']
		if prod.product_type_id == 'FRAME':
			tax_rate = taxes['frame_tax_rate']	
			
		# Calculate tax and sub_total
		item_sub_total = round( (item_price*quantity) / (1 + (tax_rate/100)), 2 )
		item_tax = round( (item_price*quantity) - item_sub_total )
		########################################################
		#	END: Calculate sub total, tax for the item
		########################################################
		

		##############################################################
		# 	Get the product promotion details, if the item carries it
		##############################################################
		promo = {}
		if prod:
			promo = get_product_promotion(prod.product_id)	
		promotion = None
		if promo :
			if promo['promotion_id']:
				promotion = Promotion.objects.filter(promotion_id = promo['promotion_id']).first()
		#####################################################
		# END:	Get the product promotion, if the item carries it
		#####################################################
		
		
		
		#####################################################
		# Create Amazone DATA
		#####################################################
		## Insert or Update
		promo_name = ''
		if promotion:
			promo_name = promotion.name
		hl = Amazon_data(
			product_id = prod.product_id,
			product_name = prod.name,
			description = prod.description,
			part_number = prod.part_number,
			product_type = prod.product_type,
			category = category.stock_image_category,
			category_name = category.stock_image_category.name,
			is_published = prod.is_published,
			aspect_ratio = prod.aspect_ratio,
			image_type = prod.image_type,
			orientation = prod.orientation,
			max_width = prod.max_width,
			max_height = prod.max_height,
			min_width = prod.min_width,
			publisher = prod.publisher,
			artist = prod.artist,
			colors = prod.colors,
			key_words = prod.key_words,
			url = prod.url,
			thumbnail_url = prod.thumbnail_url,
			framed_url = '',
			framed_thumbnail_url = '',
			promotion = promotion,
			promotion_name = promo_name,
			quantity = quantity,
			item_unit_price = item_unit_price,
			item_sub_total = item_sub_total,
			item_disc_amt  = item_disc_amt,
			item_tax  = item_tax,
			item_total = item_price,
			moulding = moulding,
			moulding_name = moulding.name,
			moulding_size = 0,
			print_medium_id = 'PAPER',
			print_medium_name = 'PAPER',
			print_medium_size = 0,
			mount = mount,
			mount_name = mount_color,
			mount_size = mount_size,
			board_id = 1,
			board_name = '1',
			board_size = 0,
			acrylic_id = 1,
			acrylic_name = '1',
			acrylic_size = 0,
			stretch_id = 1,
			stretch_name = '1',
			stretch_size = 0,
			image_width = img_width,
			image_height = img_height,
			created_date = today,
			updated_date = today
		)
		hl.save()		


		##################################################
		##################################################
		##################################################
		#   Create prod for same image without any frame
		##################################################
		##################################################
		##################################################
		if (cnt % 2) == 0:
			moulding_id = None
			img_width = 12
			mount_size = None
		else:
			moulding_id = None
			img_width = 24
			mount_size = None

		img_height = round(img_width / prod.aspect_ratio)
		moulding = None
		moulding_name = ''

		mount = None
		mount_id = None
		mount_color = ''

		category = Stock_image_stock_image_category.objects.get(
			stock_image_id = c.product_id)
		category_id = category.stock_image_category_id
		quantity = 1
		
		#####################################
		#         Get the item price
		#####################################
		price = get_prod_price(c.product_id, 
				prod_type= prod.product_type_id,
				image_width=img_width, 
				image_height=img_height,
				print_medium_id = 'PAPER',
				acrylic_id = 1,
				moulding_id = moulding_id,
				mount_size = mount_size,
				mount_id = mount_id,
				board_id = 1,
				stretch_id = 0)
		item_price = price['item_price']
		msg = price['msg']
		cash_disc = price['cash_disc']
		percent_disc = price['percent_disc']
		item_unit_price = price['item_unit_price']
		item_disc_amt = price['disc_amt']
		disc_applied = price['disc_applied']
		promotion_id = price['promotion_id']
		#####################################
		# END::::    Get the item price
		#####################################	
		
		#####################################
		# 	if item price not found, return
		#####################################	
		if item_unit_price == 0 or item_unit_price is None:
			err_flg = True
			return( JsonResponse({'msg':'Price not avaiable for this image', 'cart_quantity':quantity}, safe=False) )
		##################################################
		# END:	if item price not found, don't add to cart
		##################################################

		
		
		########################################################
		#	Calculate sub total, tax for the item
		########################################################
		item_tax = 0
		item_sub_total = 0
		#### Get Tax
		taxes = get_taxes()
		if prod.product_type_id == 'STOCK-IMAGE':
			tax_rate = taxes['stock_image_tax_rate']
		if prod.product_type_id == 'ORIGINAL-ART':
			tax_rate = taxes['original_art_tax_rate']
		if prod.product_type_id == 'USER-IMAGE':
			tax_rate = taxes['user_image_tax_rate']
		if prod.product_type_id == 'STOCK-COLLAGE':
			tax_rate = taxes['stock_image_tax_rate']
		if prod.product_type_id == 'FRAME':
			tax_rate = taxes['frame_tax_rate']	
			
		# Calculate tax and sub_total
		item_sub_total = round( (item_price*quantity) / (1 + (tax_rate/100)), 2 )
		item_tax = round( (item_price*quantity) - item_sub_total )
		########################################################
		#	END: Calculate sub total, tax for the item
		########################################################
		

		##############################################################
		# 	Get the product promotion details, if the item carries it
		##############################################################
		promo = {}
		if prod:
			promo = get_product_promotion(prod.product_id)	
		promotion = None
		if promo :
			if promo['promotion_id']:
				promotion = Promotion.objects.filter(promotion_id = promo['promotion_id']).first()
		#####################################################
		# END:	Get the product promotion, if the item carries it
		#####################################################
		
		
		
		#####################################################
		# Create Amazon DATA
		#####################################################
		## Insert or Update
		promo_name = ''
		if promotion:
			promo_name = promotion.name
		hl = Amazon_data(
			product_id = prod.product_id,
			product_name = prod.name,
			description = prod.description,
			part_number = prod.part_number,
			product_type = prod.product_type,
			category = category.stock_image_category,
			category_name = category.stock_image_category.name,
			is_published = prod.is_published,
			aspect_ratio = prod.aspect_ratio,
			image_type = prod.image_type,
			orientation = prod.orientation,
			max_width = prod.max_width,
			max_height = prod.max_height,
			min_width = prod.min_width,
			publisher = prod.publisher,
			artist = prod.artist,
			colors = prod.colors,
			key_words = prod.key_words,
			url = prod.url,
			thumbnail_url = prod.thumbnail_url,
			framed_url = '',
			framed_thumbnail_url = '',
			promotion = promotion,
			promotion_name = promo_name,
			quantity = quantity,
			item_unit_price = item_unit_price,
			item_sub_total = item_sub_total,
			item_disc_amt  = item_disc_amt,
			item_tax  = item_tax,
			item_total = item_price,
			moulding = moulding,
			moulding_name = '',
			moulding_size = 0,
			print_medium_id = 'PAPER',
			print_medium_name = 'PAPER',
			print_medium_size = 0,
			mount = None,
			mount_name = mount_color,
			mount_size = mount_size,
			board_id = None,
			board_name = '',
			board_size = 0,
			acrylic_id = None,
			acrylic_name = '',
			acrylic_size = 0,
			stretch_id = None,
			stretch_name = '',
			stretch_size = 0,
			image_width = img_width,
			image_height = img_height,
			created_date = today,
			updated_date = today
		)
		hl.save()		


	
	print("Data creation/Update complete: Count - " + str(cnt) )

def createAmazonImages():	
	amazon_data = Amazon_data.objects.all().order_by('amazon_key')
	import pdb
	pdb.set_trace()
	for h in amazon_data:
		if h.moulding:
			framed_img = get_amz_FramedImage_api(h.product_id, h.moulding_id, 
				h.mount.color, h.mount_size, h.image_width)
			f_nm = "f_"
		else:
			framed_img = get_amz_FramedImage_api(h.product_id)
			f_nm = "n_"
			
		env = settings.EXEC_ENV
		img_url = ''
		if env == 'DEV' or env == 'TESTING':
			img_loc = settings.BASE_DIR + '/artevenue/' + settings.STATIC_URL + "amazon_data/images/" 
			img_url = img_loc
		else:
			img_loc = settings.PROJECT_DIR + '/' + settings.STATIC_URL + "amazon_data/images/"
			img_url = 'https://www.artevenue.com' + settings.STATIC_URL + "amazon_data/images/"
		
		pos = h.url.rfind('/')
		loc = 0
		if pos > 0:
			loc = pos+1
		lowres_img_name = f_nm + h.url[loc:]
		
		# save image
		framed_img.save(img_loc + lowres_img_name)
		
		'''
		## Create thumbnail and save
		framed_img.thumbnail( (75, 75) )
		pos = h.thumbnail_url.rfind('/')
		loc = 0
		if pos > 0:
			loc = pos+1
		thumb_img_name = f_nm + h.thumbnail_url[loc:]
		framed_img.save(img_loc + thumb_img_name)
		'''
		
		## Save in urls table
		hf = Amazon_data.objects.filter(amazon_key = h.amazon_key).update(	
				framed_url = img_url + lowres_img_name)
		
		print("Saved: " + lowres_img_name)

def get_amz_FramedImage_api(prod_id, frame_id=None, mount_color=None, mount_size=None, user_width=None):

	# Get image
	prod_img = Stock_image.objects.filter( product_id = prod_id ).first()		
	env = settings.EXEC_ENV

	if env == 'DEV' or env == 'TESTING':
		response = requests.get(prod_img.url)
		img_source = Image.open(BytesIO(response.content))
	else:
		img_source = Image.open(settings.PROJECT_DIR + '/' + settings.STATIC_URL + prod_img.url)			
	
	## If no frame ID, return image without frame
	if not frame_id:
		return img_source
	
	# Get moulding
	moulding = Moulding_image.objects.filter(moulding_id = frame_id, image_type = "APPLY").values(
				'url', 'moulding__width_inches', 'border_slice').first()
	
	if moulding:
		m_width_inch = Decimal(moulding['moulding__width_inches'])
		
		# Image width displayed in browser in inches
		disp_inch = 450//96		
		ratio = disp_inch / user_width
		border = int(m_width_inch * ratio * 96)
		
		border = int(m_width_inch * 450 / user_width)
		
		m_size = int(mount_size * 96 * ratio)
		
		
		from django.http import HttpRequest
		request = HttpRequest()
		request.method = 'GET'
		
		if m_size > 0 and mount_color != '' and mount_color != '0' and mount_color != 'None':

			img_with_mount = image_views.addMount(img_source, mount_color, m_size, m_size, m_size, m_size)
						
			framed_img = image_views.applyBorder( request, img_with_mount, moulding['url'], border, border, border, border,
							float(moulding['border_slice']), float(moulding['border_slice']), 
							float(moulding['border_slice']), float(moulding['border_slice']) )
		else:
			framed_img = image_views.applyBorder( request, img_source, moulding['url'], border, border, border, border,
							float(moulding['border_slice']), float(moulding['border_slice']), 
							float(moulding['border_slice']), float(moulding['border_slice']) )
	else :
		# No moulding, returing the image as it is.
		framed_img = Image.new("RGB", (img_source.width, img_source.height), 0)
		framed_img.paste(img_source, (0,0))		
	
	return framed_img

	
def createAmazonFile():
	amz = Amazon_data.objects.filter(is_published = True).order_by('amazon_key')
	with open('Amazon_data.csv', 'w', newline='') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		row =['product_type', 'Seller SKU', 'Brand', 'Product ID', 'Product ID Type',
			  'Item Name', 'Manufacturer Part Number', 'Recommended Browse Nodes', 
			  'Color Name', 'Color Map', 'Size', 'Included Components', 
			  'Enclosure Material', 'Size Map', 'Batteries Included', 'Standard Price',
			  'Quantity', 'Update Delete', 'Maximum Retail Price', 'Main Image URL',
			  
			  'Manufacturer', 'Description', 'Model', 
			  
			  'Search Terms', 'Bullet Point', 'Bullet Point', 'Bullet Point',
			  'Bullet Point', 'Bullet Point', 'Occassion', 'Pattern', 
			  'Product Features', 'Product Features', 'Product Features',
			  'Product Features', 'Style', 'Number of Pieces', 'Power Source',
			  'Shape', 'Warranty Description', 'Safety Warning', 'Legal Disclaimer'
			]
		wr.writerow(row)
		for h in amz:
			length = h.image_height 
			if h.moulding:
				if h.moulding.width_inner_inches:
					length = length + (h.moulding.width_inner_inches * 2)
				if h.mount:
					if h.mount_size:
						length = length + (h.mount_size * 2)
			
			breadth = h.image_width 
			if h.moulding:
				if h.moulding.width_inner_inches:
					breadth = breadth + (h.moulding.width_inner_inches * 2)
				if h.mount:
					if h.mount_size:
						breadth = breadth + (h.mount_size * 2)

			prod_details = "Print on " + h.print_medium_id + "; "
			if h.moulding_id:
				prod_details = prod_details + "Image Print Size : " + str(h.image_width) + " X " + str(h.image_height) + "; " + "Frame: " + h.moulding.name + " (" + str(h.moulding.width_inches) + "inch, Polystyrene); "
			if h.mount_id:
				prod_details = prod_details + "Mount: " + str(h.mount_size) + ", Color: " + h.mount.name + "; "
				if h.moulding.width_inner_inches:
					prod_details = prod_details + "Total Size: " + str(h.image_width + (h.moulding.width_inner_inches *2) + (h.mount_size *2) ) + " X " + str(h.image_height + (h.moulding.width_inner_inches * 2) + ( h.mount_size * 2) ) + "; "
				else:
					prod_details = prod_details + "Total Size: " + str(h.image_width) + " X " + str(h.image_height) + "; "
				
			else:
				prod_details = prod_details + "Image Size : " + str(h.image_width) + " X " + str(h.image_height) + "; "
			
			if h.acrylic_id:
				prod_details = prod_details + "Acrylic covered; "
				
			#if i.stretch_id:
			#	prod_details = prod_details +  + "Canvas Stretched; "

			p_size = str(breadth) + '" X ' + str(length) + '" (inches)'
			search_terms = ("Art, Art Prints, Home Decor, Paintings, " + h.key_words.replace(' |', ','))[:150] 
			row =['furnitureanddecor', h.amazon_key, "Arte'Venue", 
					'', '', h.product_name, h.part_number, '4380583031',
					'Multi', 'Multi', p_size, prod_details,
					'Others', 'Medium', 'FALSE', h.item_total,
					'1000', 'Update', h.item_total, h.framed_url,
					'ArteVenue', 'We offer customization of print medium (Paper or Canvas), size, frame and mount. To customize the product please go to My Orders – Click on Contact Seller against the order - Select Subject as "Product Customization" - Write message/Add attachment - Send Mail.', '',
					search_terms, '', '' ,'' , 
					'', '', '', '',
					'', '', '', '',
					'', '', '1', 'NA', 'Square/Rectangle',
					'Carries no warranties', 'NA', 'Customized product, no returns unless delivered damaged goods. The colors seen and product sizes specificed may change slightly.'
				]
				
			'''		
			'product_type', 'Seller SKU', 'Brand', 'Product ID', 'Product ID Type',
			  'Item Name', 'Manufacturer Part Number', 'Recommended Browse Nodes', 
			  'Color Name', 'Color Map', 'Size', 'Included Components', 
			  'Enclosure Material', 'Size Map', 'Batteries Included', 'Standard Price',
			  'Quantity', 'Update Delete', 'Maximum Retail Price', 'Main Image URL',

			  'Manufacturer', 'Description', 'Model', 
			  
			  'Search Terms', 'Bullet Point', 'Bullet Point', 'Bullet Point',
			  'Bullet Point', 'Bullet Point', 'Occassion', 'Pattern', 
			  'Product Features', 'Product Features', 'Product Features', 'Product Features',
			  'Product Features', 'Style', 'Number of Pieces', 'Power Source',
			  'Shape', 'Warranty Description', 'Safety Warning', 'Legal Disclaimer'

			'''				
			
			wr.writerow(row)


@csrf_exempt		
def amazon_products(request):
	ikeywords = request.GET.get('keywords', '')
	keywords = ikeywords.split()
	keyword_filter = False # Turned on only if a keyword filter is present (through the AJAX call)
	page = 1 # default

	sortOrder = request.GET.get("sort")
	show = request.GET.get("show")
	
	prod_categories = Stock_image_category.objects.filter(store_id=settings.STORE_ID, trending = True )
	
	dt =  today.day
	products = Amazon_data.objects.all().order_by('amazon_key')
		
	width = 0
	height = 0
	if request.is_ajax():
		#Apply the user selected filters -

		# Get data from the request.
		json_data = json.loads(request.body.decode("utf-8"))

		major_array = []
		sub_array = []
		size_key = None
		size_val = None
		
		t_f = Q()
		for majorkey, subdict in json_data.items():
			#######################################
			s_keys = json_data[majorkey]
			f = Q()
			for s in s_keys:
				if majorkey == 'SIZE':
					# Get the size
					idx = s.find("_")
					width = int(s[:idx])
					height = int(s[(idx+1):])
					ratio = round(Decimal(width)/Decimal(height), 18)
					f = f | ( Q( aspect_ratio = ratio) & Q(max_width__gte = width) & Q(max_height__gte = height))				
			
				if majorkey == 'IMAGE-TYPE':
					f = f | Q(image_type = s)
				if majorkey == 'ORIENTATION':
					f = f | Q(orientation = s)
				if majorkey == 'ARTIST':
					f = f | Q(artist = s)
				if majorkey == 'COLORS':
					#f = f | Q(colors__icontains = s)
					f = f | Q(key_words__icontains = s)
				if majorkey == 'KEY-WORDS':
					ikeywords = s_keys[s] 
					print("Keywords: " + ikeywords)
					keywords = ikeywords.split()
					#f = f | Q(key_words__icontains = keywords)
					keyword_filter = True
				if majorkey == 'PAGE':									
					page = s_keys[s]
				if majorkey == 'SORT':
					sortOrder =  s_keys[s]
				if majorkey == 'SHOW':
					show =  str(s_keys[s])
			
			
			t_f = t_f & f
		products = products.filter( t_f )	

	# Apply keyword filter (through ajax or search)
	for word in keywords:
		products = products.filter( 
			Q(key_words__icontains = word) |
			Q(artist__icontains = word)
		)

	prod_filters = ['ORIENTATION', 'ARTIST', 'IMAGE-TYPE', 'COLORS']	
	prod_filter_values ={}
	orientation_values = products.values('orientation').distinct()
	
	or_arr = []
	for v in orientation_values:
		if v['orientation'] not in or_arr:
			or_arr.append ( v['orientation'] )
	prod_filter_values['ORIENTATION'] = or_arr 
	
	artist_values = products.values('artist').distinct().order_by('artist')
	ar_arr = []
	for a in artist_values:
		if a['artist'] not in ar_arr:
			ar_arr.append(a['artist'] )
	prod_filter_values['ARTIST'] = ar_arr 
	
	image_type_values = products.values('image_type').distinct()
	im_arr = []
	for i in image_type_values:
		if i['image_type'] not in im_arr:
			im_arr.append(i['image_type'] )
	prod_filter_values['IMAGE-TYPE'] = im_arr


	#image_type_values = products.values('colors').distinct()
	im_arr = ['Red', 'Orange',  'Yellow', 'Green', 'Blue', 'Purple', 'Pink', 'Brown', 'black', 'White']
	prod_filter_values['COLORS'] = im_arr
	
	price = Publisher_price.objects.filter(print_medium_id = 'PAPER') 

	if show == None :
		show = 50
	
	if show == '50':
		perpage = 50 #default
		show = '50'
	else:
		if show == '100':
			perpage = 100
			show = '100'
		else:
			if show == '1000':
				perpage = 1000
				show = '1000'
			else:
				show = '50' # default
				perpage = 50
				
	paginator = Paginator(products, perpage) 
	if not page:
		page = request.GET.get('page')

	prods = paginator.get_page(page)

	#=====================
	index = prods.number - 1 
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = list(paginator.page_range)[start_index:end_index]
	#=====================
		
	if request.is_ajax():

		template = "artevenue/homelane_prod_display_include.html"
	else :
		template = "artevenue/amazon_products.html"

	return render(request, template, {'prod_categories':prod_categories, 
		'products':products, 'prods':prods, 'sortOrder':sortOrder, 'show':show,'prod_filters':prod_filters,
		'prod_filter_values':prod_filter_values, 'price':price, 'show_artist':True,
		'width':width, 'height':height, 'page_range':page_range} )		
		