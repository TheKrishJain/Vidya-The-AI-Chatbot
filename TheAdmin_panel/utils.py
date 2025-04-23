from django.db.models import Count
from firstApp.models import ChatAnalytics

def get_analytics_summary():
    unique_visitors = ChatAnalytics.objects.values('user_id').distinct().count()
    most_asked_questions = ChatAnalytics.objects.values('question').annotate(
        count=Count('id')).order_by('-count')[:5]
    total_interactions = ChatAnalytics.objects.count()
    
    return {
        'unique_visitors': unique_visitors,
        'most_asked_questions': most_asked_questions,
        'total_interactions': total_interactions,
    }
