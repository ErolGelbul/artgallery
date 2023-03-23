from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ArtworkSerializer
from artworks.models import Artwork, Review, Tag


@api_view(["GET"])
def getRoutes(request):

    routes = [
        {"GET": "/api/artworks"},
        {"GET": "/api/artworks/id"},
        {"POST": "/api/artworks/id/vote"},
        {"POST": "/api/users/token"},
        {"POST": "/api/users/token/refresh"},
    ]
    return Response(routes)


@api_view(["GET"])
def getArtworks(request):
    artworks = Artwork.objects.all()
    serializer = ArtworkSerializer(artworks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getArtwork(request, pk):
    artwork = Artwork.objects.get(id=pk)
    serializer = ArtworkSerializer(artwork, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def artworkVote(request, pk):
    artwork = Artwork.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner=user,
        artwork=artwork,
    )

    review.value = data["value"]
    review.save()
    artwork.getVoteCount

    serializer = ArtworkSerializer(artwork, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
def removeTag(request):
    tagId = request.data["tag"]
    artworkId = request.data["aartwork"]

    artwork = Artwork.objects.get(id=artworkId)
    tag = Tag.objects.get(id=tagId)

    artwork.tags.remove(tag)

    return Response("Tag was deleted!")
