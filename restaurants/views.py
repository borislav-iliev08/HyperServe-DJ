from django.db.models import Avg, Prefetch, Q, Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from employees.models import Employee
from restaurants.forms import CreatePerkForm, RestaurantCreateForm, RestaurantEditForm
from restaurants.models import Perks, Restaurant
from reviews.models import EmployeeReview, Review


class RestaurantListView(ListView):
    model = Restaurant
    context_object_name = 'restaurants'
    paginate_by = 12
    paginate_orphans = 5

    def get_template_names(self):
        return ['restaurants/restaurants_list.html']

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

        if selected_cuisines:
            queryset = queryset.filter(cuisine_type__in=selected_cuisines)
        selected_perks = self.request.GET.getlist('perks')

        if selected_perks:
            queryset = queryset.filter(perks__id__in=selected_perks).distinct()

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'active_perks': Perks.objects.order_by('name'),
            'selected_perks': self.request.GET.getlist('perks'),
            'search_query': self.request.GET.get('q', '').strip(),
            'cuisine_choices': Restaurant.TypeChoices.choices,
            'selected_cuisines': self.request.GET.getlist('cuisine'),
        })
        return context


class RestaurantDetailView(DetailView):
    model = Restaurant
    context_object_name = 'restaurant'

    def get_template_names(self):
        return ['restaurants/details.html']

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        slug = self.kwargs.get('slug')
        if str(slug).isdigit():
            return get_object_or_404(queryset, pk=int(slug))
        return get_object_or_404(queryset, slug=slug)

    def get_queryset(self):
        employee_queryset = Employee.objects.annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('first_name', 'last_name')
        review_queryset = Review.objects.order_by('-created_at')
        return super().get_queryset().annotate(
            avg_rating=Avg('restaurant_reviews__rating')
        ).prefetch_related(
            'perks',
            Prefetch('restaurant_reviews', queryset=review_queryset, to_attr='restaurant_reviews_list'),
            Prefetch('employee_set', queryset=employee_queryset, to_attr='working_employees'),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = context['restaurant']
        reviews = restaurant.restaurant_reviews_list
        context['reviews'] = reviews
        context['review_count'] = len(reviews)
        context['employee_count'] = len(restaurant.working_employees)
        context['team_avg_rating'] = EmployeeReview.objects.filter(
            employee__restaurant=restaurant
        ).aggregate(avg_rating=Avg('rating'))['avg_rating']
        return context


class RestaurantCreateView(CreateView):
    model = Restaurant
    form_class = RestaurantCreateForm
    success_url = reverse_lazy('restaurants-list')
    def get_template_names(self):
        return ['restaurants/create.html']

class RestaurantUpdateView(UpdateView):
    model = Restaurant
    form_class = RestaurantEditForm
    success_url = reverse_lazy('restaurants-list')

    def get_template_names(self):
        return ['restaurants/edit.html']

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        slug = self.kwargs.get('slug')
        if str(slug).isdigit():
            return get_object_or_404(queryset, pk=int(slug))
        return get_object_or_404(queryset, slug=slug)


class RestaurantDeleteView(DeleteView):
    model = Restaurant
    success_url = reverse_lazy('restaurants-list')
    def get_template_names(self):
        return ['restaurants/delete.html']

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        slug = self.kwargs.get('slug')
        if str(slug).isdigit():
            return get_object_or_404(queryset, pk=int(slug))
        return get_object_or_404(queryset, slug=slug)


class CreatePerkView(CreateView):
    model = Perks
    form_class = CreatePerkForm
    success_url = reverse_lazy('home')

    def get_template_names(self):
        return ['perks/perk_create.html']


