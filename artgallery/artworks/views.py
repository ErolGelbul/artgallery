from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Artwork
from .forms import ArtworkForm, ReviewForm
from .utils import search_artworks, paginate_artworks


def artworks(request):
    artworks, search_query = search_artworks(request)
    custom_range, artworks = paginate_artworks(request, artworks, 6)

    context = {
        "artworks": artworks,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, "artworks/artworks.html", context)


def artwork(request, pk):
    artworkObj = Artwork.objects.get(id=pk)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.artwork = artworkObj
        review.owner = request.user.profile
        review.save()

        artworkObj.get_vote_count

        messages.success(request, "Your review was submitted!")
        return redirect("artwork", pk=artworkObj.id)

    return render(
        request, "artworks/single-artwork.html", {"artwork": artworkObj, "form": form}
    )


@login_required(login_url="login")
def createArtwork(request):
    profile = request.user.profile
    form = ArtworkForm()

    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            # 1:M
            artwork.owner = profile
            artwork.save()
            return redirect("account")

    context = {"form": form}
    return render(request, "artworks/artwork_form.html", context)


@login_required(login_url="login")
def updateArtwork(request, pk):
    profile = request.user.profile
    artwork = profile.artwork_set.get(id=pk)
    form = ArtworkForm(instance=artwork)

    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid():
            form.save()
            return redirect("account")

    context = {"form": form}
    return render(request, "artworks/artwork_form.html", context)


@login_required(login_url="login")
def deleteArtwork(request, pk):
    profile = request.user.profile
    artwork = profile.artwork_set.get(id=pk)
    if request.method == "POST":
        artwork.delete()
        return redirect("artworks")
    context = {"object": artwork}
    return render(request, "delete_template.html", context)
