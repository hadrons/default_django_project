#coding:utf-8

from django.contrib import admin
from django.conf.urls import url
from django.contrib.admin.utils import unquote
from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField,AdminPasswordChangeForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())

from .models import Person
from .forms import CustomUserCreationForm,CustomUserChangeForm

class UserAdmin(admin.ModelAdmin):

    add_form_template = 'admin/auth/user/add_form.html'
    
    change_user_password_template = None
    
    fieldsets = (
        (None, {'fields': ('email','password','name','cellular','gender',)}),
        (_('Personal info'), {'fields': ('email',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1', 'password2','name','interests','is_active', 'is_staff', 'is_superuser','groups',),
        }),
    )
    form = UserChangeForm
    add_form = CustomUserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ('id', 'name', 'email', 'is_staff')
    #list_filter = ('name', 'is_superuser', 'is_active',)
    search_fields = ('email','name')
    ordering = ('email',)
    filter_horizontal = ('user_permissions','groups',)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(UserAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super(UserAdmin, self).get_form(request, obj, **defaults)

    def get_urls(self):
        return [
            url(r'^(.+)/password/$', self.admin_site.admin_view(self.user_change_password), name='auth_user_password_change'),
        ] + super(UserAdmin, self).get_urls()

    def lookup_allowed(self, lookup, value):
        # See #20078: we don't want to allow any lookups involving passwords.
        if lookup.startswith('password'):
            return False
        return super(UserAdmin, self).lookup_allowed(lookup, value)


    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = self.get_object(request, unquote(id))
        if user is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': force_text(self.model._meta.verbose_name),
                'key': escape(id),
            })
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, user, change_message)
                msg = ugettext('Password changed successfully.')
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
        }
        context.update(admin.site.each_context(request))

        request.current_app = self.admin_site.name

        return TemplateResponse(request,
            self.change_user_password_template or
            'admin/auth/user/change_password.html',
            context)

admin.site.register(Person,UserAdmin)