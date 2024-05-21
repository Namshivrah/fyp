from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import AbstractUser



# Model for storing Addresses
class Address(models.Model):
    village = models.CharField(max_length=100)
    parish = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.parish
    class Meta:
        verbose_name_plural = '1. Addresses'


#Model For storing polling stations
class PollingStation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '2. PollingStations'


# Model For the Voters
GENDERS = [
    ('Male', 'Male'),
    ('Female', 'Female')
]
VOTER_TYPES = [
    ('Blind', 'Blind'),
    ('Blind_and_Mute', 'Blind_and_Mute'),
    ('Blind_and_Lame', 'Blind_and_Lame')
]
class Voters(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True,null=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=GENDERS)
    date_of_birth = models.DateField()
    nin_number = models.CharField(max_length=100)
    phone_contact = models.CharField(max_length=100)
    voter_type = models.CharField(max_length=15, choices=VOTER_TYPES)
    Polling_station = models.ForeignKey(PollingStation, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    # fingerprint xtics
    fingerprint_xtics = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.first_name
    class Meta:
        verbose_name_plural = '3. Voters'
    

# Model For the Voter's Finger Prints
HAND = [
    ('Right_Hand', 'Right_Hand'),
    ('Left_Hand', 'Left_Hand')
]
FINGER = [
    ('Thumb', 'Thumb'),
    ('Index Finger', 'Index Finger'),
    ('Middle Finger', 'Middle Finger'),
    ('Ring Finger', 'Ring Finger'),
    ('Pinky Finger', 'Pinky Finger')
]
class FingerPrints(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    voter = models.OneToOneField(Voters, on_delete=models.CASCADE)
    hand = models.CharField(max_length=10, choices=HAND)
    finger = models.CharField(max_length=13, choices=FINGER)
    fingerprint_image = models.BinaryField(default=b'')
    date_created = models.DateTimeField(auto_now_add=True)
    # def __str__(self):
    #     return self.right_thumb 
    def __str__(self):
        return f"{self.hand} - {self.finger} fingerprint for {self.voter}"


    class Meta:
        verbose_name_plural = '4. FingerPrints'
    

# Model for storing the audio types
AUDIO_TYPES = [
    ('English', 'English'),
    ('Luganda', 'Luganda'),
    ('Kiswahili', 'Kiswahili')
]
class AudioTypes(models.Model):
    audio_type = models.CharField(max_length=10, choices=AUDIO_TYPES)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.audio_type
    class Meta:
        verbose_name_plural = '5. AudioTypes'


# Model For Storing the audio files
class Audios(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    audio_type = models.ForeignKey(AudioTypes, on_delete=models.CASCADE)
    audio_text = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='Audios')
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.audio_text
    class Meta:
        verbose_name_plural = '6. Audios'
    

# Model for storing the Candiates
GENDERS = [
    ('Male', 'Male'),
    ('Female', 'Female')
]
POLITICAL_PARTY = [
    ('NRM', 'NRM'),
    ('FDC', 'FDC'),
    ('NUP', 'NUP')
]
ASPIRING_POSTS = [
    ('President', 'President'),
    ('Member of Parliament', 'Member of Parliament'),
    ('Chairperson LCV', 'Chairperson LCV'),
]
class Candidates(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    profile_pic = models.ImageField(upload_to='Candidates')
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDERS)
    political_party = models.CharField(max_length=100, choices=POLITICAL_PARTY)
    post_aspired_for = models.CharField(max_length=100, choices=ASPIRING_POSTS)
    date_created = models.DateTimeField(auto_now_add=True)

    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def __str__(self):
        return self.full_name()
    # def __str__(self):
    #     return self.first_name
    class Meta:
        verbose_name_plural = '7. Candidates'


# Model to store the casted votes [For tallying]
class CastedVotes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    candidate = models.ForeignKey(Candidates, on_delete=models.CASCADE)
    voter = models.ForeignKey(Voters, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        casted_votes = "Casted Votes"
        return casted_votes
    class Meta:
        verbose_name_plural = '8. CastedVotes'


