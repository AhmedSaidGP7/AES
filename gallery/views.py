from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
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
            Q(material__icontains=query) |
            Q(art_type__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        artworks = ArtWork.objects.all()
    
    return render(request, "gallery/index.html", {'artworks': artworks, 'query': query})


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
