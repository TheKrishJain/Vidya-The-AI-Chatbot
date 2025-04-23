from django.shortcuts import render
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from firstApp.models import ChatMessage, UserInfo
import pandas as pd
import json
import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Min
from django.db.models import OuterRef, Subquery
from datetime import timedelta
from django.utils import timezone
import pandas as pd
from firstApp.models import ChatMessage, UserInfo
from django.shortcuts import render
from django.db.models import Count, Avg, Sum

from django.db.models import Max
from django.db.models import F, ExpressionWrapper, fields
from django.db.models import F
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from firstApp.models import UserInfo  # Import your UserInfo model

from django.utils import timezone
from django.db.models import Count, Avg, Sum, F, ExpressionWrapper, fields
from django.http import JsonResponse
from datetime import timedelta
import pandas as pd


def get_user_details(request):
    users = UserInfo.objects.all().values('first_name','email', 'phone', 'created_at')
    user_list = list(users)
    return JsonResponse(user_list, safe=False)


def unique_user_details(request):
    # Subquery to get the latest created_at for each email
    latest_entry = UserInfo.objects.filter(
        email=OuterRef('email')
    ).order_by('-created_at').values('id')[:1]

    # Fetch unique users by selecting only the latest occurrence of each email
    unique_users = UserInfo.objects.filter(id__in=Subquery(latest_entry)).order_by('-created_at').values(
        'first_name', 'email', 'phone', 'created_at'
    )

    return JsonResponse(list(unique_users), safe=False)



def dashboard(request):
    time_range = request.GET.get('timeRange', 'current')

    # Determine the date range based on selected timeRange
    now = timezone.now()
    if time_range == 'previous':
        start_date = (now.replace(day=1) - timedelta(days=1)).replace(day=1)
        end_date = start_date + timedelta(days=32)
        end_date = end_date.replace(day=1)
    elif time_range == 'last3':
        start_date = now - timedelta(days=90)
        end_date = now
    else:  # default is 'current'
        start_date = now.replace(day=1)
        end_date = now

    chat_data = ChatMessage.objects.filter(received_time__gte=start_date, received_time__lt=end_date)
    user_info = UserInfo.objects.all()

    users_visited = user_info.count()
    inquiries_done = chat_data.count()

    top_questions = chat_data.values('message') \
                            .annotate(count=Count('message')) \
                            .order_by('-count')[:5]

    # Create a list of top 5 questions
    top_5_questions = [{'message': q['message'], 'count': q['count']} for q in top_questions]

    # For single most asked question (first one)
    most_asked_question_text = top_5_questions[0]['message'] if top_5_questions else "No questions yet."

    # Print them for debugging
    print("Top 5 Most Asked Questions:")
    for q in top_5_questions:
        print(f"{q['message']} - Asked {q['count']} times")



    unique_visitors = user_info.values('email').distinct().count()

    total_time_spent = 0
    for user in user_info:
        user_chats = chat_data.filter(userinfo=user)
        if user_chats.exists():
            user_time = user_chats.aggregate(time_spent=Sum(
                ExpressionWrapper(F('reply_time') - F('received_time'), output_field=fields.DurationField())
            ))['time_spent']
            if user_time:
                total_time_spent += user_time.total_seconds()

    avg_time_per_user = round(total_time_spent / users_visited, 2) if users_visited else 0

    avg_response_time = chat_data.aggregate(
        avg_response_time=Avg(ExpressionWrapper(F('reply_time') - F('received_time'), output_field=fields.DurationField()))
    )['avg_response_time']
    avg_response_time_seconds = round(avg_response_time.total_seconds(), 2) if avg_response_time else 0

    if chat_data.exists():
        chat_df = pd.DataFrame(list(chat_data.values('received_time')))
        chat_df['received_time'] = pd.to_datetime(chat_df['received_time'])
        chat_df.set_index('received_time', inplace=True)
        message_count = chat_df.resample('D').size()

        message_data = {
            'labels': message_count.index.strftime('%Y-%m-%d').tolist(),
            'counts': message_count.tolist(),
        }

        line_data = chat_df.resample('D').size()
        line_chart_data = {
            'labels': line_data.index.strftime('%Y-%m-%d').tolist(),
            'counts': line_data.tolist(),
        }
    else:
        message_data = {'labels': [], 'counts': []}
        line_chart_data = {'labels': [], 'counts': []}

    # Placeholder pie data (replace this later with real logic if needed)
    pie_chart_data = {
        'labels': ['FAQs', 'Admissions', 'General Inquiries', 'Other'],
        'counts': [100, 150, 75, 50],
    }

    return JsonResponse({
        'users_visited': users_visited,
        'inquiries_done': inquiries_done,
        'most_asked_question': most_asked_question_text,
        'top_5_questions': top_5_questions,
        'unique_visitors': unique_visitors,
        'avg_time_per_user': avg_time_per_user,
        'avg_response_time': avg_response_time_seconds,
        'message_data': message_data,
        'line_chart_data': line_chart_data,
        'pie_chart_data': pie_chart_data,
    })

# PDF Upload handling
def upload_pdf(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        name = request.POST.get('name')
        alias = request.POST.get('alias')

        if not name or not alias:
            return JsonResponse({'success': False, 'message': 'Name and Alias are required.'})

        # Use MEDIA_ROOT to get the correct directory for file storage
        media_folder = settings.MEDIA_ROOT
        if not os.path.exists(media_folder):
            os.makedirs(media_folder)

        file_path = os.path.join(media_folder, file.name)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        file_url = os.path.join(settings.MEDIA_URL, file.name)

        # Handling course-related JSON files (course.json, course_pdf.json, etc.)
        json_data = {}
        json_file_path = os.path.join(settings.BASE_DIR, 'firstApp', 'static', 'course.json')
        try:
            with open(json_file_path, 'r') as f:
                json_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Handle new file creation or errors gracefully

        # Check if alias exists
        if alias in json_data:
            return JsonResponse({'success': False, 'message': f'Alias "{alias}" already exists.'})

        # Update JSON with file data
        json_data[alias] = {'name': name, 'file_url': file_url}
        try:
            with open(json_file_path, 'w') as f:
                json.dump(json_data, f, indent=4)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error writing to {json_file_path}: {e}'})

        # Update course_pdf.json
        course_pdf_data = {}
        course_pdf_json_path = os.path.join(settings.BASE_DIR, 'firstApp', 'static', 'course_pdf.json')
        try:
            with open(course_pdf_json_path, 'r') as f:
                course_pdf_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        # Update with course file URL
        course_pdf_data[name] = file_url
        try:
            with open(course_pdf_json_path, 'w') as f:
                json.dump(course_pdf_data, f, indent=4)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error writing to {course_pdf_json_path}: {e}'})

        # Update course_alias.json
        course_alias_data = {}
        course_alias_json_path = os.path.join(settings.BASE_DIR, 'firstApp', 'static', 'course_alias.json')
        try:
            with open(course_alias_json_path, 'r') as f:
                course_alias_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        alias_list = [a.strip() for a in alias.split(',')]
        if name in course_alias_data:
            course_alias_data[name].extend(alias_list)
        else:
            course_alias_data[name] = alias_list

        try:
            with open(course_alias_json_path, 'w') as f:
                json.dump(course_alias_data, f, indent=4)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error writing to {course_alias_json_path}: {e}'})

        return JsonResponse({'success': True, 'message': 'PDF uploaded successfully', 'file_url': file_url})

    return JsonResponse({'success': False, 'message': 'No file provided or invalid method.'})

# Other views (login, index, etc.)
def index(request):
    return render(request, 'login.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def login_view(request):
    return render(request, 'login.html')




@csrf_exempt  # Disable CSRF for simplicity (use proper CSRF handling in production)
def send_notification_email(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            subject = data.get('subject')
            message = data.get('message')

            # Fetch all unique users' email addresses
            unique_emails = UserInfo.objects.values_list('email', flat=True).distinct()

            # Send the email to each unique user
            for email in unique_emails:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email='krizzjain@gmail.com',  # Replace with your email
                    recipient_list=[email],  # Send to each unique user
                    fail_silently=False,
                )

            # Return a success response
            return JsonResponse({'status': 'success', 'message': f'Emails sent successfully to {len(unique_emails)} unique users!'})
        except Exception as e:
            # Return an error response if something goes wrong
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)




