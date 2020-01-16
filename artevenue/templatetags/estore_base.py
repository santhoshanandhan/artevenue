from datetime import datetime
import datetime
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError, DatabaseError, Error
from django.db.models import Count
from django.contrib.auth.models import User

from artevenue.models import Ecom_site, Main_slider, New_arrival, Promotion, Menu, Stock_image_category
from artevenue.models import New_arrival_images, Promotion_images, Cart
from django.http import HttpResponse
from django.conf import settings

from django import template

today = datetime.date.today()

register = template.Library()
@register.inclusion_tag('artevenue/topbar.html')
def topbar(request , auth_user):
	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )
	if request:
		if request.user:
			return {'ecom_site':ecom, 'request':request, 'user': request.user, 'auth_user' : auth_user}
		else:
			return {'ecom_site':ecom, 'request':request, }
		
	else:
		return {'ecom_site':ecom}


@register.inclusion_tag('artevenue/artevenue_admin_menu.html')
def admin_menu(request):
	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )
	if request:
		if request.user:
			return {'ecom_site':ecom, 'request':request, 'user': request.user}	
		else:
			return {'ecom_site':ecom, 'request':request}
	else:
		return {'ecom_site':ecom, 'request':request}	
	
	
	
@register.inclusion_tag('artevenue/estore_menu_with_search.html')	
#@register.inclusion_tag('artevenue/estore_menu_two_lines.html')	
def menubar(request):

	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )
	
	#Level 0
	level0_menuitems = Menu.objects.filter(store = ecom, effective_from__lte = today, 
		effective_to__gte = today, level=0).order_by('sort_order')

	# Level 1
	level1_menuitems = Stock_image_category.objects.annotate(Count(
			'stock_image_stock_image_category')).filter(parent_id__isnull = True,
			stock_image_stock_image_category__count__gt = 1000).order_by('-stock_image_stock_image_category__count')

	level1_menuitems_original_art = Stock_image_category.objects.annotate(Count(
			'original_art_category')).filter(parent_id__isnull = True,
			original_art_category__count__gt = 0).order_by('-original_art_category__count')


	# Level 2
	level2_menuitems = Stock_image_category.objects.filter(parent_id__in = level1_menuitems)

	''' Get cart for total items in the cart '''
	if request:
		if request.session:
			sessionid = request.session.session_key
			if sessionid is None:
				request.session.create()
				sessionid = request.session.session_key		
	usercart = {}
	
	try:
		if request:
			if request.user:
				if request.user.is_authenticated:
					userid = User.objects.get(username = request.user)
					usercart = Cart.objects.get(user_id = userid, cart_status = "AC")
				else:
					if sessionid:
						usercart = Cart.objects.get(session_id = sessionid, cart_status = "AC")
	
	except Cart.DoesNotExist:
			usercart = {}
	
	return {'level0_menuitems':level0_menuitems, 
			'level1_menuitems':level1_menuitems,
			'level2_menuitems':level2_menuitems,
			'usercart':usercart,
			'level1_menuitems_original_art':level1_menuitems_original_art}


@register.inclusion_tag('artevenue/artevenue_text.html')	
def artevenue_text(request):
	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )

	if request:
		if request.user:
			return {'ecom_site':ecom, 'request':request, 'user': request.user}
		else:
			return {'ecom_site':ecom, 'request':request}
	else:
		return {'ecom_site':ecom}


@register.inclusion_tag('artevenue/why_artevenue_text.html')	
def why_artevenue_text():
	return {}

@register.inclusion_tag('artevenue/signup_banner.html')	
def signup_banner():
	return {}


@register.inclusion_tag('artevenue/footer.html')	
def site_footer(request):
	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )
	#Level 0
	level0_menuitems = Menu.objects.filter(store = ecom, effective_from__lte = today, 
		effective_to__gte = today, level=0).order_by('sort_order')

	# Level 1
	level1_menuitems = Stock_image_category.objects.annotate(Count(
			'stock_image_stock_image_category')).filter(parent_id__isnull = True,
			stock_image_stock_image_category__count__gt = 1000).order_by('-stock_image_stock_image_category__count')

	if request:
		if request.user:
			return {'ecom_site':ecom, 'request':request, 'user': request.user,
			'level0_menuitems':level0_menuitems, 'level1_menuitems':level1_menuitems,}
		else: 
			return {'ecom_site':ecom, 'request':request, 'level0_menuitems':level0_menuitems, 
			'level1_menuitems':level1_menuitems,}
	else:
		return {'ecom_site':ecom, 'level0_menuitems':level0_menuitems, 
			'level1_menuitems':level1_menuitems,}
		

@register.inclusion_tag('artevenue/copy_right.html')	
def copy_right(request):
	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )

	if request:
		if request.user:
			return {'ecom_site':ecom, 'request':request, 'user': request.user}
		else:
			return {'ecom_site':ecom, 'request':request}
	else:
		return {'ecom_site':ecom}

@register.inclusion_tag('artevenue/cart_update_message.html')	
def update_cart_message(result):
	return ({'result':result})

@register.inclusion_tag('artevenue/client_speak.html')	
def client_speak(request):
	ecom = get_object_or_404 (Ecom_site, store_id=settings.STORE_ID )

	return {}

@register.inclusion_tag('artevenue/referral.html')	
def show_referral():

	return{}
	
	