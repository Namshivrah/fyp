from sqlite3 import Cursor
import psycopg2
import requests
import base64
from django.conf import settings
import os
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Voters, Polling_Station, Candidates, GENDERS, VOTER_TYPES, POLITICAL_PARTY, ASPIRING_POSTS, FingerPrints, CastedVotes
from .forms import VoterRegistrationForm, CandidateRegistrationForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core.files.base import ContentFile
# from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import serial
from django.http import JsonResponse
from .models import FingerPrints
from django.urls import reverse
import wave
from django.core.files.storage import default_storage
from openai import OpenAI
# from django.template.loader import render_to_string
# import detectlanguage
import random
from django.conf import settings
# from fuzzywuzzy import process
from django.urls import reverse
from django.shortcuts import render, redirect
from pyfingerprint.pyfingerprint import PyFingerprint, FINGERPRINT_CHARBUFFER1, FINGERPRINT_CHARBUFFER2
import time
import string
import time
from time import sleep
from Verifyscanner.comparison import comparison
from Verifyscanner.connect_to_database import connect_to_database, close_database_connection
from datetime import date
from django.http import request
from Verifyscanner.main import get_data_from_database  # Import the get_data_from_database function
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from uuid import UUID



# import Levenshtein
# from IPython.display import Audio


# fuction for all voters
def allvoters(request):

    voters = Voters.objects.all()

# fuction for all voters
def allvoters(request):

    voters = Voters.objects.all().order_by('-created_at')

    content = {
        'voters': voters,
    }

    return render(request, 'registration/allvoters.html', content)

# fuction for a single voter
def voter_details(request,id):

    voter = Voters.objects.get(id=id)

    content = {
        'voter': voter,
    }

    return render(request, 'registration/voter_details.html', content)

def scan_save_fingerprint(request, id):

    try:
        voter = Voters.objects.get(id=id)

        f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

        if not f.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')
        
        print("Place Finger")
        time.sleep(3)

        while f.readImage() == False:
            pass

        f.convertImage(FINGERPRINT_CHARBUFFER1)

        result = f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)

        fingerprint_xtics = result

        voter.fingerprint_xtics = fingerprint_xtics
        voter.save()
        
        messages.success(request, 'Fingerprint saved successfully')

        return redirect(reverse('voter_details', args=[id]))

    except Exception as e:
        messages.error(request, "Operation failed!")
        print('Operation failed!')
        print('Exception message: ' + str(e))
        # messages.info(request, 'Please try again')
        return redirect(reverse('voter_details', args=[id]))



def sessions(request):
    request.session['language_key'] = '1'
    request.session.save()  # Explicitly save the session
    print("Session language_key set to:", request.session['language_key'])
    print("Session ID set to:", request.session.session_key)
    print("Session data after setting language_key:", list(request.session.items()))
    return JsonResponse({'status': 'success', 'message': 'Session created successfully'})

def main(request):
    request.session['language_key'] = '1'
    request.session.save()  # Explicitly save the session
    print("Session language_key set to:", request.session['language_key'])
    print("Session ID set to:", request.session.session_key)
    print("Session keys:", list(request.session.keys()))
    print("Session language_key:", request.session.get('language_key'))
    connection = None  # Initialize the connection variable

    try:
        f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
        if not f.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')

        get_data_from_database()  # Establish a database connection within main

        print("Waiting for finger...")
        sleep(1)

        while not f.readImage():
            pass

        f.convertImage(FINGERPRINT_CHARBUFFER1)
        scanned_xtics = f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)

        data = get_data_from_database()

        for voter in data:
            voter_characteristics1 = eval(voter[2])
            stored_characteristics1 = voter_characteristics1

            if comparison(scanned_xtics, stored_characteristics1) > 85:
                print("sam")
                language_key = request.session.get('language_key')
                print("The language key:", language_key)
                
                request.session['voter_id'] =str(voter[0])  # Assuming the voter's ID is the first element in the voter tuple

                if language_key:
                    # Map the language_key to a view function name
                    language_map = {
                        '1': 'select_post_keypad',  # English language
                        '2': 'select_post_lugkeypad',  # Luganda language
                        '3': 'select_post',  # English keypad
                        '4': 'select_post_lug',  # Luganda keypad
                    }
                    view_name = language_map.get(language_key, None)
                    if view_name:
                        print("The view name:", view_name)
                        # Redirect to the specific page
                        return redirect(reverse(view_name))
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Invalid language key'}, status=400)
                else:
                    return JsonResponse({'status': 'error', 'message': 'Language key not found in session'}, status=400)

        print("Fingerprint did not match.")

    except Exception as e:
        print(f'Exception occurred: {str(e)}')
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    finally:
        if connection:
            close_database_connection(connection)

    return JsonResponse({'status': 'success', 'message': 'Fingerprint matched!!'})

# Create your views here.
def home(request):
    images = [
        'images/cast1.png'
        'images/cast2.png'
        'images/cast3.png'
    ]
    return render(request, 'registration/home.html', {'images': images})

def voter_register(request):
    polling_stations = Polling_Station.objects.all()
    submitted = False
    if request.method =='POST':
        print(1)
        form = VoterRegistrationForm(request.POST)
        if form.is_valid():
            print(2)
            uganda_citizen = request.POST.get('uganda_citizen')

            # Check if the user is not a citizen of Uganda
            if uganda_citizen.lower() == 'no':
                #messages.error(request, 'Only citizens of Uganda can register.')
                return HttpResponse("Only citizens of Uganda can register.")
                return render(request, 'registration/voter.html',{'form':form})
            print(3)
            first_name = request.POST['first_name']
            middle_name = request.POST['middle_name']
            last_name = request.POST['last_name']
            gender = request.POST['gender']
            date_of_birth = request.POST['date_of_birth']
            nin_number = request.POST['nin_number']
            phone_contact = request.POST['phone_contact']
            voter_type = request.POST['voter_type']
            polling_station_id = request.POST.get('Polling_station')
            print(42)
            print(polling_station_id)
            print(41)
            try:
                polling_station = Polling_Station.objects.get(id=polling_station_id)
                print(polling_station)
            except Polling_Station.DoesNotExist:
                messages.error(request, 'Invalid Polling Station.')
                return render(request, 'registration/voter.html', {'polling_stations': polling_stations, 'form':form})
            print(4)
            # Create an instance of the Voters model
            new_voter = Voters(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                gender=gender,
                date_of_birth=date_of_birth,
                nin_number=nin_number,
                phone_contact=phone_contact,
                voter_type=voter_type,
                Polling_station=polling_station,
            )
            print(6)
            if Voters.objects.filter(nin_number=nin_number).exists():
                #messages.error(request, 'Error: NIN number already exists. Please check and try again.')
                return HttpResponse("Error: NIN number already exists. Please check and try again.")
                #context = {'nin_error': True}
                return render(request, 'registration/voter.html',{'form':form}) #context before form
                print(7)
            
            elif Voters.objects.filter(phone_contact=phone_contact).exists():
                #messages.error(request, 'Error: Phone contact already exists. Please check and try again.')
                return HttpResponse("Error: Phone contact already exists. Please check and try again.")
                #context = {'phone_error': True}
                return render(request, 'registration/voter.html',{'form':form}) #context before form
                print(11)
            
            else:
                new_voter.save()
                #messages.success(request, 'Account created successfully')
                return HttpResponseRedirect(reverse('voter_register') + '?submitted=True')
                #return HttpResponse("Thank you for registering")

        else:
            print(form.errors)
    else:
        # If the request method is not POST, create a new form
        print(8)
        form = VoterRegistrationForm()
        if 'submitted' in request.GET:
             submitted = True
        print(9)
    return render(request, 'registration/voter.html',{'form':form, 'submitted':submitted, 'GENDERS': GENDERS, 'polling_stations': polling_stations, 'VOTER_TYPES': VOTER_TYPES,})

      
def candidate(request):
    submitted = False
    if request.method == "POST":
        form = CandidateRegistrationForm(request.POST, request.FILES)
        print(11)
        if form.is_valid():
            uganda_citizen = request.POST.get('uganda_citizen')

            print(1)
            # Check if the user is not a citizen of Uganda
            if uganda_citizen.lower() == 'no':
                messages.error(request, 'Only citizens of Uganda can register.')
                return render(request, 'registration/candidate.html',{'form':form})

            print(2)
            first_name = request.POST['first_name']
            middle_name = request.POST['middle_name']
            last_name = request.POST['last_name']
            gender = request.POST['gender']
            post_aspired_for = request.POST['post_aspired_for']
            political_party = request.POST['political_party']

            print(3)
            # Create an instance of the Voters model
            new_candidate = Candidates(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                gender=gender,
                post_aspired_for=post_aspired_for,
                political_party=political_party,
            )
            
            print(4)
            new_candidate.save()
            #messages.success(request, 'Account created successfully')
            return HttpResponseRedirect(reverse('candidate') + '?submitted=True')
            #return HttpResponse("Thank you for registering.")
        else:
            print(form.errors)
    else:
        print(5)
        # If the request method is not POST, create a new form
        form = CandidateRegistrationForm()
        if 'submitted' in request.GET:
             submitted = True

    return render(request, 'registration/candidate.html',{'form':form, 'submitted':submitted, 'GENDERS': GENDERS, 'ASPIRING_POSTS': ASPIRING_POSTS, 'POLITICAL_PARTY': POLITICAL_PARTY,})
       

def exit(request):
    images = [
        'images/voter1.jpg'
         'images/voter2.png'
    ]
    return render(request, 'registration/exit.html', {'images': images})

@csrf_exempt
def receive_fingerprint_image(request):


    if request.method == 'POST':
        fingerprint_data = request.body
        #fingerprint_data = ser.readline().decode().strip()
        print(21)
        # try:
        #     fingerprint_image_data = request.POST.get('fingerprint_image')
        #     hand = request.POST.get('hand')
        #     finger = request.POST.get('finger')
        #     print(22)

            # Decode the base64-encoded fingerprint image data
        fingerprint_image_binary = base64.b64decode(fingerprint_data)

            # Save the fingerprint data to the database
        fingerprint = FingerPrints.objects.create(
            voter=request.user.voters,  # Assuming you have authentication and a user-voters relationship
            hand="hand",
            finger="finger",
            fingerprint_image=ContentFile(fingerprint_image_binary,name='fingerprint_image.jpg')
        )

            # Send the data as a JSON-encoded string
            # ser.write(str(data).encode())
            # print(23)
            # Add a delay to allow the Arduino to process the data
            # time.sleep(2)
        print(28)

        return JsonResponse({'success': True, 'message': 'Fingerprint saved successfully.'})

        # except Exception as e:
        #     print(24)
        #     return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
    else:
        print(25)
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def store_fingerprint(request):
    if request.method == 'POST':
        hand = request.POST.get('hand')
        finger = request.POST.get('finger')
        fingerprint_image = request.POST.get('fingerprint_image')
        FingerPrints.objects.create(hand=hand, finger=finger, fingerprint_image=fingerprint_image)
        return JsonResponse({'message': 'Fingerprint stored successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def scanner(request):
    return render(request, 'verification/finger.html')

# sunbird call STT
def sunbird(request, id):
    print("this is =>", id)

    with open(id, "rb") as filename:
        data = filename.read()
    response = requests.post(API_URL, headers=headers, data=data)
    response=response.json()
    print('Response returned:', response)

    if "text" in response:
        response_text = response['text']
        print(response_text)
        os.remove(id)
        return JsonResponse({'text': response_text})
    else:
        print(response['error'])

    return JsonResponse({'error': 'No audio data there'})
          
# # ------------------ English STT
def language(request):
    if request.method == 'POST':
        # Get the audio data from the request
        if 'audio_data' in request.FILES:
            audio_file = request.FILES['audio_data']
            # logger.info(f"Received audio data: {audio_file.name}, size: {audio_file.size} bytes, type: {audio_file.content_type}")
            # Save the audio data to a file
            path = default_storage.save('myaudio.webm', audio_file)
            myfile_path = os.path.join(settings.MEDIA_ROOT, path)
            with open(myfile_path, "rb") as myfile:
                # Send the audio data to the Whisper ASR API
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=myfile,
                    language="en",
                    response_format="text"      
                )
                # logger.info(f"Received transcript: {transcript}")
                print(transcript)
                if "English" in transcript:
                    # os.remove(myfile_path)
                    return JsonResponse({'text': transcript}) 
                else:
                    print("Path is", myfile_path)
                    return redirect("sunbird",id=myfile_path)
                  
        else:
            return JsonResponse({'error': 'No audio data found'})
    
    return render(request, 'verification/lang.html')

# selecting post to vote for view function TTS
def select_post(request):

    posts = Candidates.objects.values_list('post_aspired_for', flat=True).distinct()
    # Creating the text Input
    the_text= f"Available Posts to Vote For: "
    for post in posts:
        the_text += f"{post}. "

    # Output format
    # audio_filename =   # You can choose a desired filename
    audio_url = os.path.join(settings.MEDIA_ROOT, 'output_audio.webm')
    
    print(type(audio_url))
    print(os.path.exists(audio_url))
    with open(audio_url, 'wb') as f:
        # Creating Audio Response
        response = client.audio.speech.create(
        model="tts-1",
        voice = "onyx",
        input = the_text
        )

        print(response)
 
        content = response.content       
        f.write(content)
   
    url = reverse('posteng_choice')  # Replace 'english_vote' with the name of your view
    context = {'url':url, 'posts': posts,  'audio_url':audio_url, 'MEDIA_URL': settings.MEDIA_URL}
    
    return render(request, 'voting/select_post.html',context)

# Valaibale posts luganda version TTS
def select_post_lug(request):

    posts = Candidates.objects.values_list('post_aspired_for', flat=True).distinct()
    # Creating the text Input
    the_text= f"Ebiffo eby'okuloondebwa: "
    for post in posts:
        the_text += f"{post}. "

    # Creating Audio Response
    response =  requests.post(VOTE_API_URL, headers=headers, json={"inputs": the_text})

    # Output format
    # audio_filename =   # You can choose a desired filename
    audio_url = os.path.join(settings.MEDIA_ROOT, 'output_audio.webm')
    
    print(type(audio_url))
    print(os.path.exists(audio_url))
    with open(audio_url, 'wb') as f:
        content = response.content       
        f.write(content)
   
    lug_url = reverse('postlug_choice')  # Replace 'english_vote' with the name of your view

    context = {'posts': posts,  'audio_url':audio_url, 'MEDIA_URL': settings.MEDIA_URL, 'lug_url': lug_url}

    return render(request, 'voting/select_post_lug.html', context)

# selecting post by the voter in english STT
def posteng_choice(request):
    audio_filename = 'output_audio.webm'
    if request.method == 'POST':
        # Get the audio data from the request
        if 'audio_data' in request.FILES:
            audio_file = request.FILES['audio_data']
            path = default_storage.save('myaudio.webm', audio_file)
            myfile_path = os.path.join(settings.MEDIA_ROOT, path)
            with open(myfile_path, "rb") as myfile:
                # Send the audio data to the Whisper ASR API
                # Get the transcipt from the Whisper ASR API
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=myfile,
                    language="en",
                    response_format="text"
                )

                print(f"Transcript: {transcript}")

                # Get the Post Aspired for from the Whisper STT API
                post_aspired_for = transcript
                # To remove any spaces
                post_aspired_for = post_aspired_for.strip().translate(str.maketrans('', '', string.punctuation))
                print(f"Post aspired for: {post_aspired_for}")  
                # Generate the English Vote view with the post aspired for arguement
                url = reverse('english_vote', args=[post_aspired_for])

                # redirect to the generated URL 
                return JsonResponse({'url': url})
        else:
            return JsonResponse({'error': 'No audio data found'})

    return render(request, 'voting/posteng_choice.html', {'audio_filename': audio_filename})


# selecting post by the voter in luganda STT
# defining a dictionary that mapsa luganda words to english

luganda_to_english = {
    "njagala pulezidenti": "President",
    "njagala mmemba wa paalamenti": "Member of Parliament",
    "njagala kyeyapaasoni": "Chairperson LCV",
}

def postlug_choice(request):
    audio_filename = 'output_audio.webm'
    if request.method == 'POST':
        if 'audio_data' in request.FILES:
            audio_file = request.FILES['audio_data']
            path = default_storage.save('myaudio.webm', audio_file)
            myfile_path = os.path.join(settings.MEDIA_ROOT, path)
            
            with open(myfile_path, "rb") as filename:
                data = filename.read()
            response = requests.post(API_URL, headers=headers, data=data)
            response=response.json()
            print('Response returned:', response)

            if "text" in response:
                response_text = response['text']
                post_aspired_for = response_text

                # To remove any spaces
                post_aspired_for = post_aspired_for.strip().translate(str.maketrans('', '', string.punctuation))
                
                # Translate the Luganda word to English
                post_aspired_for = luganda_to_english.get(post_aspired_for, post_aspired_for)
                print(f"Post aspired for: {post_aspired_for}")

                
                # Generate the Luganda Vote view with the post aspired for arguement
                url = reverse('luganda_vote', args=[post_aspired_for])
                
                os.remove(myfile_path)
                return JsonResponse({'url': url})
            else:
                print(response['error'])

        else:
            return JsonResponse({'error': 'No audio data there'})

    return render(request, 'voting/postlug_choice.html', {'audio_filename': audio_filename})


# reading out the candidates in english TTS
def english_vote(request,post_aspired_for):
    candidates = Candidates.objects.filter(post_aspired_for=post_aspired_for).order_by('?')
    # Creating the text Input
    the_text= f"Candidates for {post_aspired_for}. "
    for candidate in candidates:
        the_text += f"{candidate.full_name()}. "

    # Output format
    # audio_filename =   # You can choose a desired filename
    audio_url = os.path.join(settings.MEDIA_ROOT, 'output_audio.webm')
    
    print(type(audio_url))
    print(os.path.exists(audio_url))
    with open(audio_url, 'wb') as f:
        # Creating Audio Response
        response = client.audio.speech.create(
        model="tts-1",
        voice = "onyx",
        input = the_text
        )
        content = response.content
        f.write(content)   

    # Generate the Candidate Vote view with the post aspired for arguement
    redirect_url = reverse('candidate_engvote', args=[post_aspired_for]) 
    print(f"Redirect URL: {redirect_url}")
         
    context = {'candidates': candidates, 'post_aspired_for':post_aspired_for, 'audio_url':audio_url,
                    'MEDIA_URL': settings.MEDIA_URL, 'redirect_url': redirect_url}
    
    return render(request, 'voting/englishvote.html', context)

# reading out the candidates in luganda TTS
# define the dictionary that maps numbers to Luganda words
numbers_to_luganda = {
    1: "emu",
    2: "bbiri",
    3: "ssatu",
    4: "nnya",
}

def luganda_vote(request, post_aspired_for):
    candidates = Candidates.objects.filter(post_aspired_for=post_aspired_for).order_by('?')

    # Creating the text Input
    the_text= f"Ab'esimbyewo ku kifo ky'obwa {post_aspired_for}. "
    for i, candidate in enumerate(candidates, start=1):
        # look up the Luganda equivalent for the number
        number_in_luganda = numbers_to_luganda.get(i, str(i))
        the_text += f"{number_in_luganda}:  {candidate.full_name()}, "
    
    # Creating Audio Response
    response = requests.post(VOTE_API_URL, headers=headers, json={"inputs": the_text})

    # Choosing the output format
    audio_url = os.path.join(settings.MEDIA_ROOT, 'output_audio.webm')
    
    print(type(audio_url))
    print(os.path.exists(audio_url))

    with open(audio_url, "wb") as filename:
        content = response.content       
        filename.write(content)

        # if response.status_code == 200:
        #     filename.write(response.content)
        #     print('Audio file saved:')

            
        # else:
        #     print("response failed with status code", response.status_code)

    redirect_url = reverse('candidate_lugvote', args=[post_aspired_for]) 
    print(f"Redirect URL: {redirect_url}")

    context = {'candidates': candidates, 'post_aspired_for':post_aspired_for, 'audio_url':audio_url,
               'MEDIA_URL': settings.MEDIA_URL, 'redirect_url': redirect_url}
    
    return render(request, 'voting/lugandavote.html',context)
  
# voting via the english language STT
def candidate_engvote(request, post_aspired_for):
    audio_filename = 'output_audio.webm'
    if request.method == 'POST':
        # Get the audio data from the request
        if 'audio_data' in request.FILES:
            audio_file = request.FILES['audio_data']
            path = default_storage.save('myaudio.webm', audio_file)
            myfile_path = os.path.join(settings.MEDIA_ROOT, path)
            with open(myfile_path, "rb") as myfile:
                # Send the audio data to the Whisper ASR API
                spoken_numbers = {
                    "one": 1,
                    "two": 2,
                    "three": 3,
                    "four": 4,
                }
                # Get the transcipt from the Whisper ASR API
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=myfile,
                    language="en",
                    response_format="text"
                ).strip().lower()

                # To remove any spaces
                transcript = transcript.strip().translate(str.maketrans('', '', string.punctuation))
                print(f"Transcript: {transcript}")

                # Convert the transcript to an integer
                spoken_candidate_number = spoken_numbers.get(transcript.lower())
                print(spoken_candidate_number)

                # Get the list of candidates for the specific post aspired for
                print(f"Post aspired for: {post_aspired_for}")
                candidates_for_post = Candidates.objects.filter(post_aspired_for=post_aspired_for)
                
                # Loop through the candidates and print their details
                for candidate in candidates_for_post:
                    print(candidate.full_name())

                print(f"Spoken candidate number: {spoken_candidate_number}")  # Add this line
                print(f"Number of candidates: {len(candidates_for_post)}")  # Add this line

                # Check if the spoken candidate number is within the range of the candidates list
                if spoken_candidate_number is None or  spoken_candidate_number > len(candidates_for_post):
                    print("Invalid candidate number")
                    return JsonResponse({'error':'Invalid candidate number'}) 

                # Checking if the voter has already voted inorder to prevent revoting
                if CastedVotes.objects.filter(voter_id=request.user.id).exists():
                    print("You have already voted")
                    return JsonResponse({'error':'You have already voted'})


                # Check if the user is authenticated
                voter_id = request.POST['voter_id']
                try:
                    voter = Voters.objects.get(id=voter_id)
                except Voters.DoesNotExist:
                    print("Voter does not exist")
                    return JsonResponse({'error':'Voter does not exist'})


                # Get the selected candidate
                candidate = candidates_for_post[spoken_candidate_number - 1]
                print(f"Candidate: {candidate}")
                print(f"Voter ID: {request.user.id}")
                # Vote for the candidate
                CastedVotes.objects.create(candidate=candidate, voter_id=request.user)
                
                print(f"Successfully voted for {candidate.full_name()}!")
                return JsonResponse({'messages': f'Successfully voted for {candidate.full_name()}!'})
        else:
            return JsonResponse({'error': 'No audio data found'})


    context = {'audio_filename': audio_filename, 'post_aspired_for': post_aspired_for, 'voter':voter}

    return render(request, 'voting/candidate_engvote.html', context)


# voting via the luganda language STT
def candidate_lugvote(request, post_aspired_for):
    audio_filename = 'output_audio.webm'        
    if request.method == 'POST':
        # Get the audio data from the request
        if 'audio_data' in request.FILES:
            audio_file = request.FILES['audio_data']
            path = default_storage.save('myaudio.webm', audio_file)
            myfile_path = os.path.join(settings.MEDIA_ROOT, path)
            with open(myfile_path, "rb") as myfile:
                data = myfile.read()
                # Send the audio data to the Whisper ASR API
                spoken_numbers = {
                    "njagala nnamba emu": 1,
                    "njagala nnamba bbiri": 2,
                    "njagala nnamba ssatu": 3,
                    "njagala nnamba nnya": 4,
                }
                # Get the transcipt from the Whisper ASR API
                response = requests.post(API_URL, headers=headers, data=data)
                response=response.json()
                print('Response returned:', response)
                
                # Assign a default value to spoken_candidate_number
                spoken_candidate_number = None

                if "text" in response:
                    response_text = response['text']
                    transcript = response_text.strip().lower()
                    print(transcript)
                    # To remove any spaces  
                    transcript = transcript.strip().translate(str.maketrans('', '', string.punctuation))
                    print(f"Transcript: {transcript}")

                    # Convert the transcript to an integer
                    spoken_candidate_number = spoken_numbers.get(transcript.lower())
                    print(spoken_candidate_number)

                # Get the list of candidates for the specific post aspired for
                print(f"Post aspired for: {post_aspired_for}")
                candidates_for_post = Candidates.objects.filter(post_aspired_for=post_aspired_for)

                # Loop through the candidates and print their details
                for candidate in candidates_for_post:
                    print(candidate.full_name())
                
                print(f"Spoken candidate number: {spoken_candidate_number}")  # Add this line
                print(f"Number of candidates: {len(candidates_for_post)}")

                # Check if the spoken candidate number is within the range of the candidates list
                if spoken_candidate_number is None or  spoken_candidate_number > len(candidates_for_post):
                    print("Invalid candidate number")
                    return JsonResponse({'error':'Invalid candidate number'})
                
                # Checking if the voter has already voted inorder to prevent revoting
                if CastedVotes.objects.filter(voter_id=request.user.id).exists():
                    print("You have already voted")
                    return JsonResponse({'error':'You have already voted'})
                # Get the selected candidate
                candidate = candidates_for_post[spoken_candidate_number - 1]
                print(f"Candidate: {candidate}")
                print(f"Voter ID: {request.user.id}")
                # Vote for the candidate
                CastedVotes.objects.create(candidate=candidate, voter_id=request.user)

                print(f"Successfully voted for {candidate.full_name()}!")

                os.remove(myfile_path)

                return JsonResponse({'messages': f'Successfully voted for {candidate.full_name()}!'})
        else:
            return JsonResponse({'error': 'No audio data found'})

    context = {'audio_filename': audio_filename, 'post_aspired_for': post_aspired_for}
    
    return render(request, 'voting/candidate_lugvote.html', context)

    
  # -------------------- KEYPAD ACTIVITIES ----------------------------


# -------------------- KEYPAD ACTIVITIES ----------------------------

@csrf_exempt
def language_keypad(request):
    
    if request.method == 'POST':
        key_pressed = request.POST.get('key_pressed')
        # Perform actions based on the key pressed
        # For example, you can log the key pressed, trigger further instructions, etc.
        return JsonResponse({'status': 'success'})

    elif request.method == 'GET':
        # Handle GET requests
        return render(request, 'verification/keypadlanguage.html')
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    return render(request, 'verification/keypadlanguage.html')        

#posts are read out in English using keypad
def select_post_keypad(request):
    posts = Candidates.objects.values_list('post_aspired_for', flat=True).distinct()
    # Creating the text Input
    the_text= f"Available Posts to Vote For: "
    for i, post in enumerate(posts, start=1):
        the_text += f"{i}: {post},"

    # Output format
    # audio_filename =   # You can choose a desired filename
    audio_url = os.path.join(settings.MEDIA_ROOT, 'output_audio.webm')
    
    print(type(audio_url))
    print(os.path.exists(audio_url))
    with open(audio_url, 'wb') as f:
        # Creating Audio Response
        response = client.audio.speech.create(
        model="tts-1",
        voice = "onyx",
        input = the_text
        )

        print(response)
 
        content = response.content       
        f.write(content)
   
    url = reverse('posteng_choice_keypad')  # Replace 'english_vote' with the name of your view
    context = {'url':url, 'posts':list(posts),  'audio_url':audio_url, 'MEDIA_URL': settings.MEDIA_URL}
    
    return render(request, 'voting/select_post_keypad.html',context)    
    
# Valaibale posts luganda 
numbers_to_luganda = {
    1: "emu",
    2: "bbiri",
    3: "ssatu",
}
def select_post_lugkeypad(request):
    posts = Candidates.objects.values_list('post_aspired_for', flat=True).distinct()
    # Creating the text Input
    the_text= f"Ebiffo eby'okuloondebwa:  "
    for i, post in enumerate(posts, start=1):
        # look up the Luganda equivalent for the number
        number_in_luganda = numbers_to_luganda.get(i, str(i))
        the_text += f"{number_in_luganda}:  {post}, "

    # Creating Audio Response
    response =  requests.post(VOTE_API_URL, headers=headers, json={"inputs": the_text})

    # Output format
    # audio_filename =   # You can choose a desired filename
    audio_url = os.path.join(settings.MEDIA_ROOT, 'output_audio.webm')
    
    print(type(audio_url))
    print(os.path.exists(audio_url))
    with open(audio_url, 'wb') as f:
        content = response.content       
        f.write(content)
   
    lug_url = reverse('postlug_choice_keypad')  # Replace 'english_vote' with the name of your view

    context = {'posts': list(posts),  'audio_url':audio_url, 'MEDIA_URL': settings.MEDIA_URL, 'lug_url': lug_url}

    return render(request, 'voting/select_post_lugkeypad.html', context)

# select post using keypad
@csrf_exempt
def posteng_choice_keypad(request):
    # posts = Candidates.objects.values_list('post_aspired_for', flat=True).distinct()

    post_number_map = {
    '1': 'President',
    '2': 'Member of Parliament',
    '3': 'Chairperson LCV',
    # Add more mappings as needed
    }
    if request.method == 'POST':
        # data = json.loads(request.body)
        key_pressed = request.POST.get('key_pressed')
        selected_post = post_number_map.get(key_pressed)
        print(f"Selected post: {selected_post}")

        if selected_post:
            # Perform actions based on the selected post
            url = reverse('english_vote_keypad', args=[selected_post])
            return JsonResponse({'status': 'success', 'selected_post': selected_post, 'url': url})

        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid key pressed'})

    elif request.method == 'GET':
        # Handle GET requests
        return render(request, 'voting/posteng_choice_keypad.html')
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    return render(request, 'voting/posteng_choice_keypad.html')

# selecting post by the voter in luganda 
@csrf_exempt
def postlug_choice_keypad(request):
    # posts = Candidates.objects.values_list('post_aspired_for', flat=True).distinct()

    post_number_map = {
    '1': 'President',
    '2': 'Member of Parliament',
    '3': 'Chairperson LCV',
    # Add more mappings as needed
    }
    if request.method == 'POST':
        # data = json.loads(request.body)
        key_pressed = request.POST.get('key_pressed')
        selected_post = post_number_map.get(key_pressed)
        print(f"Selected post: {selected_post}")

        if selected_post:
            # Perform actions based on the selected post
            url = reverse('luganda_vote_keypad', args=[selected_post])
            return JsonResponse({'status': 'success', 'selected_post': selected_post, 'url': url})

        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid key pressed'})

    elif request.method == 'GET':
        # Handle GET requests
        return render(request, 'voting/postlug_choice_keypad.html')
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    return render(request, 'voting/postlug_choice_keypad.html')

# reading out candidadte in English TTS under keypad
def english_vote_keypad(request, post_aspired_for):
    candidates = Candidates.objects.filter(post_aspired_for=post_aspired_for).order_by('?')
    # Creating the text Input
    the_text= f"Candidates for {post_aspired_for}. "
    for i, candidate in enumerate(candidates, start=1):
        the_text += f"{i}: {candidate.full_name()}, "

    # Output format
    # audio_filename =   # You can choose a desired filename
    audio_url = os.path.join(settings.MEDIA_ROOT, 'output_audio.webm')
    
    print(type(audio_url))
    print(os.path.exists(audio_url))
    with open(audio_url, 'wb') as f:
        # Creating Audio Response
        response = client.audio.speech.create(
        model="tts-1",
        voice = "onyx",
        input = the_text
        )
        content = response.content
        f.write(content)   

    # Generate the Candidate Vote view with the post aspired for arguement
    redirect_url = reverse('candidate_engvote_keypad', args=[post_aspired_for]) 
    print(f"Redirect URL: {redirect_url}")
         
    context = {'candidates': candidates, 'post_aspired_for':post_aspired_for, 'audio_url':audio_url,
                    'MEDIA_URL': settings.MEDIA_URL, 'redirect_url': redirect_url}
    return render(request, 'voting/englishvote_keypad.html', context)

# reading out candidadte in Luganda TTS under keypad
numbers_to_luganda = {
    1: "emu",
    2: "bbiri",
    3: "ssatu",
    4: "nnya",
}
def luganda_vote_keypad(request, post_aspired_for):
    candidates = Candidates.objects.filter(post_aspired_for=post_aspired_for).order_by('?')

    # Creating the text Input
    the_text= f"Ab'esimbyewo ku kifo ky'obwa {post_aspired_for}. "
    for i, candidate in enumerate(candidates, start=1):
        # look up the Luganda equivalent for the number
        number_in_luganda = numbers_to_luganda.get(i, str(i))
        the_text += f"{number_in_luganda}:  {candidate.full_name()}, "
    
    # Creating Audio Response
    response = requests.post(VOTE_API_URL, headers=headers, json={"inputs": the_text})

    # Choosing the output format
    audio_url = os.path.join(settings.MEDIA_ROOT, 'output_audio.webm')
    
    print(type(audio_url))
    print(os.path.exists(audio_url))

    with open(audio_url, "wb") as filename:
        content = response.content       
        filename.write(content)

        # if response.status_code == 200:
        #     filename.write(response.content)
        #     print('Audio file saved:')

            
        # else:
        #     print("response failed with status code", response.status_code)

    redirect_url = reverse('candidate_lugvote_keypad', args=[post_aspired_for]) 
    print(f"Redirect URL: {redirect_url}")

    context = {'candidates': candidates, 'post_aspired_for':post_aspired_for, 'audio_url':audio_url,
               'MEDIA_URL': settings.MEDIA_URL, 'redirect_url': redirect_url}
    
    return render(request, 'voting/lugandavote.html',context)

# selecting desired candidate using keypad
@csrf_exempt
def candidate_engvote_keypad(request, post_aspired_for):
    if not post_aspired_for:
        return JsonResponse({'error':'Post aspired for is not provided'})

    press_button = {
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,

    }


    if request.method == 'POST':
        key_pressed = request.POST.get('key_pressed')
        voted_candidate = press_button.get(key_pressed)
        print(f"Voted candidate: {voted_candidate}")

        if voted_candidate:
            # Get the list of candidates for the specific post aspired for
            print(f"Post aspired for: {post_aspired_for}")
            candidates_for_post = Candidates.objects.filter(post_aspired_for=post_aspired_for)

            # Loop through the candidates and print their details
            for candidate in candidates_for_post:
                print(candidate.full_name())

            print(f"Voted candidate: {voted_candidate}")  # Add this line
            print(f"Number of candidates: {len(candidates_for_post)}")  # Add this line


            # Check if the voted_candidate is within the range of the candidates list
            if voted_candidate is None or  voted_candidate > len(candidates_for_post):
                print("Invalid candidate number")
                return JsonResponse({'error':'Invalid candidate number'}) 


            # Checking if the voter has already voted inorder to prevent revoting
            if CastedVotes.objects.filter(voter_id=request.user.id).exists():
                print("You have already voted")
                return JsonResponse({'error':'You have already voted'})

            # Get the selected candidate
            candidate = candidates_for_post[voted_candidate - 1]
            print(f"Candidate: {candidate}")
            

            # get voter id from session or request
            voter_id = UUID(request.session.get('voter_id', ''))
            if not voter_id:
                return JsonResponse({'error': 'Voter ID not found'})
            try:
                # fetch the voter from the database
                voter = Voters.objects.get(id=voter_id)
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'error','message': 'Voter does not exist'}, status=404)
            
            print(f"Voter ID: {voter.id}")

            # Vote for the candidate but the voter votes only once 
            # Check if the voter has already voted
            existing_vote = CastedVotes.objects.filter(voter_id=voter_id).first()
            if existing_vote and existing_vote.candidate is not None:
                return JsonResponse({'status': 'error', 'message': 'Voter has already cast a vote'}, status=400)
            else:
                # If the voter has not voted, cast the vote
                CastedVotes.objects.create(candidate=candidate, voter_id=voter_id)
                print(f"Successfully voted for {candidate.full_name()}!")
                return JsonResponse({'status': 'success', 'voted_candidate': voted_candidate, 'post_aspired_for': post_aspired_for})

        else:
            print("Invalid key pressed")
            return JsonResponse({'status': 'error', 'message': 'Invalid key pressed'})

    elif request.method == 'GET':
        # Handle GET requests
        return render(request, 'voting/candidate_engvote_keypad.html', {'post_aspired_for': post_aspired_for})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
        # Add an indented block here

    return render(request, 'voting/candidate_engvote_keypad.html', {'post_aspired_for': post_aspired_for})

# selecting desired candidate using keypad
@csrf_exempt
def candidate_lugvote_keypad(request, post_aspired_for):
    if not post_aspired_for:
        return JsonResponse({'error':'Post aspired for is not provided'})

    press_button = {
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,

    }


    if request.method == 'POST':
        key_pressed = request.POST.get('key_pressed')
        voted_candidate = press_button.get(key_pressed)
        print(f"Voted candidate: {voted_candidate}")

        if voted_candidate:
            # Get the list of candidates for the specific post aspired for
            print(f"Post aspired for: {post_aspired_for}")
            candidates_for_post = Candidates.objects.filter(post_aspired_for=post_aspired_for)

            # Loop through the candidates and print their details
            for candidate in candidates_for_post:
                print(candidate.full_name())

            print(f"Voted candidate: {voted_candidate}")  # Add this line
            print(f"Number of candidates: {len(candidates_for_post)}")  # Add this line

            # Check if the voted_candidate is within the range of the candidates list
            if voted_candidate is None or  voted_candidate > len(candidates_for_post):
                print("Invalid candidate number")
                return JsonResponse({'error':'Invalid candidate number'}) 


            # Checking if the voter has already voted inorder to prevent revoting
            if CastedVotes.objects.filter(voter_id=request.user.id).exists():
                print("You have already voted")
                return JsonResponse({'error':'You have already voted'})

            # Get the selected candidate
            candidate = candidates_for_post[voted_candidate - 1]
            print(f"Candidate: {candidate}")
            print(f"Voter ID: {request.user.id}")

            # Vote for the candidate
            CastedVotes.objects.create(candidate=candidate, voter_id=request.user)

            print(f"Successfully voted for {candidate.full_name()}!")

            return JsonResponse({'status': 'success', 'voted_candidate': voted_candidate, 'post_aspired_for': post_aspired_for})

        else:
            print("Invalid key pressed")
            return JsonResponse({'status': 'error', 'message': 'Invalid key pressed'})

    elif request.method == 'GET':
        # Handle GET requests
        return render(request, 'voting/candidate_lugvote_keypad.html', {'post_aspired_for': post_aspired_for})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
        # Add an indented block here

    return render(request, 'voting/candidate_lugvote_keypad.html', {'post_aspired_for': post_aspired_for})



# ------------------TALLYING ACTIVITIES ----------------------------
def tally_votes(request):
     # Query the database for all votes and count the number of votes for each candidate
    # vote_counts = CastedVotes.objects.values('candidate').annotate(vote_count=Count('candidate'))

    # # Covert the Queryset to a list of dictionaries
    # vote_counts = list(vote_counts)

    # Get the list of candidates
    candidates = Candidates.objects.all()
    # Create a dictionary to store the votes for each candidate
        # votes = CastedVotes.objects.values('candidate').annotate(vote_count=Count('candidate'))
    votes = {}
     # Covert the Queryset to a list of dictionaries
    # votes = list(votes)

    # Loop through the candidates and get the number of votes for each candidate
    for candidate in candidates:
        votes[candidate.full_name()] = candidate.castedvotes_set.count()
    # Sort the votes in descending order
    sorted_votes = dict(sorted(votes.items(), key=lambda item: item[1], reverse=True))
    # Get the winner
    winner = next(iter(sorted_votes))
    # Get the number of votes for the winner
    winning_votes = sorted_votes[winner]
    # Get the total number of votes cast
    total_votes = sum(votes.values())
    context = {'votes': sorted_votes, 'winner': winner, 'winning_votes': winning_votes, 'total_votes': total_votes}
    return render(request, 'tallying/tallying.html', context)
