from django.db.models import Avg, Prefetch, Q
from django.http import HttpRequest
from django.shortcuts import  render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from employees.models import Employee
from restaurants.forms import RestaurantCreateForm, RestaurantEditForm
from restaurants.mixins import RestaurantLookupMixin
from restaurants.models import Perks, Restaurant
from reviews.models import Review


def index(request: HttpRequest):
    return render(request, 'base/base.html')


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/restaurants_list.html'
    context_object_name = 'restaurants'
    paginate_orphans = 5
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            avg_rating=Avg('restaurant_reviews__rating')
        ).prefetch_related('perks')
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(cuisine_type__icontains=search_query)
            )

        selected_cuisines = self.request.GET.getlist('cuisine')
        valid_cuisines = {value for value, _label in Restaurant.TypeChoices.choices}
        selected_cuisines = [value for value in selected_cuisines if value in valid_cuisines]
        if selected_cuisines:
            queryset = queryset.filter(cuisine_type__in=selected_cuisines)

        selected_perks = self.request.GET.getlist('perks')
        if selected_perks:
            queryset = queryset.filter(perks__id__in=selected_perks).distinct()
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perks = Perks.objects.order_by('name')
        valid_perk_ids = {str(perk_id) for perk_id in perks.values_list('id', flat=True)}
        selected_cuisines = [cuisine for cuisine in self.request.GET.getlist('cuisine')]

        context.update({
            'active_perks': perks,
            'selected_perks': [
                perk_id for perk_id in self.request.GET.getlist('perks')
                if perk_id in valid_perk_ids
            ],
            'search_query': self.request.GET.get('q', '').strip(),
            'cuisine_choices': Restaurant.TypeChoices.choices,
            'selected_cuisines': selected_cuisines,
        })
        return context





class RestaurantDetailView(RestaurantLookupMixin, DetailView):
    model = Restaurant
    template_name = 'restaurants/details.html'
    context_object_name = 'restaurant'

    def get_queryset(self):
        review_queryset = Review.objects.order_by('-created_at')
        employee_queryset = Employee.objects.annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('position', 'first_name', 'last_name')
        return super().get_queryset().annotate(
            avg_rating=Avg('restaurant_reviews__rating')
        ).prefetch_related(
            'perks',
            Prefetch('restaurant_reviews', queryset=review_queryset),
            Prefetch('employee_set', queryset=employee_queryset, to_attr='working_employees'),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = list(self.object.restaurant_reviews.all())
        context.update({'reviews': reviews, 'review_count': len(reviews)})
        return context


class RestaurantCreateView(CreateView):
    model = Restaurant
    form_class = RestaurantCreateForm
    success_url = reverse_lazy('restaurants-list')
    def get_template_names(self):
        return ['restaurants/create.html']

class RestaurantUpdateView(RestaurantLookupMixin, UpdateView):
    model = Restaurant
    form_class = RestaurantEditForm
    success_url = reverse_lazy('restaurants-list')
    def get_template_names(self):
        return ['restaurants/edit.html']

class RestaurantDeleteView(RestaurantLookupMixin, DeleteView):
    model = Restaurant
    success_url = reverse_lazy('restaurants-list')
    def get_template_names(self):
        return ['restaurants/delete.html']