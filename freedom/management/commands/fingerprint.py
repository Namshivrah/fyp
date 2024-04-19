# create_fingerprints.py
from django.core.management.base import BaseCommand

from freedom.models import (Address, FingerprintBinaryData, Fingerprints,
                            Polling_station, Voter, Voter_type)


class Command(BaseCommand):
    help = 'Create Fingerprints instances with JSON data'

    def handle(self, *args, **options):
        address_instance = Address.objects.get(village='kyampiisi', parish='kitezi', sub_county='karagwa', county='busima',district='Buwata',region='Central')

        voter_type_instance = Voter_type.objects.get(name='Blind-Lame', description='Cannot see at the same time cannot walk', priveledges='VC')

        #polling_station_instance = Polling_station.objects.get(name='Kitezi',address='kitezi')
        polling_station_instance = Polling_station.objects.get(name='Kitezi',address='kitezi')
        # Assuming you have a Voter instance and a FingerprintBinaryData instance already created
        voter_instance, created = Voter.objects.get_or_create(id=1, defaults={
            'first_name': 'John',
            'middle_name': 'Doe',
            'last_name': 'Smith',
            'gender': 'Male',
            'date_of_birth': '2020-10-19',
            'nin_number': 'CF12056743JKL',
            'phone_contact':'0756432871',
            'address':'kitezi',
            'Voter_type': 'Blind-Lame',
            'Polling_station':'Kitezi',
        })

        fingerprint_binary_data_instance, created = FingerprintBinaryData.objects.get_or_create(id=1, defaults={
            'binary_data': b'Some binary data',  # Replace with actual binary data
        })

        fingerprint_instance = Fingerprints.objects.create(
            voter=voter_instance,
            finger_positions={
                'right_thumb': 'some_data',
                'right_index_finger': 'some_data',
                'right_middle_finger': 'some_data',
                'right_ring_finger': 'some_data',
                'right_pinky_finger': 'some_data',
                'left_thumb': 'some_data',
                'left_index_finger': 'some_data',
                'left_middle_finger': 'some_data',
                'left_ring_finger': 'some_data',
                'left_pinky_finger': 'some_data',
            },
            fingerprint_binary_data=fingerprint_binary_data_instance
        )

        self.stdout.write(self.style.SUCCESS('Successfully created Fingerprints instance'))
