import math

from django.core.paginator import Paginator





class ProblemPaginator(Paginator):
    def __init__(self, current_page, **kwargs):
        super().__init__(**kwargs)
        self.current_page = self._format_current_page(current_page)

    def _format_current_page(self, current_page):
        if isinstance(current_page, int) and current_page > 0 and current_page <= self.num_pages:
            return current_page
        return 1

    @property
    def page_range(self):
        if self.num_pages < 9:
            return super().page_range
        elif self.current_page - 4 < 1:
            return range(1, 10)
        elif self.current_page + 5 > self.num_pages:
            return range(self.num_pages-8, self.num_pages+1)
        else:
            return range(self.current_page - 4, self.current_page+5)


