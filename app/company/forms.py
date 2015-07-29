# coding: utf-8

from django import forms
import django_filters
from app.company.models import Company, CompanyStatus, Presence
from app.founder.models import Founder
from app.mentor.models import Mentor
from django.contrib.admin.widgets import AdminDateWidget
from django.db import models

from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, \
    Submit, Field, ButtonHolder, Hidden, Div

from embed_video.fields import EmbedVideoField
from django.utils.translation import ugettext_lazy as _
from django.forms import widgets

#http://django-filter.readthedocs.org/en/latest/usage.html
class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = {'companyStatus' : ['exact'], 'name': ['icontains']}


class PresenceForm(forms.ModelForm):
    class Meta:
        model = Presence
        fields = ['date']
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date', 'class':'datepicker'})
        }

    date = forms.DateField()

class CompanyStatusCreateForm(forms.Form):

    name = forms.CharField(
        label=_('Name'),
        required=True,
    )
    name.widget.attrs.update({'placeholder': _(u'Name of the new status')})

    def __init__(self, *args, **kwargs):
        super(CompanyStatusCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'content-wrapper'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            HTML("<h1>"),
            HTML(_("New status")),
            HTML("</h1>"),
            Field('name'),
            StrictButton(_('Save'), type="submit")
        )

class CompanyCreateForm(forms.Form):

    incubated_on = forms.DateField(
        label=_('Incubated on'),
        required = False,
        input_formats=('%Y-%m-%d',),
    )
    incubated_on.widget.attrs.update({'type': 'date', 'class': 'datepicker'})

    endOfIncubation = forms.DateField(
        label=_('Incubation end on'),
        required = False,
        input_formats=('%Y-%m-%d',),
    )
    endOfIncubation.widget.attrs.update({'type': 'date', 'class': 'datepicker'})

    name = forms.CharField(
        label=_('Name'),
        required=True,
    )
    name.widget.attrs.update({'placeholder': _(u'Name of the company')})

    logo = forms.ImageField(
        label=_('Logo'),
        required=False,
    )

    video = forms.URLField(
        label=_('Video'),
        required=False,
    )
    video.widget.attrs.update({'placeholder': _(u'https://urlvideo.com/')})

    url = forms.URLField(
        label=_('Web site'),
        required=False,
    )
    url.widget.attrs.update({'placeholder': _(u'https://example.com')})

    facebook = forms.URLField(
        label=_('Facebook'),
        required=False,
    )
    facebook.widget.attrs.update({'placeholder': _(u'https://www.facebook.com/lastname.firstname')})

    twitter = forms.URLField(
        label=_('Twitter'),
        required=False,
    )
    twitter.widget.attrs.update({'placeholder': _(u'https://twitter.com/username')})

    googlePlus = forms.URLField(
        label=_('Google+'),
        required=False,
    )
    googlePlus.widget.attrs.update({'placeholder': _(u'https://plus.google.com/id')})

    linkedIn = forms.URLField(
        label=_('linkedIn'),
        required=False,
    )
    linkedIn.widget.attrs.update({'placeholder': _(u'https://ca.linkedin.com/in/username')})

    about = forms.CharField(
        label=_('Description'),
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': _(u'Write here a brief summary of your business.'),
                'class': 'md-editor'
            }
        )
    )

    status = forms.ModelChoiceField(
        label=_(u"Incubation phase"),
        queryset=CompanyStatus.objects.all(),
        required=True,
    )

    founders = forms.ModelMultipleChoiceField(
        label=_(u"Founders"),
        queryset=Founder.objects.all(),
        required=False,
        widget=forms.SelectMultiple()
    )

    mentors = forms.ModelMultipleChoiceField(
        label=_(u"Mentors"),
        queryset=Mentor.objects.all(),
        required=False,
        widget=forms.SelectMultiple()
    )

    def __init__(self, *args, **kwargs):
        super(CompanyCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'content-wrapper'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            HTML("<h1>"),
            HTML(_("New company")),
            HTML("</h1>"),
            Field('name'),
            Field('status'),
            Field('incubated_on'),
            Field('endOfIncubation'),
            Field('logo'),
            Field('video'),
            Field('url'),
            Field('facebook'),
            Field('twitter'),
            Field('googlePlus'),
            Field('linkedIn'),
            Field('about'),
            Field('founders'),
            Field('mentors'),
            StrictButton(_('Save'), type="submit")
        )

class MiniCompanyUpdateForm(forms.Form):
    name = forms.CharField(
        label=_('Name'),
        required=True,
    )
    name.widget.attrs.update({'placeholder': _(u'Name of the company')})

    logo = forms.ImageField(
        label=_('Logo'),
        required=False,
    )

    video = forms.URLField(
        label=_('Video'),
        required=False,
    )
    video.widget.attrs.update({'placeholder': _(u'https://urlvideo.com/')})

    url = forms.URLField(
        label=_('Web site'),
        required=False,
    )
    url.widget.attrs.update({'placeholder': _(u'https://example.com')})

    facebook = forms.URLField(
        label=_('Facebook'),
        required=False,
    )
    facebook.widget.attrs.update({'placeholder': _(u'https://www.facebook.com/lastname.firstname')})

    twitter = forms.URLField(
        label=_('Twitter'),
        required=False,
    )
    twitter.widget.attrs.update({'placeholder': _(u'https://twitter.com/username')})

    googlePlus = forms.URLField(
        label=_('Google+'),
        required=False,
    )
    googlePlus.widget.attrs.update({'placeholder': _(u'https://plus.google.com/id')})

    linkedIn = forms.URLField(
        label=_('linkedIn'),
        required=False,
    )
    linkedIn.widget.attrs.update({'placeholder': _(u'https://ca.linkedin.com/in/username')})

    about = forms.CharField(
        label=_('Description'),
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': _(u'Write here a brief summary of your business.'),
                'class': 'md-editor'
            }
        )
    )

    def __init__(self, company, *args, **kwargs):
        super(MiniCompanyUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'content-wrapper'
        self.helper.form_method = 'post'

        self.company = company
        self.fields['about'].initial = company.description
        self.fields['name'].initial = company.name
        self.fields['url'].initial = company.url
        self.fields['video'].initial = company.video

        self.fields['facebook'].initial = company.facebook
        self.fields['twitter'].initial = company.twitter
        self.fields['googlePlus'].initial = company.googlePlus
        self.fields['linkedIn'].initial = company.linkedIn

        self.helper.layout = Layout(
            HTML("<h1>"),
            HTML(_("Update company")),
            HTML("</h1>"),
            Field('name'),
            Field('logo'),
            Field('video'),
            Field('url'),
            Field('facebook'),
            Field('twitter'),
            Field('googlePlus'),
            Field('linkedIn'),
            Field('about'),
            StrictButton(_('Save'), type="submit")
        )

    def save(self):
        self.company.save()


class CompanyUpdateForm(MiniCompanyUpdateForm):

    incubated_on = forms.DateField(
        label=_('Incubated on'),
        required = False,
        input_formats=('%Y-%m-%d',),
    )
    incubated_on.widget.attrs.update({'type': 'date', 'class': 'datepicker'})

    endOfIncubation = forms.DateField(
        label=_('Incubation end on'),
        required = False,
        input_formats=('%Y-%m-%d',),
    )
    endOfIncubation.widget.attrs.update({'type': 'date', 'class': 'datepicker'})

    founders = forms.ModelMultipleChoiceField(
        label=_(u"Founders"),
        queryset=Founder.objects.all(),
        required=False,
        widget=forms.SelectMultiple()
    )

    mentors = forms.ModelMultipleChoiceField(
        label=_(u"Mentors"),
        queryset=Mentor.objects.all(),
        required=False,
        widget=forms.SelectMultiple()
    )

    def __init__(self, company, *args, **kwargs):
        super(CompanyUpdateForm, self).__init__(company, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'content-wrapper'
        self.helper.form_method = 'post'

        self.company = company
        self.fields['about'].initial = company.description
        self.fields['name'].initial = company.name
        self.fields['url'].initial = company.url
        self.fields['video'].initial = company.video
        self.fields['founders'].initial = company.founders.all
        self.fields['mentors'].initial = company.mentors.all
        if company.incubated_on :
            self.fields['incubated_on'].initial = company.incubated_on.isoformat()
        if company.endOfIncubation :
            self.fields['endOfIncubation'].initial = company.endOfIncubation.isoformat()
        self.fields['facebook'].initial = company.facebook
        self.fields['twitter'].initial = company.twitter
        self.fields['googlePlus'].initial = company.googlePlus
        self.fields['linkedIn'].initial = company.linkedIn

        self.helper.layout = Layout(
            HTML("<h1>"),
            HTML(_("Update company")),
            HTML("</h1>"),
            Field('name'),
            Field('logo'),
            Field('video'),
            Field('url'),
            Field('facebook'),
            Field('twitter'),
            Field('googlePlus'),
            Field('linkedIn'),
            Field('founders'),
            Field('mentors'),
            Field('incubated_on'),
            Field('endOfIncubation'),
            Field('about'),
            StrictButton(_('Save'), type="submit")
        )