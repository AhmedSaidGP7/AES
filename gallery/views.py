from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q


# Create your views here.

def index(request):
    query = request.GET.get('q', '')
    if query:
        artworks = ArtWork.objects.filter(
            Q(name__icontains=query) |
            Q(author__username__icontains=query) | 
             Q(author__first_name__icontains=query) |  # Search by first name
            Q(author__last_name__icontains=query) |   # Search by last name
            Q(material__icontains=query) |
            Q(art_type__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-date_created')  # Ensure ordering for the filtered queryset
    else:
        artworks = ArtWork.objects.all().order_by('-date_created')  # Explicit ordering for default query

    paginator = Paginator(artworks, 15)  # Show 15 artworks per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "gallery/index.html", {'page_obj': page_obj, 'query': query})


def artwork_detail(request, artwork_id):
    artwork = get_object_or_404(ArtWork, pk=artwork_id)
    images = ArtworkImage.objects.filter(artwork=artwork)
    return render(request, 'gallery/artwork_detail.html', {'artwork': artwork, 'images': images})



@login_required
def sell_artwork(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        art_type = request.POST['art_type']
        material = request.POST['material']
        height = request.POST['height']
        width = request.POST['width']
        length = request.POST.get('length', 0)  # optional field
        style = request.POST.get('style', '')  # optional field
        description = request.POST['description']
        main_img = request.FILES.get("main_image", False)


        # Create the ArtWork instance
        artwork = ArtWork.objects.create(
            name=name,
            price=price,
            art_type=art_type,
            material=material,
            height=height,
            width=width,
            length=length,
            style=style,
            description=description,
            author=request.user,
            main_img = main_img
        )

        # Handle multiple images
        images = request.FILES.getlist('image')
        for image in images:
            ArtworkImage.objects.create(
                artwork=artwork,
                image=image
            )
        return render(request, 'gallery/sell.html', 
        {
            "message": "Done"
        }) 
    return render(request, 'gallery/sell.html')




@login_required
def add_to_cart(request, artwork_id):
    artwork = get_object_or_404(ArtWork, pk=artwork_id)
    if artwork.availability != 'In Stock':
        messages.error(request, 'هذا العمل الفني غير متاح حاليا')
        return redirect('gallery:artwork_detail', artwork_id=artwork_id)
    
    cart_item, created = Cart.objects.get_or_create(user=request.user, artwork=artwork)
    if created:
        messages.success(request, 'تم اضافة العمل الفني بنجاح')
    else:
        messages.info(request, 'العمل الفني موجود في عربة التسوق بالفعل')
    return redirect('gallery:artwork_detail', artwork_id=artwork_id)

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.artwork.price * item.quantity for item in cart_items)
    vat = total_price * 0.14  # Calculate VAT at 14%
    shipping_fee = 50  # Set your shipping fee
    total_order = total_price + vat + shipping_fee

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'vat': vat,
        'shipping_fee': shipping_fee,
        'total_order': total_order
    }

    return render(request, 'gallery/cart.html', context)


@login_required
def remove_from_cart(request, artwork_id):
    artwork = get_object_or_404(ArtWork, pk=artwork_id)
    cart_item = Cart.objects.filter(user=request.user, artwork=artwork).first()
    if cart_item:
        cart_item.delete()
        messages.success(request, 'تمت إزالة العمل الفني من سلة التسوق بنجاح.')
    else:
        messages.error(request, 'لم يتم العثور على العمل الفني في سلة التسوق.')

    return redirect('gallery:cart')