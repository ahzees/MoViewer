from Comments.models import Comments
from Movie.models import Movie, Category
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.generic import ListView
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from Movie.serializers import MovieSerializer
from rest_framework import status


class MovieAPIView(APIView):
    serializer_class = MovieSerializer

    def get(self, request):
        return Response(MovieSerializer(Movie.objects.all(), many=True).data, )

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TheMovieApiView(APIView):
    serializer_class = MovieSerializer

    def get_objects(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):
        movie = self.get_objects(pk=pk)
        return Response(MovieSerializer(movie).data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_objects(pk=kwargs.get('pk'))
        serializer = MovieSerializer(data=request.data,instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk):
        instance = self.get_objects(pk=pk)
        serializer = MovieSerializer(instance=instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


def all_films(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            if request.GET.get('category'):
                posts = Movie.objects.filter(category__name__in=request.GET.getlist('category'))
                return render(request, 'authentication/all_films.html',
                              {'posts': posts, 'categories': Category.objects.all()})
            if request.GET.get('q'):
                return render(request, 'authentication/all_films.html',
                              {'posts': Movie.objects.filter(name=request.GET.get('q')),
                               'categories': Category.objects.all()})
        posts = Movie.objects.order_by('pk')
        return render(request, 'authentication/all_films.html',
                      {'posts': posts, 'categories': Category.objects.all(),
                       'years': Movie.objects.all().values_list('year', flat=True).distinct('year')
                       })
    else:
        return redirect('home')


def movie(request, movie_slug):
    comments = Comments.objects.filter(movie__slug=movie_slug)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            x = Comments(user=request.user, movie=(Movie.objects.get(slug=movie_slug)),
                         comment=request.POST.get('comment'))
            x.save()
            return redirect(request.META.get('HTTP_REFERER'))
        except:
            return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'authentication/video.html',
                  {'item': Movie.objects.get(slug=movie_slug), 'comments': comments})


def like_movie(request, movie_slug):
    if request.user.dislike.filter(slug=movie_slug):
        request.user.dislike.remove(Movie.objects.get(slug=movie_slug))
    if not request.user.like.filter(slug=movie_slug):
        request.user.like.add(Movie.objects.get(slug=movie_slug))
        return redirect(request.META.get('HTTP_REFERER'))
    if request.user.like.filter(slug=movie_slug):
        request.user.like.remove(Movie.objects.get(slug=movie_slug))
        return redirect(request.META.get('HTTP_REFERER'))


def dislike_movie(request, movie_slug):
    if request.user.like.filter(slug=movie_slug):
        request.user.like.remove(Movie.objects.get(slug=movie_slug))
    if not request.user.dislike.filter(slug=movie_slug):
        request.user.dislike.add(Movie.objects.get(slug=movie_slug))
        return redirect(request.META.get('HTTP_REFERER'))
    if request.user.dislike.filter(slug=movie_slug):
        request.user.dislike.remove(Movie.objects.get(slug=movie_slug))
        return redirect(request.META.get('HTTP_REFERER'))


def category_movie(request, category_slug):
    posts = Movie.objects.filter(category__slug=category_slug)
    return render(request, 'authentication/all_films.html', {'posts': posts, 'categories': Category.objects.all()})


class FilterMovieView(ListView):
    model = Movie
    template_name = 'authentication/all_films.html'
    context_object_name = 'posts'
    extra_context = {'categories': Category.objects.all(),
                     'years': list(Movie.objects.all().values_list('year', flat=True).distinct('year__year'))}

    def get_queryset(self):
        posts = Movie.objects.filter(
            category__name__in=self.request.GET.getlist('category') or Movie.objects.all().values_list(
                'category__name'),
            year__year__in=self.request.GET.getlist('year') or Movie.objects.all().values_list('year__year')).distinct(
            'name')
        return posts
