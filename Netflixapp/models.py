import email
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
import uuid
from django.conf import settings
from django.db.models.signals import post_save
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

AGE_CHOICES = (
    ('All', 'All'),
    ('Kids', 'Kids'),
)

MOVIE_CHOICES = (
    ('seasonal', 'Seasonal'),
    ('single', 'Single'),
)

WEBSERIES_CHOICES = (
    ('episode', 'Episode'),
)

MEMBERSHIP_CHOICES = (
    ('Free', 'free'),
    ('Montly', 'montly'),
    ('Yearly', 'yearly')
)

# profile


class CustomUser(AbstractUser):
    profiles = models.ManyToManyField('Profile', blank=True)


class Profile(models.Model):
    name = models.CharField(max_length=1000)
    age_limit = models.CharField(choices=AGE_CHOICES, max_length=10)
    uuid = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.name

# movie


class Movie(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    type = models.CharField(choices=MOVIE_CHOICES, max_length=10)
    video = models.ManyToManyField('Video')
    image = models.ImageField(upload_to='covers')
    age_limit = models.CharField(choices=AGE_CHOICES, max_length=10)

    def __str__(self):
        return self.title


class Video(models.Model):
    title = models.CharField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to='movies')

    def __str__(self):
        return self.title

# web series models


class Webseries(models.Model):
    webseries_name = models.CharField(max_length=1000)
    webseries_description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    type = models.CharField(choices=WEBSERIES_CHOICES, max_length=10)
    is_premium = models.BooleanField(default=False)
    webseries_image = models.ImageField(upload_to='webseries')
    age_limit = models.CharField(choices=AGE_CHOICES, max_length=10)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.webseries_name


class webseriesepisodes(models.Model):
    webseries = models.ForeignKey(Webseries, on_delete=models.CASCADE)
    webseriesepisodes_name = models.CharField(max_length=1000)
    webseries_description = models.TextField()
    video_url = models.URLField(max_length=500)
    can_view = models.BooleanField(default=False)

    def __str__(self):
        return self.webseriesepisodes_name


# membership

# class Membership(models.Model):
#     slug = models.SlugField()
#     membership_type = models.CharField(
#         choices=MEMBERSHIP_CHOICES,
#         default='Free',
#         max_length=30)
#     price = models.IntegerField(default=15)
#     stripe_plan_id = models.CharField(max_length=40)

#     def __str__(self):
#         return self.membership_type


# class UserMembership(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     stripe_customer_id = models.CharField(max_length=40)
#     membership = models.ForeignKey(
#         Membership, on_delete=models.SET_NULL, null=True)

#     def __str__(self):
#         return self.user.username


# def post_save_usermembership_create(sender, instance, created, *args, **kwargs):
#     user_membership, created = UserMembership.objects.get_or_create(
#         user=instance)

#     if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
#         new_customer_id = stripe.Customer.create(email=instance.email)
#         free_membership = Membership.objects.get(membership_type='Free')
#         user_membership.stripe_customer_id = new_customer_id['id']
#         user_membership.membership = free_membership
#         user_membership.save()


# post_save.connect(post_save_usermembership_create,
#                   sender=settings.AUTH_USER_MODEL)


# class Subscription(models.Model):
#     user_membership = models.ForeignKey(
#         UserMembership, on_delete=models.CASCADE)
#     stripe_subscription_id = models.CharField(max_length=40)
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.user_membership.user.username
