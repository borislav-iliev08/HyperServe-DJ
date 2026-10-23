from django.db.models import Avg
from employees.models import Employee
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import TemplateView

from restaurants.models import Restaurant
from reviews.models import Review


def custom_404(request:HttpRequest,exception=None):
    return render(request, '404.html', status=404)


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        top_restaurants = Restaurant.objects.annotate(
            avg_rating=Avg('restaurant_reviews__rating')
        ).filter(avg_rating__isnull=False).order_by('-avg_rating')[:5]
        latest_reviews = Review.objects.select_related('restaurant').order_by('-created_at')[:5]
        top_chefs = Employee.objects.filter(position=Employee.PositionChoices.CH).annotate(
            avg_rating=Avg('reviews__rating')
        ).filter(avg_rating__isnull=False).order_by('-avg_rating', 'first_name', 'last_name')[:5]

        stats = {
            'total_restaurants': Restaurant.objects.count(),
            'total_reviews': Review.objects.count(),
        }

        context.update({
            'top_restaurants': top_restaurants,
            'latest_reviews': latest_reviews,
            'top_chefs': top_chefs,
            'stats': stats,
        })
        return context
