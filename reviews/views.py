from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from employees.forms import EmployeeCreateForm, EmployeeDeleteForm, EmployeeEditForm
from employees.models import Employee
from restaurants.models import Restaurant
from reviews.forms import ReviewCreateForm, ReviewEditForm
from reviews.models import Review


class ReviewListView(ListView):
    model = Review
    context_object_name = 'reviews'
    paginate_by = 12
    paginate_orphans = 5

    def get_template_names(self):
        return ['reviews/review_list.html']

    def get_queryset(self):
        query = super().get_queryset().select_related('restaurant')
        search_query = self.request.GET.get('q', '')
        if search_query:
            query = query.filter(
                Q(title__icontains=search_query) | Q(restaurant__name__icontains=search_query)
            )

        flagged = self.request.GET.get('flagged', '')
        if flagged == 'flagged':
            query = query.filter(is_flagged=True)
        elif flagged == 'normal':
            query = query.filter(is_flagged=False)

        return query.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_query': self.request.GET.get('q', ''),
            'selected_flagged': self.request.GET.get('flagged', ''),
        })
        return context


class ReviewDetailView(DetailView):
    model = Review
    context_object_name = 'review'

    def get_template_names(self):
        return ['reviews/details.html']


class ReviewDeleteView(DeleteView):
    model = Review
    context_object_name = 'review'
    success_url = reverse_lazy('reviews-list')

    def get_template_names(self):
        return ['reviews/delete.html']


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewCreateForm
    context_object_name = 'review'
    success_url = reverse_lazy('reviews-list')

    def get_template_names(self):
        return ['reviews/create.html']

    def get_selected_restaurant(self):
        restaurant_id = self.request.GET.get('restaurant', '')
        if not restaurant_id.isdecimal():
            return None
        return Restaurant.objects.filter(pk=restaurant_id).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = self.get_selected_restaurant()
        return context

    def form_valid(self, form):
        form.instance.restaurant = self.get_selected_restaurant()
        return super().form_valid(form)


class ReviewEditView(UpdateView):
    model = Review
    form_class = ReviewEditForm
    context_object_name = 'review'
    success_url = reverse_lazy('reviews-list')

    def get_template_names(self):
        return ['reviews/edit.html']


class EmployeesReviewsListView(ListView):
    model = Employee
    context_object_name = 'employee'
    paginate_by = 12
    paginate_orphans = 5

    def get_template_names(self):
        return ['employees/reviews_list.html']

    def get_queryset(self):
        query = super().get_queryset().select_related('restaurant')
        search_query = self.request.GET.get('q', '')
        if search_query:
            query = query.filter(title__icontains=search_query)

        return query.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_query': self.request.GET.get('q', '')
        })
        return context


class EmployeesReviewsDetailsView(DetailView):
    model = Employee
    context_object_name = 'employee'

    def get_template_names(self):
        return ['reviews/employee_review_details.html']


class EmployeesReviewsCreateView(CreateView):
    model = Employee
    form_class = EmployeeCreateForm
    context_object_name = 'employee'

    def get_template_names(self):
        return ['reviews/employee_review_create.html']


class EmployeesReviewsDeleteView(DeleteView):
    model = Employee
    form_class = EmployeeDeleteForm
    context_object_name = 'employee'

    def get_template_names(self):
        return ['reviews/emoployee_review_delete.html']


class EmployeesReviewsEditView(UpdateView):
    model = Employee
    form_class = EmployeeEditForm
    context_object_name = 'employee'

    def get_template_names(self):
        return ['reviews/employee_review_edit.html']