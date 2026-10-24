from django.db.models import Avg, Prefetch, Q
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from employees.models import Employee
from restaurants.forms import RestaurantCreateForm, RestaurantEditForm, CreatePerkForm
from restaurants.mixins import RestaurantLookupMixin
from restaurants.models import Perks, Restaurant
from reviews.models import Review

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

        selected_cuisine = self.request.GET.getlist('cuisine')
        valid_cuisines = {value for value, _label in Restaurant.TypeChoices.choices}
        selected_cuisines = [value for value in selected_cuisine if value in valid_cuisines]
        if selected_cuisines:
            queryset = queryset.filter(cuisine_type__in=selected_cuisines)

        selected_perks = self.request.GET.getlist('perks')
        if selected_perks:
            queryset = queryset.filter(perks__id__in=selected_perks).distinct()

        return queryset.order_by('name')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perks = Perks.objects.order_by('name')

        for restaurant in context['restaurants']:
            restaurant.detail_url = RestaurantDetailView.get_absolute_url(restaurant)
        selected_cuisines = [cuisine for cuisine in self.request.GET.getlist('cuisine')]

        context.update({
            'active_perks': perks,
            'selected_perks': [perk_id for perk_id in self.request.GET.getlist('perks')],
            'search_query': self.request.GET.get('q', '').strip(),
            'cuisine_choices': Restaurant.TypeChoices.choices,
            'selected_cuisines': selected_cuisines,
        })
        return context


class RestaurantDetailView(RestaurantLookupMixin, DetailView):
    model = Restaurant
    template_name = 'restaurants/details.html'
    context_object_name = 'restaurant'

    @staticmethod
    def get_absolute_url(restaurant):
        identifier = restaurant.slug or restaurant.pk
        return reverse('restaurant-detail', kwargs={'slug': identifier})

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
        employees = self.object.working_employees
        rated_employees = [employee.avg_rating for employee in employees if employee.avg_rating is not None]
        team_avg_rating = sum(rated_employees) / len(rated_employees) if rated_employees else None
        context.update({
            'reviews': reviews,
            'review_count': len(reviews),
            'employee_count': len(employees),
            'rated_employee_count': len(rated_employees),
            'team_avg_rating': team_avg_rating,
        })
        return context


class RestaurantCreateView(CreateView):
    model = Restaurant
    template_name = 'restaurants/create.html'
    form_class = RestaurantCreateForm
    success_url = reverse_lazy('restaurants-list')



class RestaurantUpdateView(RestaurantLookupMixin, UpdateView):
    model = Restaurant
    form_class = RestaurantEditForm
    success_url = reverse_lazy('restaurants-list')
    def get_template_names(self):
        return ['restaurants/edit.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant_url'] = RestaurantDetailView.get_absolute_url(self.object)
        return context

class RestaurantDeleteView(RestaurantLookupMixin, DeleteView):
    model = Restaurant
    success_url = reverse_lazy('restaurants-list')
    def get_template_names(self):
        return ['restaurants/delete.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant_url'] = RestaurantDetailView.get_absolute_url(self.object)
        return context



class CreatePerkView(CreateView):
    model = Perks
    form_class = CreatePerkForm
    template_name = 'restaurants/perk_create.html'
    success_url = reverse_lazy('restaurants-list')