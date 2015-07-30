from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from gameapi.models import *


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'email', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class TeamInline(admin.TabularInline):
    model = Team
    extra = 3


class HomeMatchInline(admin.TabularInline):
    model = Match
    fk_name = 'Team1'
    extra = 3


class AwayMatchInline(admin.TabularInline):
    model = Match
    fk_name = 'Team2'
    extra = 3


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3


class PredictInline(admin.TabularInline):
    model = Predict
    extra = 3


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('personal info', {'fields': ('rank',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'rank', 'password1', 'password2')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()
    inlines = [CommentInline, PredictInline]


class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('other info', {'fields': ('country',)}),
    )
    search_fields = ('name',)
    ordering = ('name', 'country')
    list_filter = ('country',)
    inlines = [TeamInline]


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'league')
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('League info', {'fields': ('league', 'rank',)}),
    )
    search_fields = ('name',)
    ordering = ('name', 'rank', 'league')
    list_filter = ('league',)
    inlines = [HomeMatchInline, AwayMatchInline]


class MatchAdmin(admin.ModelAdmin):
    list_display = ('definition', 'date', 'Team1', 'Team2')
    fieldsets = (
        (None, {'fields': ('definition', 'date',)}),
        ('Home and Away Team', {'fields': ('Team1', 'Team2',)}),
    )
    search_fields = ('definition',)
    ordering = ('definition', 'Team1', 'Team2', 'date',)
    list_filter = ('date',)
    inlines = [CommentInline, PredictInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'match', 'is_approved')
    fieldsets = (
        (None, {'fields': ('content', 'author', 'match', 'is_approved')}),
    )
    search_fields = ('content',)
    ordering = ('content', 'author', 'match',)
    list_filter = ('author', 'match')


class PredictAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'goals1', 'goals2',)
    fieldsets = (
        (None, {'fields': ('user', 'match',)}),
        ('Goals', {'fields': ('goals1', 'goals2',)}),
    )
    search_fields = ('user',)
    ordering = ('user', 'match',)
    list_filter = ('match', 'user')


admin.site.register(UserProfile, MyUserAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Predict, PredictAdmin)
admin.site.unregister(Group)
