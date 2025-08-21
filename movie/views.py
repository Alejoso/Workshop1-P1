from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
# Create your views here.

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html' , {'searchTerm' : searchTerm , 'movies' : movies , 'name' : "Alejandro Tirado Ramírez"})

def about(request):
    return render(request , 'about.html')

def statistics_view(request):
    matplotlib.use('Agg')

    # -------------------- Gráfico por año --------------------
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        movie_counts_by_year[year] = movies_in_year.count()

    plt.bar(range(len(movie_counts_by_year)), movie_counts_by_year.values())
    plt.title('Movies per Year')
    plt.xticks(range(len(movie_counts_by_year)), movie_counts_by_year.keys(), rotation=90)
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    year_graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()

    # -------------------- Gráfico por género --------------------
    genres = Movie.objects.values_list('genre', flat=True).distinct()

    movie_counts_by_genre = {}

    for genre_str in genres:
        if genre_str:
            # Tomar solo el primer género (separado por coma)
            first_genre = genre_str.split(',')[0].strip()
        else:
            first_genre = "None"

        # Contar películas cuyo primer género coincida
        movies_in_genre = Movie.objects.filter(genre__startswith=first_genre)
        movie_counts_by_genre[first_genre] = movies_in_genre.count()

    # Crear gráfico
    plt.bar(range(len(movie_counts_by_genre)), movie_counts_by_genre.values())
    plt.title('Movies per First Genre')
    plt.xticks(range(len(movie_counts_by_genre)), movie_counts_by_genre.keys(), rotation=90)
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    genre_graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()


    return render(request, 'statistics.html', {
        'graphicYear': year_graphic,
        'graphicGenre': genre_graphic,
    })

def signup(request):
    email = request.GET.get('email')
    return render(request , 'signup.html' , {'email':email})