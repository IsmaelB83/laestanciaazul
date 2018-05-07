# coding=utf-8
# decoding=utf-8
# Python imports
# Django imports
from django.apps import apps
from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.template.defaultfilters import slugify
# Third party app imports
# Local app imports
import gallery
from utilidades import PaginatorWithPageRange
from .forms import PostForm, PostFormEdit
from .models import Post, PostImage, PostCategory, PostComment, PostArchive, add_log_archive, add_log_search, PostImageSmall
from discuss.models import Comment
from gallery.models import Image
from user.models import UserProfile
from category.models import Category
from like.models import PostLike


def index_view(request):
    # Se obtienen los primeros 15 posts, y se crea un paginador de 5 posts por pagina
    posts_all = Post.objects.filter(status='PB').order_by('-published_date')[:15]
    paginator = PaginatorWithPageRange(posts_all, 5, 5)
    page_request_var = 'page'
    page = request.GET.get('page')
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        messages.warning(request, u'Página indicada fuera de rango')
        return redirect('blog:index')
    # Los posts tipo carta son siempre 3. Ahora mismo se muestran los 3 más recientes
    posts_cards = Post.objects.filter(status='PB').order_by('-published_date')[:3]
    # Se devuelven los 5 postst más populares. Ahora mismo son los que más comentarios tienen
    posts_popular = Post.objects.filter(status='PB').annotate(comment_count=Count('postcomment__comment')).order_by('-comment_count')[:4]
    # Se devuelven los 5 últimos comentarios de la web
    comments_recent = PostComment.objects.order_by('-comment__timestamp')[:5]
    # Se devuelven las 12 últimas imagenes cargadas
    pictures_recent = PostImageSmall.objects.filter(post__status='PB').order_by('-image__timestamp')[:20]
    # Se genera el contexto con toda la información y se renderiza
    context = {
        'posts': posts_page,
        'posts_cards': posts_cards,
        'posts_popular': posts_popular,
        'comments_recent': comments_recent,
        'pictures_recent': pictures_recent,
        'page_request': page_request_var,
    }
    return render(request, 'index.html', context)


def archive_view(request, year, month):
    # Se generan todos los posts para el filtrado especificado
    if 1999 < int(year) < 2035:
        if 0 < int(month) < 13:
            posts_filtered = Post.objects.filter(status='PB', published_date__year=int(year), published_date__month=int(month))
        elif int(month) == 13:
            posts_filtered = Post.objects.filter(status='PB', published_date__year=int(year))
        else:
            messages.error(request, 'El mes indicado es incorrecto')
            return redirect('blog:index')
    else:
        messages.error(request, u'El año indicado es incorrecto')
        return redirect('blog:index')
    # Se genera el paginador para esos posts
    paginator = PaginatorWithPageRange(posts_filtered, 12, 5)
    page_request_var = 'page'
    page = request.GET.get('page')
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    # Se prepara la tabla para navegación por el archivo
    years_list = []
    months_list = []
    for i in PostArchive.objects.values('year').distinct():
        years_list.append(i['year'])
        aux_list = []
        j = 13
        while j > 0:
            if j == 13:
                cont = PostArchive.objects.filter(year=i['year']).aggregate(Sum('posts'))
                aux_list.append(cont['posts__sum'])
            else:
                if PostArchive.objects.filter(year=i['year'], month=j).exists():
                    aux = PostArchive.objects.get(year=i['year'], month=j)
                    aux_list.append(aux.posts)
                else:
                    aux_list.append(0)
            j -= 1
        months_list.append(aux_list)
    archivo = zip(years_list, months_list)
    # Añadir log
    if request.user.is_authenticated:
        add_log_archive(request.user, year + "/" + month)

    # Se genera el contexto y se renderiza
    context = {
        'year': int(year),
        'month': int(month),
        'archivo': archivo,
        'posts': posts_page,
        'page_request': page_request_var
    }
    return render(request, 'archive.html', context)


def search_view(request, filter):
    # Se generan todos los posts para el filtrado especificado
    filter = filter.replace('-', ' ')
    if filter == '_not_published_':
        if not request.user.is_authenticated:
            messages.error(request, 'Buen intento :). Debes loguearte para editar tus post en draft o inactivos')
            return redirect('blog:index')
        if request.user.userprofile:
            posts_filtered = Post.objects.filter(status__in=['IN', 'DR'], author=request.user.userprofile).order_by('-published_date')
    else:
        posts_filtered = Post.objects.filter(status='PB', title__icontains=filter).order_by('-published_date')
    # Se genera el paginador para esos posts
    paginator = PaginatorWithPageRange(posts_filtered, 12, 5)
    page_request_var = 'page'
    page = request.GET.get('page')
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    # Se devuelven los 5 postst más populares. Ahora mismo son los que más comentarios tienen
    posts_popular = Post.objects.filter(status='PB').annotate(comment_count=Count('postcomment__comment')).order_by('-comment_count')[:4]
    # Se devuelven los 5 últimos comentarios de la web
    comments_recent = PostComment.objects.order_by('-comment__timestamp')[:5]
    # Se devuelven las 12 últimas imagenes cargadas
    pictures_recent = PostImageSmall.objects.filter(post__status='PB').order_by('-image__timestamp')[:12]
    # Añadir log
    if request.user.is_authenticated:
        add_log_search(request.user, filter)

    # Se genera el contexto y se renderiza
    context = {
        'filter': filter,
        'posts': posts_page,
        'posts_popular': posts_popular,
        'comments_recent': comments_recent,
        'pictures_recent': pictures_recent,
        'page_request': page_request_var,
    }
    return render(request, 'search.html', context)


def gallery_view(request):
    # Se recuperan todas las imagenes
    post_images_all = PostImageSmall.objects.filter(post__status='PB').order_by('-image__timestamp')
    # Se genera el paginador para esos posts
    paginator = PaginatorWithPageRange(post_images_all, 18, 5)
    page_request_var = 'page'
    page = request.GET.get('page')
    try:
        post_images_page = paginator.page(page)
    except PageNotAnInteger:
        post_images_page = paginator.page(1)
    except EmptyPage:
        messages.warning(request, u'Página indicada fuera de rango')
        return redirect('blog:gallery')
    # Se genera el log
    if request.user.is_authenticated:
        gallery.models.add_log(request.user)

    # Se genera el contexto y se renderiza
    context = {
        'post_images': post_images_page,
        'page_request': page_request_var
    }
    return render(request, 'gallery.html', context)


def category_view(request, id):
    # Se obtienen la categoria pasada como parametro, y con ella todos los posts de esa categoría
    try:
        category = Category.objects.get(id=id)
        if id != 'all' and category:
            posts_all = Post.objects.filter(status='PB', postcategory__category=category).order_by('-published_date')
        else:
            posts_all = Post.objects.filter(status='PB').order_by('-published_date')
    except ObjectDoesNotExist:
        messages.error(request, u'La categoría no existe')
        return redirect('blog:index')
    # Si la categoria está vacia se redirige al index
    if posts_all.count() == 0:
        messages.warning(request, u'La categoría ' + category.name + '  no tiene posts')
        return redirect('blog:index')
    # Se crea un paginador de 5 posts por pagina
    paginator = PaginatorWithPageRange(posts_all, 3, 5)
    page_request_var = 'page'
    page = request.GET.get('page')
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)
    # Posts populares (sólo de posts de esta categoría)
    posts_popular = posts_all.annotate(comment_count=Count('postcomment__comment')).order_by('-comment_count')[:5]
    # Últimos comentarios (sólo de posts de esta categoría)
    comments_recent = PostComment.objects.filter(post__in=posts_all).order_by('-comment__timestamp')[:5]
    # Ultimas imagenes (TO-DO: deberían ser sólo la de esta categoría)
    pictures_recent = []
    for post_picture in PostImageSmall.objects.filter(post__in=posts_all).order_by('-image__timestamp')[:12]:
        pictures_recent.append(post_picture)
    # Se añade un log de la visita a esta categoría
    if request.user.is_authenticated:
        category.add_log(request.user, "view")

    # Se genera el contexto con toda la información y se renderiza
    context = {
        'category': category,
        'posts': posts_page,
        'posts_popular': posts_popular,
        'comments_recent': comments_recent,
        'pictures_recent': pictures_recent,
        'page_request': page_request_var
    }
    return render(request, 'category.html', context)


def post_view(request, id):
    # Se obtiene el post a visualizar y si no existe se redirige al index
    try:
        post = Post.objects.get(id=id)
        if post.status != 'PB':
            if (post.status != 'PB' and not request.user.is_authenticated) or \
                    (post.status != 'PB' and post.author != request.user.userprofile):
                messages.error(request, 'El post indicado no existe')
                return redirect('blog:index')
    except ObjectDoesNotExist:
        messages.error(request, 'El post indicado no existe')
        return redirect('blog:index')

    # Añadir log de la visita
    if request.user.is_authenticated:
        post.add_log(request.user, "view")

    # Se crea un paginador con las imagenes del post (si son más de 6)
    post_images_small = PostImageSmall.objects.filter(post=post)
    paginator = PaginatorWithPageRange(post_images_small, 6, 5)
    page_request_var = 'page'
    page = request.GET.get('page')
    try:
        post_images_small = paginator.page(page)
    except PageNotAnInteger:
        post_images_small = paginator.page(1)
    except EmptyPage:
        post_images_small = paginator.page(paginator.num_pages)

    # POST en esta vista significa nuevos comentarios o likes
    if request.method == 'POST':
        # Es necesario estar logueado
        if request.user.is_authenticated:
            # Si la petición es AJAX (TO-DO: mejorar esta lógica e incluirla también para comentarios)
            if request.is_ajax():
                # Para controlar que un mismo usuario/ip no de más de un like
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                if not PostLike.objects.filter(post=post, user=request.user, ip=ip).exists():
                    like = PostLike()
                    like.post = post
                    like.user = request.user
                    like.ip = ip
                    like.add_log(True)
                    like.save()
                # Si llegamos aquí es que el usuario ya no quiere dar like. Lo eliminamos en ese caso
                else:
                    like = PostLike.objects.filter(post=post, user=request.user, ip=ip)[0]
                    like.add_log(False)
                    like.delete()
            # Se añade un nuevo comentario a la base de datos y se asocia al post
            else:
                comment = Comment()
                comment.user = request.user
                comment.content = request.POST['comment']
                comment.save()
                post_comment = PostComment()
                post_comment.post = post
                post_comment.comment = comment
                post_comment.save()
                post_comment.add_log("create")
                messages.success(request, u'Comentario añadido')

    # Se recuperan los posts más populares
    posts_popular = Post.objects.filter(status='PB').annotate(comment_count=Count('postcomment__comment')).order_by('-comment_count')[:5]
    # Se devuelven los 5 últimos comentarios de la web
    comments_recent = PostComment.objects.filter(post__status='PB').order_by('-comment__timestamp')[:5]

    # El usuario logueado ha hecho ya Like en este post?
    already_like = "False"
    if request.user.is_authenticated:
        already_like = PostLike.objects.filter(post=post, user=request.user).exists()
    if post.updated.date() != post.timestamp.date():
        updated = True
    else:
        updated = False

    # Se genera el contexto y se renderiza
    context = {
        'posts_popular': posts_popular,
        'comments_recent': comments_recent,
        'already_like': already_like,
        'post': post,
        'post_images_small': post_images_small,
        'page_request': page_request_var,
        'updated': updated,
    }
    return render(request, 'post.html', context)


def post_create_view(request):

    # Es obligatorio estar loguedo
    if not request.user.is_authenticated:
        messages.error(request, 'Es necesario estar autenticado para crear posts')
        return redirect('blog:index')

    # Es obligatorio ser editor para crear un post
    if not request.user.userprofile.author:
        messages.error(request, u'No está autorizado para crear posts')
        return redirect('blog:index')

    # Se ha hecho SUBMIT en el FORM?
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Si se llega hasta aquí es que la información del form es correcta
            post = form.save(commit=False)
            post.id = slugify(post.title)
            # Se genera la imagen de cabecera y se asocia al post
            image = Image()
            image.caption = form.cleaned_data['image_file'].name
            image.post_slug = post.id
            image.image = form.cleaned_data['image_file']
            image.save()
            post.image = image
            # El autor del post es el usuario logueado
            post.author = UserProfile.objects.get(user=request.user)
            # Se graba el post ya que es necesario para seguir trabajando con los objetos relacionados
            post.save()
            post.add_log(request.user, "create")
            # Se actualiza la tabla de archivo de posts sólo si es un post publicado
            if post.status == 'PB':
                try:
                    post_archive = PostArchive.objects.get(year=post.published_date.year, month=post.published_date.month)
                    post_archive.posts += 1
                    post_archive.save(force_update=True)
                except ObjectDoesNotExist:
                    post_archive = PostArchive()
                    post_archive.year = post.published_date.year
                    post_archive.month = post.published_date.month
                    post_archive.posts = 1
                    post_archive.save()
            # Se graban las categorías a las que está asignado el post
            for category in form.cleaned_data['postcategory']:
                post_category = PostCategory()
                post_category.post = post
                post_category.category = apps.get_model('category', 'Category').objects.get(id=category)
                post_category.save()
            # Se graban las imagenes que se han asignado al post
            for file_image in form.cleaned_data['postimage']:
                image = Image()
                image.caption = file_image.name
                image.image = file_image
                image.post_slug = post.id
                image.save()
                post_image = PostImage()
                post_image.post = post
                post_image.image = image
                post_image.save()
            # Se graban las imagenes small que se han asignado al post
            for file_image_sm in form.cleaned_data['postimagesmall']:
                image_sm = Image()
                image_sm.caption = file_image_sm.name
                image_sm.post_slug = post.id
                image_sm.image = file_image_sm
                image_sm.save()
                post_image_sm = PostImageSmall()
                post_image_sm.post = post
                post_image_sm.image = image_sm
                post_image_sm.save()
            # Mensaje de OK y se redirige al index
            messages.success(request, 'Post creado correctamente')
            return redirect('blog:index')
    else:
        # No es un SUBMIT, en ese caso se genera un form vacio
        form = PostForm()

    # Se genera el contexto y se renderiza
    context = {
        'title': 'Create post',
        'form': form,
    }
    return render(request, 'post_form.html', context)


def post_edit_view(request, id):
    # Es obligatorio estar loguerdo
    if not request.user.is_authenticated:
        messages.error(request, 'Es necesario estar autenticado para editar posts')
        return redirect('blog:index')

    # Es obligatorio ser editor para tocar un post
    if not request.user.userprofile.author:
        messages.error(request, u'No está autorizado para editar posts')
        return redirect('blog:index')

    # Se obtiene el post a editar y si no existe se redirige al index
    try:
        post = Post.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.error(request, 'El post indicado no existe')
        return redirect('blog:index')
    
    # Sólo se pueden editar posts propios
    if request.user != post.author.user:
        messages.error(request, u'Sólo pueden editarse los posts propios')
        return redirect('blog:index')

    # Si llega hasta aquí se puede continuar
    form = PostFormEdit(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST':
        # Está correcta la información del form?
        if form.is_valid():
            status_old = post.status
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            # Sólo si se selecciona una nueva imagen de cabecera se borra la antigua y se asigna la nueva
            if form.cleaned_data['image_file']:
                post.image.delete()
                image = Image()
                image.caption = form.cleaned_data['image_file'].name
                image.image = form.cleaned_data['image_file']
                image.post_slug = post.id
                image.save()
                post.image = image
            # Se graban los cambios del post, para poder seguir con el resto de datos
            post.save()
            post.add_log(request.user, "edit")
            # Si ha pasado a status publicado en este momento se actualizan los contadores del archivo
            if status_old != 'PB' and post.status == 'PB':
                try:
                    post_archive = PostArchive.objects.get(year=post.published_date.year, month=post.published_date.month)
                    post_archive.posts += 1
                    post_archive.save(force_update=True)
                except ObjectDoesNotExist:
                    post_archive = PostArchive()
                    post_archive.year = post.published_date.year
                    post_archive.month = post.published_date.month
                    post_archive.posts = 1
                    post_archive.save()
            # Se borran las categorías a las que estuviese asignado el post antteriormente y se crean y asocian
            # las nuevas categorías asignadas al post al editarlo
            for postC in PostCategory.objects.filter(post=post):
                postC.delete()
            for category in form.cleaned_data['postcategory']:
                post_category = PostCategory()
                post_category.post = post
                post_category.category = apps.get_model('category', 'Category').objects.get(id=category)
                post_category.save()
            # Sólo si se han asignado nuevas imagenes al post se borran las antiguas y se asignan las nuevas
            if len(form.cleaned_data['postimage']) > 0:
                for image in PostImage.objects.filter(post=post):
                    image.delete()
                for file_image in form.cleaned_data['postimage']:
                    image = Image()
                    image.caption = file_image.name
                    image.image = file_image
                    image.post_slug = post.id
                    image.save()
                    post_image = PostImage()
                    post_image.post = post
                    post_image.image = image
                    post_image.save()
            # Sólo si se han asignado nuevasss imagenes small al post se borran las antiguas y se asignan las nuevas
            if len(form.cleaned_data['postimagesmall']) > 0:
                for image_sm in PostImageSmall.objects.filter(post=post):
                    image_sm.delete()
                for file_image_sm in form.cleaned_data['postimagesmall']:
                    image_sm = Image()
                    image_sm.caption = file_image_sm.name
                    image_sm.image = file_image_sm
                    image_sm.post_slug = post.id
                    image_sm.save()
                    post_image_sm = PostImageSmall()
                    post_image_sm.post = post
                    post_image_sm.image = image_sm
                    post_image_sm.save()
            # Datos grabados y se redirige al index
            messages.success(request, 'Post editado correctamente')
            return redirect('blog:index')

    # Se genera el contexto y se renderiza
    context = {
        'title': 'Edit post',
        'post': post,
        'form': form,
    }
    return render(request, 'post_form.html', context)

