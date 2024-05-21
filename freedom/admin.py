from django.contrib import admin
from .models import *


# Register the address model to the admin panel
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'village', 'parish', 'sub_county', 'county', 'district', 'region']
    search_fields = ['village', 'parish', 'sub_county', 'county', 'district', 'region']

admin.site.register(Address, AddressAdmin)


# Registering the polling stations model to the admin panel
class PollingStationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'date_created']
admin.site.register(PollingStation, PollingStationAdmin)


# Registering the Voters model to the admin panel
class VotersAdmin(admin.ModelAdmin):

    list_display = ['id', 'first_name', 'last_name', 'gender', 'voter_type', 'Polling_station', 'date_created', 'fingerprint_xtics']

admin.site.register(Voters, VotersAdmin)


# Registering the FingerPrints model to the database
class FingerPrintsAdmin(admin.ModelAdmin):
    list_display = ['id', 'voter', 'hand', 'finger', 'date_created']
admin.site.register(FingerPrints, FingerPrintsAdmin)


# Registering the AudioTypes model to the admin panel
class AudioTypesAdmin(admin.ModelAdmin):
    list_display = ['id', 'audio_type', 'date_created']
admin.site.register(AudioTypes, AudioTypesAdmin)


# Registering the audios model to the admin panel
class AudiosAdmin(admin.ModelAdmin):
    list_display = ['id', 'audio_type','audio_text', 'date_created']
admin.site.register(Audios, AudiosAdmin)


# Registering the candiates model into the database
class CandidatesAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name','last_name','gender', 'political_party', 'post_aspired_for', 'date_created']
admin.site.register(Candidates, CandidatesAdmin)


# Registering the model of casted votes to the admin panel
class CastedVotesAdmin(admin.ModelAdmin):
    list_display = ['id', 'candidate', 'voter', 'date_created']
admin.site.register(CastedVotes, CastedVotesAdmin)
