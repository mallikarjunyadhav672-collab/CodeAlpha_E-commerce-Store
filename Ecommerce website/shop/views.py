from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Cart, CartItem


def index(request):
    return render(request, 'index.html')


def shop_list(request):
    qs = Product.objects.all().order_by('id')
    cat = request.GET.get('cat')
    if cat and cat != 'all':
        qs = qs.filter(category=cat)
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 8)  # 8 products per page
    page_obj = paginator.get_page(page)
    return render(request, 'shop_list.html', {'page_obj': page_obj, 'cat': cat})


def collections(request):
    # collections with representative images and sample products
    cols_def = [
        {'key': 'fashion', 'name': 'Summer Edit', 'count': Product.objects.filter(category='fashion').count()},
        {'key': 'electronics', 'name': 'Luxury Tech', 'count': Product.objects.filter(category='electronics').count()},
        {'key': 'home', 'name': 'Home Luxe', 'count': Product.objects.filter(category='home').count()},
        {'key': 'beauty', 'name': 'Beauty & Grooming', 'count': Product.objects.filter(category='beauty').count()},
    ]
    cols = []
    for i, c in enumerate(cols_def, start=1):
        # use picsum seeded image to ensure availability
        img = f'https://picsum.photos/seed/collection{i}/900/600'
        samples = list(Product.objects.filter(category=c['key']).order_by('-rating')[:4])
        cols.append({'key': c['key'], 'name': c['name'], 'count': c['count'], 'img': img, 'samples': samples})
    # gallery images for the collections page (14 images)
    gallery_images = [f'https://picsum.photos/seed/collection_gallery_{i}/400/300' for i in range(1,15)]
    return render(request, 'collections.html', {'collections': cols, 'gallery_images': gallery_images})



def about(request):
    return render(request, 'about.html')


@csrf_exempt
def newsletter_api(request):
    # accept POST with JSON { email: '...' } or form-encoded
    if request.method != 'POST':
        return JsonResponse({'error': 'method not allowed'}, status=405)
    try:
        import json
        data = json.loads(request.body.decode('utf-8') or '{}')
        email = data.get('email')
    except Exception:
        email = request.POST.get('email')
    if not email:
        return JsonResponse({'error': 'missing email'}, status=400)
    from .models import NewsletterEmail
    obj, created = NewsletterEmail.objects.get_or_create(email=email)
    return JsonResponse({'ok': True, 'created': created})


def products_api(request):
    qs = Product.objects.all().order_by('id')
    return JsonResponse({'products': [p.to_dict() for p in qs]})


@csrf_exempt
def cart_api(request):
    # DB-backed cart (scoped to session_key)
    # ensure session exists
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    cart_obj, _ = Cart.objects.get_or_create(session_key=session_key)

    if request.method == 'GET':
        return JsonResponse({'cart': cart_obj.items_mapping()})

    if request.method == 'POST':
        import json
        data = json.loads(request.body.decode('utf-8') or '{}')
        pid = data.get('id')
        try:
            qty = int(data.get('qty', 1))
        except Exception:
            qty = 1
        if pid is None:
            return JsonResponse({'error': 'missing id'}, status=400)

        # ensure product exists
        try:
            prod = Product.objects.get(pk=pid)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'invalid product id'}, status=400)

        ci, created = CartItem.objects.get_or_create(cart=cart_obj, product=prod, defaults={'qty': max(0, qty)})
        if not created:
            ci.qty = ci.qty + qty
            if ci.qty <= 0:
                ci.delete()
            else:
                ci.save()
        # if created and qty <=0, remove
        if created and ci.qty <= 0:
            ci.delete()

        return JsonResponse({'cart': cart_obj.items_mapping()})


@csrf_exempt
def wishlist_api(request):
    wl = set(request.session.get('wishlist', []))
    if request.method == 'GET':
        return JsonResponse({'wishlist': list(wl)})
    if request.method == 'POST':
        import json
        data = json.loads(request.body.decode('utf-8') or '{}')
        pid = str(data.get('id'))
        if pid in wl:
            wl.remove(pid)
        else:
            wl.add(pid)
        request.session['wishlist'] = list(wl)
        return JsonResponse({'wishlist': list(wl)})
