# coding=utf-8
# decoding=utf-8
# Python imports
# Django imports
from django.apps import apps
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.template.defaultfilters import slugify
# Third party app imports
# Local app imports
from utilidades import PaginatorWithPageRange
from .forms import PostForm, PostFormEdit
from .models import Post, PostImage, PostCategory, PostComment, PostArchive, PostImage, PostView, PostLike
from discuss.models import Comment
from gallery.models import Image
from user.models import UserProfile
from category.models import Category


def index_view(request):

    # Se obtienen los primeros 99 posts, y se crea un paginador de 5 posts por pagina
    posts_all = Post.objects.filter(status='PB').order_by('-published_date')[:1000]
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
    # Se devuelven los 5 postst más populares. Los que mas visualizaciones tienen
    posts_popular = Post.objects.filter(status='PB').annotate(views_count=Count('postview__post')).order_by('-views_count')[:4]
    # Se devuelven los 5 últimos comentarios de la web
    comments_recent = PostComment.objects.order_by('-comment__timestamp')[:5]
    # Se devuelven las 12 últimas imagenes cargadas
    pictures_recent = PostImage.objects.filter(post__status='PB', image__show_gallery='True').order_by('-image__timestamp')[:20]
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
    if 2000 < int(year) < 2040:
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
    pictures_recent = PostImage.objects.filter(post__status='PB', image__show_gallery='True').order_by('-image__timestamp')[:12]

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
    post_images_all = PostImage.objects.filter(post__status='PB', image__show_gallery='True').order_by('-image__timestamp')
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
    paginator = PaginatorWithPageRange(posts_all, 5, 5)
    page_request_var = 'page'
    page = request.GET.get('page')
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)
    # Posts populares (sólo de posts de esta categoría)
    posts_popular = posts_all.annotate(comment_count=Count('postcomment__comment')).order_by('-comment_count').order_by('-published_date')[:5]
    # Últimos comentarios (sólo de posts de esta categoría)
    comments_recent = PostComment.objects.filter(post__in=posts_all).order_by('-comment__timestamp')[:5]
    # Ultimas imagenes (TO-DO: deberían ser sólo la de esta categoría)
    pictures_recent = []
    for post_picture in PostImage.objects.filter(post__in=posts_all).order_by('-image__timestamp')[:12]:
        pictures_recent.append(post_picture)

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

    # Añadir visita al post en caso de no ser una visita de una IP ya resgistrada
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if not PostView.objects.filter(post=post, ip=ip).exists():
        view = PostView()
        view.post = post
        view.ip = ip
        view.save()
        
    # Se crea un paginador con las imagenes del post (si son más de 6)
    post_images = PostImage.objects.filter(post=post)
    paginator = PaginatorWithPageRange(post_images, 6, 5)
    page_request_var = 'page'
    page = request.GET.get('page')
    try:
        post_images = paginator.page(page)
    except PageNotAnInteger:
        post_images = paginator.page(1)
    except EmptyPage:
        post_images = paginator.page(paginator.num_pages)

    # POST en esta vista significa nuevos comentarios o likes
    if request.method == 'POST' and request.user.is_authenticated:
        comment = Comment()
        comment.user = request.user
        comment.content = request.POST['comment']
        comment.save()
        post_comment = PostComment()
        post_comment.post = post
        post_comment.comment = comment
        post_comment.save()
        messages.success(request, 'Comentario añadido')

    # El usuario logueado ha hecho ya Like en este post?
    already_like = "False"
    if request.user.is_authenticated:
        already_like = PostLike.objects.filter(post=post, user=request.user).exists()
    if post.updated.date() != post.timestamp.date():
        updated = True
    else:
        updated = False

    # Se recuperan los posts más populares
    posts_popular = Post.objects.filter(status='PB').annotate(comment_count=Count('postcomment__comment')).order_by('-comment_count')[:5]
    # Se devuelven los 5 últimos comentarios de la web
    comments_recent = PostComment.objects.filter(post__status='PB').order_by('-comment__timestamp')[:5]
    # Post editado
    updated = False
    if post.updated.date() != post.timestamp.date():
        updated = True

    # Se genera el contexto y se renderiza
    context = {
        'posts_popular': posts_popular,
        'comments_recent': comments_recent,
        'already_like': already_like,
        'post': post,
        'post_images': post_images,
        'page_request': page_request_var,
        'updated': updated,
    }
    return render(request, 'post.html', context)


def post_like_view(request, id):
    if request.user.is_authenticated:
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
        # Se busca un like previo, y si no hay, se hace el like
        if not PostLike.objects.filter(post=post, user=request.user).exists():
            like = PostLike()
            like.post = post
            like.user = request.user
            like.save()
            data = {
                'already_like': 'true',
                'likes': PostLike.objects.filter(post=post).count()
            }
            return JsonResponse(data)
        # Si llegamos aquí es que el usuario ya no quiere dar like. Lo eliminamos en ese caso
        else:
            like = PostLike.objects.filter(post=post, user=request.user)[0]
            like.delete()
            data = {
                'already_like': 'false',
                'likes': PostLike.objects.filter(post=post).count()
            }
            return JsonResponse(data)


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
            if len(form.cleaned_data['postimage']) > 0:
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
            # Mensaje de OK y se redirige al index
            messages.success(request, 'Post creado correctamente')
            return redirect('blog:index')
        else:
            messages.error(request, 'Error creando el post')
    else:
        # No es un SUBMIT, en ese caso se genera un form vacio
        form = PostForm()

    # Se genera el contexto y se renderiza
    context = {
        'title': 'Create post',
        'errors': form.errors,
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
            # Datos grabados y se redirige al index
            messages.success(request, 'Post editado correctamente')
            return redirect('blog:index')
        else:
            messages.error(request, 'Error editando el post')


    # Se genera el contexto y se renderiza
    context = {
        'title': 'Edit post',
        'post': post,
        'errors': form.errors,
        'form': form,
    }
    return render(request, 'post_form.html', context)

def post_delete_view(request, id):
    # Es obligatorio estar loguerdo
    if not request.user.is_authenticated:
        messages.error(request, 'Es necesario estar autenticado para eliminar posts')
        return redirect('blog:index')

    # Es obligatorio ser editor para tocar un post
    if not request.user.userprofile.author:
        messages.error(request, u'No está autorizado para eliminar el post indicado')
        return redirect('blog:index')

    # Se obtiene el post a eliminar y si no existe se redirige al index
    try:
        post = Post.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.error(request, 'El post indicado no existe')
        return redirect('blog:index')
    
    # Sólo se pueden eliminar posts propios
    if request.user != post.author.user:
        messages.error(request, u'Sólo pueden eliminarse los posts propios')
        return redirect('blog:index')

    # Si llega hasta aquí se puede continuar
    try:
        post.delete()
        messages.success(request, 'Post eliminado con exito')
    except Exception:
        messages.error(request, 'Error eliminando post')

    return redirect('blog:index')
