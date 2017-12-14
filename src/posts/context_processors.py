from .models import Category


def categories(request):
    categories = Category.objects.filter(sort__gt=0)
    return {"categories": categories}
