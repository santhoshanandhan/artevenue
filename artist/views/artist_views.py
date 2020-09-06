from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, DatabaseError, Error
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q, F
from django.http import HttpResponse, JsonResponse

from artist.models import Artist_group, Artist_sms_email, Artist, Artist_original_art
from artevenue.models import Country, State, City, Pin_code, Ecom_site, Original_art
from artevenue.models import Original_art_original_art_category, Stock_image_category
from artevenue.models import Wishlist, Wishlist_item_view, Publisher_price
from artevenue.models import Print_medium, Cart_item_view

from artist.forms import artistGroupForm, artistRegisterForm, artistUserForm, artistProfileForm
from artevenue.forms import registerForm

from artevenue.views import price_views, frame_views
from artevenue.decorators import is_artist

from django.contrib import messages
import datetime
import re



ecom = Ecom_site.objects.get(pk=settings.STORE_ID)
wall_colors = ['255,255,255', '255,255,224', '242,242,242', '230,242,255', '65,182,230', '64,224,208', '204,255,204', '128,128,0', '255,255,179', '255,205,72', '255,215,0', '255,230,230', '137,46,58', '255,0,0']

def register_as_artist(request, email=None):
	msg =''
	if request.method == 'POST':	
		next = request.POST['curr_pg']
		form = artistUserForm(request.POST)
		artistform = artistRegisterForm(request.POST)
		if form.is_valid():
			if artistform.is_valid():
				user = form.save()
				auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
				
				artistf = artistform.save(commit=False)
				artistf.user = user
				artistf.save()

				# Update email, sms table				
				tday = datetime.datetime.today()
				a_email = Artist_sms_email(
					user = user,
					msg_type = 'NEW-ACCNT',
					email_sent = False,
					sms_sent = False,
					created_date = tday,	
					updated_date = tday
				)
				a_email.save()
				
				# After successful sign up redirect to cuurent page
				return redirect('artist_registration_confirmation', id=user.id)
	else:
		email = request.GET.get('email', '')
		if email:
			form = artistUserForm({'email':email})
			artistform = artistRegisterForm()
		else:
			form = artistUserForm()
			artistform = artistRegisterForm()


	country_list = Country.objects.all()
	country_arr = []
	for c in country_list:
		country_arr.append(c.country_name)
		
	state_list = State.objects.all()
	state_arr = []
	for s in state_list:
		state_arr.append(s.state_name)
		
	
	city_list = City.objects.all()
	city_arr = []
	for ct in city_list:
		city_arr.append(ct.city)
	
	pin_code_list = Pin_code.objects.all()
	pin_code_arr = []
	for p in pin_code_list:
		pin_code_arr.append(p.pin_code)
		
		
	return render(request, "artist/artist_registration.html", {'form':form, 
			'artistform':artistform, 'country_arr':country_arr, 'state_arr':state_arr,
			'city_arr':city_arr, 'pin_code_arr':pin_code_arr} )
	
@login_required
def artist_registration_confirmation(request, id):

	try:
		artist = Artist.objects.get(user_id=id)
	except Artist.DoesNotExist:
		artist = {}
	return render(request, "artist/artist_registration_confirmation.html", {'artist':artist} )


@is_artist
def create_artist_profile(request):
		
	try:
		userObj = User.objects.get(username = request.user)
		artist = Artist.objects.get(user = userObj)
	except Artist.DoesNotExist:
		artist = None
	except User.DoesNotExist:
		userObj = None
		artist = None
		
	return render(request, "artist/create_artist_profile.html", {'artist':artist} )

@login_required
def artist_webpage(request, url_name, cat_id = '', page = 1):
	ikeywords = request.GET.get('keywords', '')
	keywords = ikeywords.split()
	keyword_filter = False # Turned on only if a keyword filter is present (through the AJAX call)
	sortOrder = request.GET.get("sort")
	show = request.GET.get("show", '50')

	if page is None or page == 0:
		page = 1 # default

	try:
		artist = Artist.objects.get(url_name__iexact=url_name)
		form = artistProfileForm(instance=artist)
	except Artist.DoesNotExist:
		artist = {}

	a_prods = Artist_original_art.objects.filter(artist_id = artist.artist_id).values('product_id')
	products = Original_art.objects.filter(product_id__in = a_prods, 
				is_published = True)
				
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
				
	return render(request, "artist/artist_webpage.html", {'form':form,
		'artist':artist,'prods':prods} )


@staff_member_required
def create_artist_group(request):
	##curr_groups = Artist_group.objects.all()
	if request.method == 'POST':	
		next = request.POST['curr_pg']
		form = registerForm(request.POST)

		if form.is_valid():
			grp = form.save()

			# After successful sign up redirect to current page
			return redirect('index')
	else:
		form = artistGroupForm()
		
	return render(request, "artist/create_artist_group.html", {'form':form,
			##'curr_groups':curr_groups
			})
			
			
def get_original_arts(request, cat_nm = None, page = None, curated_coll_id = None):
	if cat_nm:
		if cat_nm != 'Still-Life' and cat_nm != 'X-Ray':
			cat_nm = cat_nm.replace("-", " ")
		try:
			product_cate = Stock_image_category.objects.filter(name = cat_nm).first()
			cat_id = product_cate.category_id
		except Stock_image_category.DoesNotExist:
			cat_id = 0
			product_cate = None
		except Stock_image_category.MultipleObjectsReturned:
			cat_id = 0
			product_cate = None		
	else:
		cat_id = 0
		product_cate = None
		
	if page is None:
		page = request.GET.get("page_num", 1)

	sortOrder = request.GET.get("sort")
	show = request.GET.get("show", "100")
	result_limit = request.GET.get("result_limit", "0-50")
	filt_colors = request.GET.get("filt_colors", "")
	colors = filt_colors.split('|')
	
	filt_size = request.GET.get("filt_size", "")
	filt_width = request.GET.get("filt_width", "")
	filt_height = request.GET.get("filt_height", "")
	filt_artist = request.GET.get("filt_artist", "")
	artists = filt_artist.split('|')
	
	filt_orientation = request.GET.get("filt_orientation", "")
	orientation = filt_orientation.split('|')

	filt_image_type = request.GET.get("filt_image_type", "")
	image_type = filt_image_type.split('|')

	ikeywords = request.GET.get('keywords', '')	
	keywords = ikeywords.split()
	keyword_filter = False # Turned on only if a keyword filter is present (through the AJAX call)

	if page is None or page == 0:
		page = 1 # default

	prod_categories = Stock_image_category.objects.filter(store_id=settings.STORE_ID, trending = True )

	if cat_id:
		category_prods = Original_art_original_art_category.objects.filter(
				stock_image_category_id = cat_id).values('original_art_id')
		products = Original_art.objects.filter(product_id__in = category_prods, 
				is_published = True)
	elif curated_coll_id:
		curated_coll = Curated_collection.objects.filter(curated_category_id = curated_coll_id,
				product_type_id = 'ORIGINAL-ART').values('product_id')
		try:
			product_cate = Curated_category.objects.get(category_id = curated_coll_id);
		except Curated_category.DoesNotExist:
			product_cate = {}
		products = Original_art.objects.filter(product_id__in = curated_coll, 
			is_published = True)
	else :
		category_prods = Original_art_original_art_category.objects.values('original_art_id')		
		product_cate = {}		
		products = Original_art.objects.filter(product_id__in = category_prods, 
				is_published = True)

	if request.user.is_authenticated:
		user = User.objects.get(username = request.user)
		wishlist = Wishlist.objects.filter(
			user = user).values('wishlist_id')
		wishlistitems = Wishlist_item_view.objects.filter(
			wishlist_id__in = wishlist, product_type_id = 'ORIGINAL-ART')
	else:
		session_id = request.session.session_key
		wishlist = Wishlist.objects.filter(
			session_id = session_id).values('wishlist_id')
		wishlistitems = Wishlist_item_view.objects.filter(
			wishlist_id__in = wishlist, product_type_id = 'ORIGINAL-ART')

	wishlist_prods = []
	if wishlistitems:
		for w in wishlistitems:
			wishlist_prods.append(w.product_id)
		
	
	###### Apply the user selected filters
	t_f = Q()
	f = Q()

	if filt_size:
		# Get the size
		idx = filt_size.find("_")
		filt_width = int(filt_size[:idx])
		filt_height = int(filt_size[(idx+1):])
		ratio = round(Decimal(filt_width)/Decimal(filt_height), 18)
		#f = f | Q( aspect_ratio = ratio) & Q(max_width__gte = filt_width) & Q(max_height__gte = filt_height)
		products = products.filter(aspect_ratio = ratio, art_width__gte = filt_width, art_height__gte = filt_height)

	t_f = t_f & f 
	
	f = Q()
	for i in image_type :
		if i == '':
			continue
		f = f | Q(image_type = i)

	t_f = t_f & f 
		
	f = Q()
	for o in orientation:
		if o == '':
			continue
		f = f | Q(orientation = o)
	t_f = t_f & f 
	
	f = Q()
	for a in artists:
		if a == '':
			continue	
		f = f | Q(artist = a)
	t_f = t_f & f 
	
	f = Q()
	for c in colors:
		if c == '':
			continue
		f = f | Q(key_words__icontains = c)
	t_f = t_f & f 
	
	print (t_f)
	products = products.filter( t_f )

	# Apply keyword filter (through ajax or search)
	for word in keywords:
		if word == '':
			continue
		products = products.filter( 
			Q(key_words__icontains = word) |
			Q(artist__icontains = word) |
			Q(name__icontains = word) |
			Q(part_number__icontains = word)
			)
	
	products = products.order_by('category_disp_priority')
	
	price = Publisher_price.objects.filter(print_medium_id = 'PAPER') 
	
	prod_filters = ['ORIENTATION', 'ARTIST', 'COLORS']	
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

	#image_type_values = products.values('colors').distinct()
	im_arr = ['Red', 'Orange',  'Yellow', 'Green', 'Blue', 'Purple', 'Pink', 'Brown', 'black', 'White']
	prod_filter_values['COLORS'] = im_arr

	####################################
	####### Limiting the result set
	####################################
	slab_0_50 = 'NO'
	slab_50_100 = 'NO'
	slab_100_150 = 'NO'
	slab_150_200 = 'NO'
	slab_200_plus = 'NO'
	
	sliced_count = 0
	total_count = products.count()
	if total_count > 50000 and result_limit != '0-50':		
		slab_0_50 = 'YES'
	if total_count > 50000 and result_limit != '50-100':		
		slab_50_100 = 'YES'
	if total_count > 100000 and result_limit != '100-150':
		slab_100_150 = 'YES'
	if total_count > 150000  and result_limit != '150-200':		
		slab_150_100 = 'YES'
	if total_count > 200000  and result_limit != '200+':
		slab_200_plus = 'YES'


	if result_limit == '0-50':
		products = products[:50000]
	elif result_limit == '50-100':
		products = products[50001:100000]
	elif result_limit == '100-150':
		products = products[100001:150000]
	elif result_limit == '150-200':
		products = products[150001:200000]
	elif result_limit == '200+':
		products = products[200001:]

	sliced_count = products.count()
	####################################
	####### END: Limiting the result set
	####################################

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
	
	template = "artevenue/original_art_by_category.html"

	env = settings.EXEC_ENV

	print("prod_categories:")
	print(prod_categories)
	print("=========================")
	print("product_category")
	print(product_cate)
	
	
	return render(request, template, {'prod_categories':prod_categories, 
		'category_prods': category_prods, 'product_category':product_cate, 
		'products':products, 'prods':prods, 'sortOrder':sortOrder, 'show':show,'prod_filters':prod_filters,
		'prod_filter_values':prod_filter_values, 'price':price, 'ikeywords':ikeywords,
		'page':page, 'wishlistitems':wishlistitems, 'wishlist_prods':wishlist_prods,
		'filt_width':filt_width, 'filt_height':filt_height, 'page_range':page_range, 'result_limit':result_limit,
		'filt_colors':filt_colors, 'filt_size':filt_size, 'filt_artist':filt_artist,
		'filt_orientation':filt_orientation, 'filt_image_type':filt_image_type,
		'total_count':total_count, 'sliced_count':sliced_count, 'result_limit':result_limit,
		'slab_0_50':slab_0_50, 'slab_50_100':slab_50_100, 'slab_100_150':slab_100_150, 
		'slab_150_200':slab_150_200, 'slab_200_plus':slab_200_plus, 'env':env} )


def original_art_detail(request, prod_id = ''):
	cart_item_id = request.GET.get("cart_item_id", "")
	wishlist_item_id = request.GET.get("wishlist_item_id", "")
	if not prod_id or prod_id == '' :
		prod_id = request.GET.get("product_id", "")
	
	if prod_id == None:
		render(request, "artevenue/original_art_detail.html", {} )
	
	# get the product
	try:
		product = Original_art.objects.get(is_published = True, pk=prod_id)
	except Original_art.DoesNotExist:
		render(request, "artevenue/original_art_detail.html", {} )
		
	product_category = Original_art_original_art_category.objects.get(original_art = product)
	
	prod_categories = Original_art_original_art_category.objects.filter(
		stock_image_category__store_id=settings.STORE_ID)
	
	printmedium = Print_medium.objects.all()

	##############################################
	## Get the similar products
	##############################################
	similar_products = {}
	## First get rpoducts by same artist
	similar_products_artist = Original_art.objects.filter(  
			artist = product.artist).exclude(product_id = prod_id)
	## If same artist has more than 8 products, then filter further
	if similar_products_artist:
		if similar_products_artist.count() > 8 :
			## Filter for the same artist and same category
			prods_in_cat = Original_art_original_art_category.objects.filter(
				stock_image_category_id = product_category.stock_image_category).values('stock_image_id')
				
			similar_products_cat = similar_products_artist.filter(
				product_id__in = prods_in_cat)
			## Same artist has more than 8 products in same category, filter further
			if similar_products_cat: 
				if similar_products_cat.count() > 8 :
					## Filter for having same key words
					similar_products_kw = similar_products_cat.filter( key_words__in = product.key_words )
					if similar_products_kw :
						if similar_products_kw.count() > 8:
							similar_products = similar_products_kw
						else :
							similar_products = similar_products_cat.filter(
								product_id__in = prods_in_cat)
					else:
						similar_products = similar_products_cat.filter(
							product_id__in = prods_in_cat)
						
				## if the filter causes the result to be empty, revert to earlier filter
				else:
					similar_products = Original_art.objects.filter(  
							artist = product.artist)
			else :
					similar_products = Original_art.objects.filter(  
						artist = product.artist)
		else:
			similar_products = Original_art.objects.filter(  
					artist = product.artist)

	## Restrict the result to 10 products
	if similar_products:
		if similar_products.count() > 8:
			similar_products = similar_products[:8]

	price = Publisher_price.objects.filter(print_medium_id = 'PAPER') 


	if request.user.is_authenticated:
		user = User.objects.get(username = request.user)
		wishlist = Wishlist.objects.filter(
			user = user).values('wishlist_id')
		wishlistitems = Wishlist_item_view.objects.filter(
			wishlist_id__in = wishlist)
	else:
		session_id = request.session.session_key
		wishlist = Wishlist.objects.filter(
			session_id = session_id).values('wishlist_id')
		wishlistitems = Wishlist_item_view.objects.filter(
			wishlist_id__in = wishlist)

	wishlist_prods = []
	if wishlistitems:
		for w in wishlistitems:
			wishlist_prods.append(w.product_id)

	
	# Get image price on paper and canvas
	per_sqinch_price = price_views.get_per_sqinch_price(prod_id, 'STOCK-IMAGE')
	per_sqinch_paper = per_sqinch_price['per_sqin_paper']
	per_sqinch_canvas = per_sqinch_price['per_sqin_canvas']

	# get mouldings
	mouldings = frame_views.get_mouldings(request)
	# defaul we send is for PAPER
	paper_mouldings_apply = mouldings['paper_mouldings_apply']
	paper_mouldings_show = mouldings['paper_mouldings_show']
	moulding_diagrams = mouldings['moulding_diagrams']
	# get mounts
	mounts = frame_views.get_mounts(request)

	# get arylics
	acrylics = frame_views.get_acrylics(request)
	
	# get boards
	boards = frame_views.get_boards(request)

	# get Stretches
	stretches = frame_views.get_stretches(request)

	# get the images with all mouldings
	###############img_with_all_mouldings = get_ImagesWithAllFrames(request, prod_id, 16)
	
	# Check if request contains any components, if it does send those to the front end
	cart_item_view = {}
	if cart_item_id != '':
		cart_item_view = Cart_item_view.objects.filter(cart_item_id = cart_item_id).first()
	wishlist_item_view = {}
	if wishlist_item_id != '':
		wishlist_item_view = Wishlist_item_view.objects.filter(wishlist_item_id = wishlist_item_id).first()

	art_width = product.art_width
	art_height = product.art_height

	request.session.set_test_cookie()   ## To test if cookie is enabled on the browser. If not display message in Size and Color Tool.

	return render(request, "artevenue/original_art_detail.html", {'product':product,
		'prod_categories':prod_categories, 'printmedium':printmedium, 'product_category':product_category,
		'mouldings_apply':paper_mouldings_apply, 'mouldings_show':paper_mouldings_show, 'mounts':mounts,
		'per_sqinch_paper':per_sqinch_paper, 'per_sqinch_canvas':per_sqinch_canvas, 'acrylics':acrylics,
		'boards':boards, 
		#######'img_with_all_mouldings':img_with_all_mouldings, 
		'stretches':stretches,
		'cart_item':cart_item_view, 'art_width':art_width, 'art_height':art_height,
		'prods':similar_products, 'price':price, 'wishlist_prods':wishlist_prods,
		'wall_colors':wall_colors} )

@csrf_exempt
def upload_artist_photo(request):
	today = datetime.date.today()
	img_str = ''
	if request.method == 'POST':
		from PIL import Image, ExifTags
		from io import BytesIO
		import base64

		file = request.FILES.get('file')
		session_id = request.session.session_key
		user = None
		
		if request.user.is_authenticated:
			try:
				user = User.objects.get(username = request.user)
				artist = Artist.objects.get(user = user)
			except User.DoesNotExist:
				user = None
			except Artist.DoesNotExist:
				artist = None
		else:
			HttpResponse(img_str)

		if artist :
			artist.profile_photo = file
			artist.updated_date = today
			artist.save()
			
			im=Image.open(artist.profile_photo)
			
			exifData = {}
			exif_data = im._getexif()
			if exif_data:
				for tag, value in exif_data.items():
					decodedTag = ExifTags.TAGS.get(tag, tag)
					exifData[decodedTag] = value		
			
				if exifData :
					if 'Orientation' in exifData:
						if exifData['Orientation'] == 6:
							im.rotate(90)
						if exifData['Orientation'] == 3:
							im.rotate(180)
						if exifData['Orientation'] == 8:
							im.rotate(270)
				
			buffered = BytesIO()
			im.save(buffered, format='JPEG')
			img_data = buffered.getvalue()
			img_str = base64.b64encode(img_data)						

	return HttpResponse(img_str)

@csrf_exempt
def validate_url_name(request):
	
	url = request.POST.get('url_name', '')
	artist_id = request.POST.get('artist_id', '')
	
	if url == '':
		return JsonResponse( {'ret_msg': "Url name can't be blank"})
		
	if url:		
		if re.search("^[a-zA-Z0-9_-]+$", url) is None:
			return JsonResponse( {'ret_msg': "The webpage URL you entered is invalid. It can only contain alphabets, number, '-' & '_' and no blanks spaces are allowed."})

	artist = Artist.objects.filter(url_name = url).exclude(artist_id = artist_id)
	
	if artist:
		return JsonResponse( {'ret_msg': "This URL is already taken. Please choose another URL."})
	
	a = Artist.objects.filter(artist_id = artist_id).update(url_name = url)
	
	return JsonResponse({'ret_msg': "SUCCESS"})

@csrf_exempt
@is_artist
def save_artist_profile(request):
	if request.method == 'POST':
		artist_id = request.POST.get("artist_id", "")
		mode = request.POST.get("mode", "")
		profile_name = request.POST.get("profile_name", "")
		url_name = request.POST.get("url_name", "")
		tag_line = request.POST.get("tag_line", "")
		profile = request.POST.get("profile", "")
		a1 = request.POST.get("a1", "")
		a2 = request.POST.get("a2", "")
		a3 = request.POST.get("a3", "")
		a4 = request.POST.get("a4", "")
		a5 = request.POST.get("a5", "")

		e1 = request.POST.get("e1", "")
		e2 = request.POST.get("e2", "")
		e3 = request.POST.get("e3", "")
		e4 = request.POST.get("e4", "")
		e5 = request.POST.get("e5", "")
		
		achievements = ''
		if a1:
			achievements = achievements + a1
		if a2:
			achievements = achievements + '<br />'+ a2
		if a3:
			achievements = achievements + '<br />'+ a3
		if a4:
			achievements = achievements + '<br />'+ a4
		if a5:
			achievements = achievements + '<br />'+ a5

		events = ''
		if e1:
			events = events + e1
		if e2:
			events = events + '<br />'+ e2
		if e3:
			events = events + '<br />'+ e3
		if e4:
			events = events + '<br />'+ e4
		if e5:
			events = events + '<br />'+ e5

		e1 = request.POST.get("#e1", "")
		e2 = request.POST.get("#e2", "")
		e3 = request.POST.get("#e3", "")
		e4 = request.POST.get("#e4", "")
		e5 = request.POST.get("#e5", "")			

		if request.user.is_authenticated:
			try:
				artist = Artist.objects.get(artist_id = artist_id)
			except Artist.DoesNotExist:
				artist = None

			if mode == 'NEXT':
				if not profile_name:
					return JsonResponse({'ret_msg': "Your display name can't be blank"})					
				if not url_name:
					return JsonResponse({'ret_msg': "Your url name can't be blank. this become part of the url of your webpage on our website."})
				if not profile:
					return JsonResponse({'ret_msg': "Please include a few words about yourself. This will be displayed on your webpage."})					

			
			artist.profile_name = profile_name
			artist.url_name = url_name
			artist.artist_profile = profile
			artist.profile_tagline = tag_line
			artist.artist_showcase1_name = 'ACHIEVEMENTS'
			artist.artist_showcase1 = achievements
			artist.artist_showcase2_name = 'EVENTS'
			artist.artist_showcase2 = events
			
			artist.save()
		else:
			return JsonResponse({'ret_msg': "FAILURE"})

		return JsonResponse({'ret_msg': "SUCCESS"})
	else:
		return JsonResponse({'ret_msg': "FAILURE"})		
	

@is_artist
def upload_art(request, part_number=None):
	today = datetime.date.today()
	artist = {}
	artwork = {}
	if request.user.is_authenticated:
		try:
			user = User.objects.get(username = request.user)
			artist = Artist.objects.get(user = user)
		except User.DoesNotExist:
			user = None
		except Artist.DoesNotExist:
			artist = None
	if artist is None:
		return render(request, "artist/upload_artwork.html", {})

	medium_list = Original_art.MEDIUM
	surface_list = Original_art.SURFACE
	img_type_list = Original_art.IMAGE_TYPE
	category_list = Stock_image_category.objects.all().order_by('name')

	if request.POST:
		if "SAVE_DRAFT" in request.POST:
			save_draft = True
		else:
			save_draft = False
			
		if "SUBMIT_ARTWORK" in request.POST:
			submit_artwork = True
		else:
			submit_artwork = False
	else:
		submit_artwork = False
		save_draft = False

	import pdb
	pdb.set_trace()
		
		
	if save_draft or submit_artwork :
		product_id = request.POST.get("product_id", "")
		file = request.FILES.get('file')
		art_type = request.POST.get("art_type", "")
		title = request.POST.get("title", "")
		category = request.POST.get("category", "")
		art_width = request.POST.get("art_width", "")
		art_height = request.POST.get("art_height", "")
		medium = request.POST.get("medium", "")
		surface_description = request.POST.get("surface_description", "")
		art_print_option = request.POST.get("art_print_option", "")
		original_art_price = request.POST.get("original_art_price", "")
		keywords = request.POST.get("keywords", "")
		
	else:	
		if part_number:
			artwork = Artist_art_view.objects.filter(part_number = part_number)
		
	return render(request, "artist/upload_artwork.html", {'artist':artist, 'medium_list': medium_list, 'artwork': artwork,
		'surface_list': surface_list, 'img_type_list': img_type_list, 'product_id': product_id, 'category_list': category_list})
	

def save_art(request):
	today = datetime.date.today()
	art = {}
	if request.method == 'POST':
		from PIL import Image, ExifTags
		from io import BytesIO
		import base64

		file = request.FILES.get('file')
		session_id = request.session.session_key
		user = None
		
		if request.user.is_authenticated:
			try:
				user = User.objects.get(username = request.user)
				artist = Artist.objects.get(user = user)
			except User.DoesNotExist:
				user = None
			except Artist.DoesNotExist:
				artist = None
		else:
			return render(request, "artist/show_original_art.html", {'art':art})

		if artist :
		
			art = Original_art()
			
			IMAGE_TYPE = (
				('ART', 'Art Work'),
				('PHT', 'Photograph'),
			)
			MEDIUM = (
				('OIL', 'Oil'),
				('ACR', 'Acrylic'),
				('WTR', 'Water Color'),
				('GOU', 'Gouache'),
				('INK', 'Ink'),
				('PEN', 'Pen'),
				('PST', 'Pastel'),
				('PNC', 'Pencil'),
				('COL', 'Charcoal'),
			)
			SURFACE = (
				('CVS', 'Canvas'),
				('PPR', 'Paper'),
				('FAB', 'Fabric'),	
				('GLS', 'Glass'),	
				('WOD', 'Wood'),	
			)
			#product_id = 
			art.product_type = 'ORIGINAL-ART'
			art.name = name
			description = description
			price = price
			available_on = None
			part_number = part_number
			is_published = False
			seo_description = None
			seo_title  = None
			charge_taxes = True
			featured = False
			has_variants = False
			aspect_ratio = aspect_ratio
			image_type = image_type
			orientation = orientation
			max_width = max_width
			max_height = max_height
			min_width = min_width
			publisher = '0001'
			artist = artist.artist_id
			colors = color
			key_words = key_words
			url = url
			thumbnail_url = thumbnail_url
			high_resolution_url = high_resolution_url
			art_width = art_width
			art_height = art_height
			art_medium = art_medium
			art_surface = art_surface
			art_surface_desc = art_surface_desc
			category_disp_priority = None
			art_print_allowed = art_print_allowed
			original_art_price = original_art_price
			available_qty = available_qty
			sold_qty = none
			stock_image = stock_image	
	#	artist.profile_photo = file
		art.save()
		
		im=Image.open(artist.profile_photo)
			

	return render(request, "artist/show_original_art.html", {'art':art})
	