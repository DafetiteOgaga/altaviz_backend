from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from django.contrib.auth import authenticate, login, logout, get_user_model
User = get_user_model()
import os
import base64
import requests
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.
try:
    from project_altaviz.myCredentials import credentials
    print(f'credentials from server home dir:: {credentials}')
except ImportError as e:
    print(f"Error importing credentials: {e}")

def sendEmail(user, context, subject):
    # Render HTML content with the context
    context['message'] = f'{context["message"]}\n\n'
    context['reachoutText'] = f'If you have any questions or need assistance, feel free to reach out to our support team.\n\n'
    context['linkText'] = 'Click here\n\n'
    email_body = render_to_string('baseEmail.html', context)

    # Encode the logo image (if you have one)
    logo_path = os.path.join(settings.BASE_DIR, 'app_email', 'emailTemplates', 'altavizLogo.png') # development
    with open(logo_path, 'rb') as file:
        encoded_image = base64.b64encode(file.read()).decode('utf-8')

    email_data = {
        'sender': {'name': 'Altaviz Support Limited', 'email': 'ogagadafetite@gmail.com'},
        'to': [{'email': user.email, 'name': user.first_name}],
        'subject': subject,
        'htmlContent': email_body,
        # 'textContent': f'Password Reset Link: {user.username}',
        'attachment': [
            {
                'content': encoded_image,
                'name': 'logo.png',
                'contentType': 'image/png',
                'disposition': 'inline',  # This is important for inline images
                'cid': 'logo.png',
            },
        ],
    }
    # print(f'email_data: {email_data}') # do not uncomment this line, it will break the code in production

    # Request headers
    headers = {
        'accept': 'application/json',
        # 'api-key': settings.BREVO_API_KEY,  # Make sure your API key is in settings
        'api-key': credentials['BREVOAPIKEY'],  # Make sure your API key is in settings
        'content-type': 'application/json'
    }
    print(f'headers: {headers}')
    return requests.post(credentials['BREVOURL'], headers=headers, json=email_data)

@csrf_exempt
@api_view(['POST'])
def sendEmailToClient(request=None, pk=None):
    print('send email to user')
    if request.method == 'POST':
        print(f'payload: {request.data}')
        try:
            # data = json.loads(request.data)
            print(f'data: {request.data}')
            subject = request.data.get('subject', 'No Subject')
            print(f'subject: {subject}')
            heading = request.data.get('heading', 'No Heading')
            print(f'heading: {heading}')
            message = request.data.get('message', 'No Message')
            print(f'message: {message}')
            support = request.data.get('support', 'No Link')
            print(f'support: {support}')
        except Exception as e:
                print(f'Oopsy! Error: {str(e)}')
                return JsonResponse({'success': False, 'message': str(e)}, status=500)

        user = User.objects.filter(pk=pk).first()
        print(f'user: {user}')

        # Set up the context for rendering
        context = {
            'user': user,
            'heading': heading,
            'message': message,
            'support': support,
        }

        response = sendEmail(user, context, subject)

        # Check response status
        if str(response.status_code).startswith('2'):
            print(f'Email sent successfully: {response.json()}')
            return Response(response.json(), status=status.HTTP_200_OK)  # Return the response in JSON format if successful
        else:
            # Handle failure
            print(f'Failed to send email: {response.status_code} - {response.text}')
            return Response({'error': f'Failed to send email: {response.status_code} - {response.text}'}, status=status.HTTP_417_EXPECTATION_FAILED)

def sendEmailMethod(user=None, data=None):
    print('send email to user')
    subject = data.get('subject', 'No Subject')
    print(f'subject: {subject}')
    heading = data.get('heading', 'No Heading')
    print(f'heading: {heading}')
    message = data.get('message', 'No Message')
    print(f'message: {message}')
    support = data.get('support', 'No Link')
    print(f'support: {support}')

    print(f'user: {user}')

    # Set up the context for rendering
    context = {
        'user': user,
        'heading': heading,
        'message': message,
        'support': support,
    }

    response = sendEmail(user, context, subject)
    
    # Check response status
    if str(response.status_code).startswith('2'):
        print(f'Email sent successfully: {response.json()}')
        return 'success'
    else:
        # Handle failure
        print(f'Failed to send email: {response.status_code}')
        return 'error'
