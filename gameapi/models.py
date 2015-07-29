from bson.json_util import default
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None):
        if not email:
            raise ValueError('Email Required')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    rank = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class League(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=50)
    rank = models.IntegerField(default=0)
    league = models.ForeignKey(League, related_name='teams')

    def __str__(self):
        return self.name


class Match(models.Model):
    definition = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()
    Team1 = models.ForeignKey(Team, related_name='matchs_team1')
    Team2 = models.ForeignKey(Team, related_name='matchs_team2')

    def __str__(self):
        return self.definition


class Comment(models.Model):
    content = models.CharField(max_length=255)
    author = models.ForeignKey(UserProfile, related_name='comments')
    is_approved = models.BooleanField(default=False)


class Predict(models.Model):
    goals1 = models.IntegerField(default=0)
    goals2 = models.IntegerField(default=0)
    match = models.ForeignKey(Match, related_name='matchpredicts')
    user = models.ForeignKey(UserProfile, related_name='userpredicts')

    def __str__(self):
        return str(self.goals1) + '-' + str(self.goals2) + self.match.definition
