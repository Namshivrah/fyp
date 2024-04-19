import requests
import base64
from django.conf import settings
import os
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Voters, PollingStation, Candidates, GENDERS, VOTER_TYPES, POLITICAL_PARTY, ASPIRING_POSTS, FingerPrints, CastedVotes
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
# import Levenshtein
# from IPython.display import Audio

# Enable secure mode (SSL) if you are passing sensitive data
# detectlanguage.configuration.secure = True


# fuction for all voters
def allvoters(request):

    voters = Voters.objects.order_by('-date_created')[:5]

# fuction for all voters
def allvoters(request):

    voters = Voters.objects.all()

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
        time.sleep(2)

        while f.readImage() == False:
            pass

        f.convertImage(FINGERPRINT_CHARBUFFER1)

        result = f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)

        fingerprint_xtics = result

        voter.fingerprint_xtics = fingerprint_xtics
        voter.save()

        return redirect(reverse('voter_details', args=[id]))

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return redirect(reverse('voter_details', args=[id]))
# Create your views here.
def home(request):
    images = [
        'images/cast1.png'
        'images/cast2.png'
        'images/cast3.png'
    ]
    return render(request, 'registration/home.html', {'images': images})

def voter_register(request):
    polling_stations = PollingStation.objects.all()
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
                polling_station = PollingStation.objects.get(id=polling_station_id)
                print(polling_station)
            except PollingStation.DoesNotExist:
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

# sunbird call
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
          
# # ------------------
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

# selecting post to vote for view function
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

# selecting post by the voter in english
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

# reading out the candidates in english
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

# reading out the candidates in luganda
def luganda_vote(request, post_aspired_for):
    candidates = Candidates.objects.filter(post_aspired_for=post_aspired_for).order_by('?')

    # Creating the text Input
    the_text= f"Ab'esimbyewo ku kifo ky'obwa {post_aspired_for}. "
    for candidate in candidates:
        the_text += f"{candidate.full_name()}. "
    
    # Choosing the output format
    audio_url = os.path.join(settings.MEDIA_ROOT, 'output_audio.webm')
    
    print(type(audio_url))
    print(os.path.exists(audio_url))

    with open(audio_url, "wb") as filename:
        data = the_text
        response = requests.post(VOTE_API_URL, headers=headers, json={"inputs": data})
        # print("response content:", response.content)

        if response.status_code == 200:
            filename.write(response.content)
            print('Audio file saved:')
        else:
            print("response failed with status code", response.status_code)

    context = {'candidates': candidates, 'post_aspired_for':post_aspired_for, 'audio_url':audio_url,
               'MEDIA_URL': settings.MEDIA_URL}
    return render(request, 'voting/lugandavote.html',context)
  
# voting via the english language
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




    
          
    
    




import requests
import base64
from django.conf import settings
import os
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Voters, PollingStation, Candidates, GENDERS, VOTER_TYPES, POLITICAL_PARTY, ASPIRING_POSTS, FingerPrints, CastedVotes
from .forms import VoterRegistrationForm, CandidateRegistrationForm
from django.views.decorators.csrf import csrf_exempt
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
# import Levenshtein
# from IPython.display import Audio

# fuction for all voters
def allvoters(request):

    voters = Voters.objects.all()

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
        time.sleep(2)

        while f.readImage() == False:
            pass

        f.convertImage(FINGERPRINT_CHARBUFFER1)

        result = f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)

        fingerprint_xtics = result

        voter.fingerprint_xtics = fingerprint_xtics
        voter.save()

        return redirect(reverse('voter_details', args=[id]))

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return redirect(reverse('voter_details', args=[id]))
# Create your views here.
def home(request):
    images = [
        'images/cast1.png'
        'images/cast2.png'
        'images/cast3.png'
    ]
    return render(request, 'registration/home.html', {'images': images})

def voter_register(request):
    polling_stations = PollingStation.objects.all()
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
                polling_station = PollingStation.objects.get(id=polling_station_id)
                print(polling_station)
            except PollingStation.DoesNotExist:
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

# sunbird call
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
          
# # ------------------
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

# selecting post to vote for view function
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

# selecting post by the voter in english
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

# reading out the candidates in english
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

# reading out the candidates in luganda
def luganda_vote(request, post_aspired_for):
    candidates = Candidates.objects.filter(post_aspired_for=post_aspired_for).order_by('?')

    # Creating the text Input
    the_text= f"Ab'esimbyewo ku kifo ky'obwa {post_aspired_for}. "
    for candidate in candidates:
        the_text += f"{candidate.full_name()}. "
    
    # Choosing the output format
    audio_url = os.path.join(settings.MEDIA_ROOT, 'output_audio.webm')
    
    print(type(audio_url))
    print(os.path.exists(audio_url))

    with open(audio_url, "wb") as filename:
        data = the_text
        response = requests.post(VOTE_API_URL, headers=headers, json={"inputs": data})
        # print("response content:", response.content)

        if response.status_code == 200:
            filename.write(response.content)
            print('Audio file saved:')
        else:
            print("response failed with status code", response.status_code)

    context = {'candidates': candidates, 'post_aspired_for':post_aspired_for, 'audio_url':audio_url,
               'MEDIA_URL': settings.MEDIA_URL}
    return render(request, 'voting/lugandavote.html',context)
  
# voting via the english language
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

    context = {'audio_filename': audio_filename, 'post_aspired_for': post_aspired_for}

    return render(request, 'voting/candidate_engvote.html', context)


# def candidate_engvote(request):
#     audio_filename = 'output_audio.webm'
#     if request.method == 'POST':
#         # Get the audio data from the request
#         if 'audio_data' in request.FILES:
#             audio_file = request.FILES['audio_data']
#             path = default_storage.save('myaudio.webm', audio_file)
#             myfile_path = os.path.join(settings.MEDIA_ROOT, path)
#             with open(myfile_path, "rb") as myfile:
#                 # Send the audio data to the Whisper ASR API
#                 transcript = client.audio.transcriptions.create(
#                     model="whisper-1",
#                     file=myfile,
#                     language="en",
#                     response_format="text"
#                 )
                
#                 print(transcript)
#                 # Get the recognized candidate name from the result
#                 candidate_name = transcript.strip()
                
#                 # Extract the first name from the recognized candidate name
#                 spoken_first_name = candidate_name.split()[0]
                
#                 # Use fuzzy matching to find the closest matching candidate first name
#                 matched_first_name, confidence = process.extractOne(spoken_first_name, Candidates.objects.values_list('first_name', flat=True))
                
#                 # Check if the confidence score is above a certain threshold
#                 if confidence >= 80:
#                     # Find the candidate with the matched first name
#                     candidate = Candidates.objects.filter(first_name=matched_first_name).first()
                    
#                     # Vote for the candidate
#                     if candidate:
#                         dummy_user_id = User.objects.get(username='dummy').id
#                         CastedVotes.objects.create(candidate=candidate, voter_id=dummy_user_id)
#                         # CastedVotes.objects.create(candidate=candidate, voter_id=request.user.id) 
#                         # voter_id=request.user.id requires authentication to add casted vote to database
#                         print(f"Successfully voted for {candidate.full_name()}!")
#                     else:
#                         print("No candidate found with the matched first name")
#                 else:
#                     print("No candidate found with sufficient confidence")
#         else:
#             return JsonResponse({'error': 'No audio data found'})

#     return render(request, 'voting/candidate_engvote.html', {'audio_filename': audio_filename})



    
          
    
    




