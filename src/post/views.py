# Python imports
# Django imports
from django.apps import apps
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
# Third party app imports
# Local app imports
from .forms import PostForm, PostFormEdit
from .models import Post, PostImage, PostCategory, PostComment
from discuss.models import Comment
from gallery.models import Image
from user.models import UserProfile
from category.models import Category
from like.models import PostLike


def index_view(request):
    # Se obtienen los primeros 15 posts, y se crea un paginador de 5 posts por pagina
    posts_all = Post.objects.all()[:15]
    paginator = Paginator(posts_all, 5)
    page_request_var = 'page'
    page = request.GET.get('page')
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    # Los posts tipo carta son siempre 3. Ahora mismo se muestran los 3 más recientes
    posts_cards = Post.objects.order_by('timestamp')[:3]
    # Se devuelven los 5 postst más populares. Ahora mismo son los que más comentarios tienen
    posts_popular = Post.objects.annotate(comment_count=Count('postcomment__comment')).order_by('-comment_count')[:4]
    # Se devuelven los 5 últimos comentarios de la web
    comments_recent = PostComment.objects.order_by('-comment__timestamp')[:5]
    # Se devuelven las 12 últimas imagenes cargadas
    pictures_recent = Image.objects.order_by('-timestamp')[:12]

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


def contact_view(request):
    # Se genera el contexto con toda la información y se renderiza
    return render(request, 'contact.html')


def archive_view(request, year, month):
    # Se generan todos los posts para el filtrado especificado
    if int(month) > 0:
        posts_all = Post.objects.filter(timestamp__year=int(year), timestamp__month=int(month))
    else:
        posts_all = Post.objects.filter(timestamp__year=int(year))
    # Se genera el paginador para esos posts
    paginator = Paginator(posts_all, 12)
    page_request_var = 'page'
    page = request.GET.get('page')
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    # Se genera el contexto y se renderiza
    context = {
        'year': year,
        'month': month,
        'post': posts_page,
        'page_request': page_request_var
    }
    return render(request, 'archive.html', context)


def category_view(request, id):
    # Se obtienen la categoria pasada como parametro, y con ella todos los posts de esa categoría
    try:
        category = Category.objects.get(id=id)
        if id != 'all' and category:
            posts_all = Post.objects.filter(postcategory__category=category)
        else:
            posts_all = Post.objects.all()
    except ObjectDoesNotExist:
        messages.error(request, 'La categoría no existe')
        return redirect('blog:index')
    # Se crea un paginador de 5 posts por pagina
    paginator = Paginator(posts_all, 3)
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
    pictures_recent = PostImage.objects.filter(post__in=posts_all).order_by('-image__timestamp')[:12]

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
        post = get_object_or_404(Post, id=id)
    except ObjectDoesNotExist:
        messages.error(request, 'El post indicado no existe')
        return redirect('blog:index')
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
                    like.save()
                # Si llegamos aquí es que el usuario ya no quiere dar like. Lo eliminamos en ese caso
                else:
                    like = PostLike.objects.filter(post=post, user=request.user, ip=ip)
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
                messages.success(request, 'Comentario añadido')
        else:
            messages.error(request, 'Es necesario hacer log in para dar un like')

    # Se recuperan los posts más populares
    posts_popular = Post.objects.annotate(comment_count=Count('postcomment__comment')).order_by('-comment_count')[:5]
    # Se recuperan las 12 imagenes más recientes
    pictures_recent = Image.objects.order_by('-timestamp')[:12]
    # El usuario logueadoha hecho ya Like en este post?
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
        'pictures_recent': pictures_recent,
        'already_like': already_like,
        'post': post,
        'updated': updated,
    }
    return render(request, 'post.html', context)


def post_create_view(request):
    # Es obligatorio estar loguedo
    if not request.user.is_authenticated:
        messages.error(request, 'Es necesario estar autenticado para crear posts')
        return redirect('blog:index')
    # TO-DO sólo los autores pueden crear posts

    # Se ha hecho SUBMIT en el FORM?
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Si se llega hasta aquí es que la información del form es correcta
            post = form.save(commit=False)
            # Se genera la imagen de cabecera y se asocia al post
            image = Image()
            image.caption = form.cleaned_data['image_file'].name
            image.image = form.cleaned_data['image_file']
            image.save()
            post.image = image
            # El autor del post es el usuario logueado
            post.author = UserProfile.objects.get(user=request.user)
            # Se graba el post ya que es necesario para seguir trabajando con los objetos relacionados
            post.save()
            # Se graban las categorías a las que está asignado el post
            for category in form.cleaned_data['postcategory']:
                post_category = PostCategory()
                post_category.post = post
                post_category.category = apps.get_model('category', 'Category').objects.get(id=category)
                post_category.save()
            # Se graban las imagene que se han asignado al post
            for file_image in form.cleaned_data['postimage']:
                image = Image()
                image.caption = file_image.name
                image.image = file_image
                image.save()
                post_image = PostImage()
                post_image.post = post
                post_image.image = image
                post_image.save()
            # Mensaje de OK y se redirige al index
            messages.success(request, 'Successfully created')
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
    # Es obligatorio estar loguedo
    if not request.user.is_authenticated:
        messages.error(request, 'Es necesario estar autenticado para editar posts')
        return redirect('blog:index')
    # Se obtiene el post a editar y si no existe se redirige al index
    try:
        post = get_object_or_404(Post, id=id)
    except ObjectDoesNotExist:
        messages.error(request, 'El post indicado no existe')
        return redirect('blog:index')
    # Sólo se pueden editar posts propios
    if request.user != post.author.user:
        messages.error(request, 'Sólo pueden editarse los posts propios')
        return redirect('blog:index')

    # Si llega hasta aquí se puede continuar
    form = PostFormEdit(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST':
        # Está correcta la información del form?
        if form.is_valid():
            post = form.save(commit=False)
            # Sólo si se selecciona una nueva imagen de cabecera se borra la antigua y se asigna la nueva
            if form.cleaned_data['image_file']:
                post.image.delete()
                image = Image()
                image.caption = form.cleaned_data['image_file'].name
                image.image = form.cleaned_data['image_file']
                image.save()
                post.image = image
            # Se graban los cambios del post, para poder seguir con el resto de datos
            post.save()
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
            if len(form.cleaned_data['postimage'])>0:
                for image in PostImage.objects.filter(post=post):
                    image.delete()
                for file_image in form.cleaned_data['postimage']:
                    image = Image()
                    image.caption = file_image.name
                    image.image = file_image
                    image.save()
                    post_image = PostImage()
                    post_image.post = post
                    post_image.image = image
                    post_image.save()
            # Datos grabados y se redirige al index
            messages.success(request, 'Successfully created')
            return redirect('blog:index')

    # Se genera el contexto y se renderiza
    context = {
        'title': 'Edit post',
        'post': post,
        'form': form,
    }
    return render(request, 'post_form.html', context)
