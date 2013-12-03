from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.functional import cached_property

from . import fields

from taggit.managers import TaggableManager

from datetime import datetime

class TimestampedMixin(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = datetime.now()
        self.modified = datetime.now()
        return super(TimestampedMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class Category(models.Model):
    '''Category exists primarily as an access control mechanism.

We could simply organise Forum by tags, but then it would be a lot more
difficult to control.
'''
    title = fields.TitleField()

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('view_category', args=(self.id,))

    def __unicode__(self):
        return self.title

class Forum(TimestampedMixin):
    title = fields.TitleField()
    categories = models.ManyToManyField('Category', related_name='forums')

    def get_absolute_url(self):
        return reverse('view_forum', args=(self.id,))

    def __unicode__(self):
        return self.title

class ThreadManager(models.Manager):
    def with_counts(self):
        return self.get_query_set().annotate(
            post_count=models.Count('posts'),
            most_recent=models.Max('posts__created'),
            involved_count=models.Count('posts__user'), # Will this be distinct?
        )

class Thread(TimestampedMixin):
    #TODO: thread slug?
    subject = fields.TitleField()
    forum = models.ForeignKey('Forum', related_name='threads')
    tags = TaggableManager(blank=True)

    objects = ThreadManager()

    @cached_property
    def post_count(self):
        return self.posts.count()

    @cached_property
    def most_recent(self):
        return self.posts.aggregate(
            most_recent=models.Max('posts__created')
        )['most_recent']

    @cached_property
    def involved_count(self):
        return self.posts.aggregate(
            involved=models.Count('posts__user')
        )['involved']

    def get_absolute_url(self):
        return reverse('view_thread', args=(self.forum.id, self.id,))

    def __unicode__(self):
        return self.subject


class Post(TimestampedMixin):
    thread = models.ForeignKey('Thread', related_name='posts')
    subject = fields.TitleField(blank=True)
    author = models.ForeignKey('Profile', related_name='posts')
    content = models.TextField(blank=True)
    tags = TaggableManager(blank=True)


##
## Profile
##

class ProfileManager(models.Manager):
    def get_queryset(self):
        return super(ProfileManager, self).get_queryset().select_related('user')

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    nickname = fields.TitleField(blank=True)

    avatar = models.ImageField(blank=True, upload_to='avatars')

    signature = models.TextField(blank=True)

    objects = ProfileManager()

##
## Permission models
##
from django.contrib.contenttypes.models import ContentType

class ThreadAdmin(models.Model):
    profile = models.ForeignKey('Profile', related_name='thread_perms')
    thread = models.ForeignKey('Thread', related_name='admin_perms')
    permissions = models.ManyToManyField('auth.Permission',
        limit_choices_to=lambda: {
            'content_type': ContentType.objects.get_for_model(Post),
        },
    )

class ForumAdmin(models.Model):
    profile = models.ForeignKey('Profile', related_name='forum_perms')
    forum = models.ForeignKey('Forum', related_name='admin_perms')
    permissions = models.ManyToManyField('auth.Permission',
        limit_choices_to=lambda: {
            'content_type': ContentType.objects.get_for_model(Thread),
        },
    )