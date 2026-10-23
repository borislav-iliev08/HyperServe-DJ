from django.shortcuts import get_object_or_404


class RestaurantLookupMixin:
    def get_object(self, queryset=None):

        queryset = self.get_queryset()

        slug = self.kwargs.get('slug')
        if str(slug).isdigit():
            value = {'pk': int(slug)}
        else:
            value = {'slug': slug}

        return get_object_or_404(queryset, **value)