from django.contrib import admin
from .models import *


# Register the address model to the admin panel
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'village', 'parish', 'sub_county', 'county', 'district', 'region']
    search_fields = ['village', 'parish', 'sub_county', 'county', 'district', 'region']

admin.site.register(Address, AddressAdmin)


# Registering the polling stations model to the admin panel
class PollingStationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address']
admin.site.register(Polling_Station, PollingStationAdmin)


# Registering the Voters model to the admin panel
class VotersAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'gender', 'voter_type', 'Polling_station', 'fingerprint_xtics']

    def delete_model(self, request, obj):
        # Clear the voter_id in the session
        if 'voter_id' in request.session and str(obj.id) == request.session['voter_id']:
            del request.session['voter_id']
        super().delete_model(request, obj)

admin.site.register(Voters, VotersAdmin)


# Registering the FingerPrints model to the database
class FingerPrintsAdmin(admin.ModelAdmin):
    list_display = ['id', 'voter', 'hand', 'finger']
admin.site.register(FingerPrints, FingerPrintsAdmin)


# # Registering the AudioTypes model to the admin panel
# class AudioTypesAdmin(admin.ModelAdmin):
#     list_display = ['id', 'audio_type']
# admin.site.register(AudioTypes, AudioTypesAdmin)


# Registering the audios model to the admin panel
# class AudiosAdmin(admin.ModelAdmin):
#     list_display = ['id', 'audio_type','audio_text']
# admin.site.register(Audios, AudiosAdmin)


# Registering the candiates model into the database
class CandidatesAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name','last_name','gender', 'political_party', 'post_aspired_for']
admin.site.register(Candidates, CandidatesAdmin)


# Registering the model of casted votes to the admin panel
class CastedVotesAdmin(admin.ModelAdmin):
    list_display = ['id', 'candidate', 'voter']
admin.site.register(CastedVotes, CastedVotesAdmin)
