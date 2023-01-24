from rest_framework.pagination import LimitOffsetPagination

from settings import MAX_PAGINATION_LIMIT


class LimitOffsetPaginationParamsWithoutParams(LimitOffsetPagination):
    max_limit = MAX_PAGINATION_LIMIT

    def get_limit(self, request):
        limit = super().get_limit(request)
        return limit or self.count

    def paginate_queryset(self, queryset, request, view=None):
        self.count = self.get_count(queryset)
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset : self.offset + self.limit])
