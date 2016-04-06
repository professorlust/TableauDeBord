# coding: utf-8

from datetime import date
from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views import generic

from app.floorMap.forms import RentalForm, RentalFormUpdate
from app.floorMap.models import Room, Rent


class FloorMapIndex(generic.ListView):
    # Floor Plan Page
    model = Room
    template_name = 'floorMap/floorMap.html'
    context_object_name = 'list_room_data'

    # You need to be connected, and you need to have access as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech() or\
                self.request.user.profile.isFounder() or\
                self.request.user.profile.isMentor() or\
                self.request.user.profile.isExecutive():
            return super(FloorMapIndex, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")


class RoomDetails(generic.DetailView):
    # View room details
    model = Room
    template_name = 'floorMap/room_details.html'

    # You need to be connected, and you need to have access as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech() or \
                self.request.user.profile.isFounder() or \
                self.request.user.profile.isMentor() or \
                self.request.user.profile.isExecutive():
            return super(RoomDetails, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_context_data(self, **kwargs):
        context = super(RoomDetails, self).get_context_data(**kwargs)

        room = Room.objects.get(id=self.kwargs['pk'])

        context['room_label'] = room.static_label
        context['room_color'] = room.type.bg_color

        if room.is_rental():
            active_rental = room.get_active_rental()

            if self.request.user.profile.isCentech():
                rentals = room.rentals.all().order_by("-date_start")
            else:
                upcoming = room.get_upcoming_rentals().order_by("-date_start")
                if active_rental:
                    rentals = list(chain(upcoming, [active_rental]))
                else:
                    rentals = upcoming

            if active_rental:
                context['room_label'] = active_rental.company.name
            else:
                context['room_label'] = _(u'Available')
                context['room_color'] = room.type.alt_bg_color

            context['rentals'] = rentals
            context['active_rental'] = active_rental
        return context


class RentalCreate(generic.CreateView):
    # Add a new rental
    model = Rent
    template_name = 'rental/rent_form.html'
    form_class = RentalForm

    # You need to be connected, and you need to have access
    # as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(RentalCreate, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_initial(self):
        if 'pk' in self.kwargs:
            return {'company': int(self.kwargs['pk'])}

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _(u'The rental has been saved.')
        )
        return self.request.GET['next']

    def form_valid(self, form):
        redirect_url = super(RentalCreate, self).form_valid(form)
        if self.object.date_start <= date.today() <= self.object.date_end:
            call_command('updateFloorMap')
        return redirect_url


class RentalUpdate(generic.UpdateView):
    # Update the rental
    model = Rent
    template_name = 'rental/rent_form.html'
    form_class = RentalFormUpdate

    # You need to be connected, and you need to have access
    # as Centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(RentalUpdate, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _(u'The rental has been saved.')
        )
        return self.request.GET['next']

    def form_valid(self, form):
        redirect_url = super(RentalUpdate, self).form_valid(form)
        if self.object.date_start <= date.today() <= self.object.date_end:
            call_command('updateFloorMap')
        return redirect_url


class RentalDelete(generic.DeleteView):
    # Delete the rental
    model = Rent
    template_name = 'rental/rent_confirm_delete.html'

    # You need to be connected, and you need to have access
    # as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(RentalDelete, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_success_url(self, **kwargs):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _(u'The rental has been removed.')
        )
        return self.request.GET['next']

    def get_context_data(self, **kwargs):
        context = super(RentalDelete, self).get_context_data(**kwargs)
        context['rental'] = kwargs['object']
        return context

    def delete(self, request, *args, **kwargs):
        redirect_url = super(RentalDelete, self).\
            delete(request, *args, **kwargs)
        if self.object.date_start <= date.today() <= self.object.date_end:
            call_command('updateFloorMap')
        return redirect_url
