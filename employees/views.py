from django.db.models import Avg, Prefetch, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from employees.forms import EmployeeCreateForm, EmployeeDeleteForm, EmployeeEditForm
from employees.models import Employee
from reviews.forms import EmployeeReviewCreateForm, EmployeeReviewEditForm
from reviews.models import EmployeeReview
from restaurants.models import Restaurant


class EmployeesListView(ListView):
    model = Employee
    context_object_name = 'employees'
    template_name = 'employees/list.html'
    paginate_by = 12
    paginate_orphans = 5

    def get_queryset(self):
        queryset = super().get_queryset().select_related('restaurant').annotate(
            avg_rating=Avg('reviews__rating')
        )
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
            )
        selected_positions = self.request.GET.getlist('position')
        valid_positions = {value for value, _label in Employee.PositionChoices.choices}
        selected_positions = [position for position in selected_positions if position in valid_positions]
        if selected_positions:
            queryset = queryset.filter(position__in=selected_positions)
        return queryset.order_by('first_name', 'last_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        valid_positions = {value for value, _label in Employee.PositionChoices.choices}
        context.update({
            'search_query': self.request.GET.get('q', '').strip(),
            'position_choices': Employee.PositionChoices.choices,
            'selected_positions': [position for position in self.request.GET.getlist('position') if position in valid_positions],
        })
        return context


class EmployeeReviewsListView(ListView):
    model = EmployeeReview
    context_object_name = 'employee_reviews'
    template_name = 'employees/reviews_list.html'
    paginate_by = 12
    paginate_orphans = 5

    def get_queryset(self):
        queryset = super().get_queryset().select_related('employee', 'employee__restaurant')
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(employee__first_name__icontains=search_query)
                | Q(employee__last_name__icontains=search_query)
            )
        flagged = self.request.GET.get('flagged', '')
        if flagged == 'flagged':
            queryset = queryset.filter(is_flagged=True)
        elif flagged == 'normal':
            queryset = queryset.filter(is_flagged=False)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_query': self.request.GET.get('q', '').strip(),
            'selected_flagged': self.request.GET.get('flagged', ''),
        })
        return context


class EmployeesDetailsView(DetailView):
    model = Employee
    context_object_name = 'employee'
    template_name = 'employees/details.html'

    def get_queryset(self):
        review_queryset = EmployeeReview.objects.order_by('-created_at')
        return super().get_queryset().select_related('restaurant').annotate(
            avg_rating=Avg('reviews__rating')
        ).prefetch_related(Prefetch('reviews', queryset=review_queryset, to_attr='team_reviews'))


class EmployeeReviewDetailView(DetailView):
    model = EmployeeReview
    context_object_name = 'review'
    template_name = 'reviews/employee_review_details.html'

    def get_queryset(self):
        return super().get_queryset().select_related('employee', 'employee__restaurant')


class EmployeesCreateView(CreateView):
    model = Employee
    form_class = EmployeeCreateForm
    context_object_name = 'employee'
    template_name = 'employees/create.html'
    success_url = reverse_lazy('employees-list')

    def get_success_url(self):
        if self.object.restaurant_id:
            return reverse('restaurant-detail', kwargs={'slug': self.object.restaurant.slug or self.object.restaurant.pk})
        return super().get_success_url()

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


class EmployeeReviewCreateView(CreateView):
    model = EmployeeReview
    form_class = EmployeeReviewCreateForm
    template_name = 'reviews/employee_review_create.html'
    context_object_name = 'review'

    def get_employee(self):
        return get_object_or_404(Employee, pk=self.kwargs['employee_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = self.get_employee()
        return context

    def form_valid(self, form):
        form.instance.employee = self.get_employee()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('employee-detail', kwargs={'pk': self.object.employee_id})


class EmployeeReviewEditView(UpdateView):
    model = EmployeeReview
    form_class = EmployeeReviewEditForm
    template_name = 'reviews/employee_review_edit.html'
    context_object_name = 'review'

    def get_queryset(self):
        return super().get_queryset().select_related('employee')

    def get_success_url(self):
        return reverse('employee-detail', kwargs={'pk': self.object.employee_id})


class EmployeeReviewDeleteView(DeleteView):
    model = EmployeeReview
    template_name = 'reviews/employee_review_delete.html'
    context_object_name = 'review'

    def get_queryset(self):
        return super().get_queryset().select_related('employee')

    def get_success_url(self):
        return reverse('employee-detail', kwargs={'pk': self.object.employee_id})


class EmployeesDeleteView(DeleteView):
    model = Employee
    form_class = EmployeeDeleteForm
    context_object_name = 'employee'
    template_name = 'employees/delete.html'
    success_url = reverse_lazy('employees-list')


class EmployeesEditView(UpdateView):
    model = Employee
    form_class = EmployeeEditForm
    context_object_name = 'employee'
    template_name = 'employees/edit.html'
    success_url = reverse_lazy('employees-list')