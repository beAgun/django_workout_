from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
         'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'sh', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'e', 'ю': 'yu',
         'я': 'ya', ' ': '-', '/': '-', ',': '', '«': '', '»': '',}

    return "".join(map(lambda x: d[x] if x in d else x, s.lower()))


def get_photo_path(instance, filename):
    return f'exercises/{instance.name}/{filename}'


# Create your models here.
class Exercise(models.Model):
    objects = models.Manager()

    class IsCompound(models.IntegerChoices):
        compound = 1, 'Базовое'
        isolation = 0, 'Изолирующее'

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    name = models.CharField(max_length=255, verbose_name='Название')

    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    description = models.TextField(blank=True, verbose_name='Краткое описание')
    start = models.TextField(blank=True, verbose_name='Исходное положение')
    performing = models.TextField(blank=True, verbose_name='Исполнение')
    variations = models.TextField(blank=True, verbose_name='Вариации')
    remarks = models.TextField(blank=True, verbose_name='Примечания')
    safety = models.TextField(blank=True, verbose_name='Безопасность')
    additional = models.TextField(blank=True, verbose_name='Дополнительная информация')

    image = models.ImageField(upload_to=get_photo_path,
                              default='exercises/no_picture.jpg',
                              blank=True, null=True, verbose_name='Картинка')

    equipment = models.ManyToManyField(to='Equipment', related_name='exercises',
                                       blank=True, verbose_name='Инвентарь')

    muscle = models.ManyToManyField(to='TargetMuscle', related_name='muscles',
                                    blank=True, verbose_name='Целевая мышечная группа')

    level = models.ManyToManyField(to='ExperienceLevel', related_name='levels',
                                   blank=True, verbose_name='Уровень подготовки')

    is_compound = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), IsCompound.choices)),
                                      blank=True, null=True,
                                      verbose_name='Тип')

    workout_type = models.ForeignKey(to='WorkoutType', on_delete=models.RESTRICT,
                                     verbose_name='Тип тренировки')

    def get_absolute_url(self):
        return reverse('exercise', kwargs={'ex_slug': self.slug})

    def get_muscles(self):
        return self.muscle.all()

    def get_equipment(self):
        return self.equipment.all()

    def get_level(self):
        return self.level.all()

    def get_text_elements(self):
        return {'Описание': self.description, 'Исходное положение': self.start,
                'Исполнение': self.performing, 'Примечания': self.remarks,
                'Безопасность': self.safety, 'Дополнительная информация': self.additional,
                'Вариации': self.variations}

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     if self.slug is None:
    #         self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)


class Equipment(models.Model):

    class Meta:
        verbose_name = 'Categories by equipment'
        verbose_name_plural = 'Categories by equipment'

    objects = models.Manager()

    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('equipment', kwargs={'eq_slug': self.slug})

    def __str__(self):
        return self.name


class ExperienceLevel(models.Model):

    class Meta:
        verbose_name = 'Categories by experience level'
        verbose_name_plural = 'Categories by experience level'

    objects = models.Manager()

    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('level', kwargs={'lvl_slug': self.slug})

    def __str__(self):
        return self.name


# class Muscle(models.Model):
#
#     objects = models.Manager()
#
#     name = models.CharField(max_length=100, db_index=True)
#     slug = models.SlugField(max_length=100, unique=True, db_index=True)
#
#     def get_absolute_url(self):
#         return reverse('muscle', kwargs={'muscle_slug': self.slug})
#
#     def __str__(self):
#         return self.name


class TargetMuscle(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
    position = models.PositiveIntegerField('Позиция', default=1)
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name='children',
                               verbose_name='Родитель')

    tree = None

    class Meta:
        verbose_name = 'Categories by target muscle group'
        verbose_name_plural = 'Categories by target muscle group'
        ordering = ['position']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('muscle', kwargs={'muscle_path': self.slug})

    def update_tree(self):
        self.tree = get_tree()

    @property
    def get_descendants(self):
        if self.tree is None:
            self.update_tree()
        return self.tree[self.pk]['descendants']

    # @property
    # def path(self):
    #     return '/'.join(i.slug for i in self.get_ancestors(include_self=True))

    # def get_absolute_url(self):
    #     return reverse('muscle', kwargs={'muscle_path': self.path})


def get_tree():
    muscles = TargetMuscle.objects.all()
    tree = {}
    roots = []
    print('00000', tree)
    for i in muscles:
        tree[i.id] = {'id': i.id, 'name': i.name, 'slug': i.slug, 'children': []}

        if i.parent_id is None:
            roots += [i.id]
        else:
            tree[i.parent_id]['children'] += [i.id]
    print('00000', tree)

    def rec(node, tree):
        if node in roots:
            tree[node]['path'] = reverse('muscle',
                                         kwargs={'muscle_path': tree[node]['slug']})

        for child in tree[node]['children']:
            tree[child]['path'] = tree[node]['path'] + tree[child]['slug'] + '/'
            tree = rec(child, tree)

        return tree

    def rec2(node):
        tree[node]['descendants'] = [node]

        for child in tree[node]['children']:
            tree[node]['descendants'] += rec2(child)

        return tree[node]['descendants']

    for root in roots:
        tree = rec(root, tree)
        print(tree)

    for root in roots:
        rec2(root)
        print('77777', tree)

    return tree

# class TargetMuscle(MPTTModel):
#
#     objects = models.Manager()
#
#     name = models.CharField(max_length=100, unique=True, db_index=True)
#     slug = models.SlugField(max_length=100, unique=True, db_index=True)
#     position = models.PositiveIntegerField('Позиция', default=1)
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
#                             related_name='children')
#
#     class MPTTMeta:
#         order_insertion_by = ['position']
#
#     def __str__(self):
#         return str(self.name)
#
#     @property
#     def path(self):
#         return '/'.join(i.slug for i in self.get_ancestors(include_self=True))
#
#     def get_absolute_url(self):
#
#         return reverse('muscle', kwargs={'muscle_path': self.path})
#
#     class Meta:
#         verbose_name = 'Categories by target muscle group'
#         verbose_name_plural = 'Categories by target muscle group'


class WorkoutType(models.Model):
    title = models.CharField(max_length=200, unique=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.title}'



