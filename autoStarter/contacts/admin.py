from django.contrib import admin
from contacts.models import Phone, Schedule, Address, Email, Contact, SocialLink, Messenger

class MessengerInline(admin.TabularInline):
    model = Messenger
    extra = 0


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 0


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0


class EmailInline(admin.TabularInline):
    model = Email
    extra = 0


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 0


class ContactAdmin(admin.ModelAdmin):
    inlines = [EmailInline, AddressInline, PhoneInline, MessengerInline, ScheduleInline, SocialLinkInline]


admin.site.register(Contact, ContactAdmin)
