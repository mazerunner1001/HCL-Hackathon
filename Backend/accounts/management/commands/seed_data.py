"""
Management command to seed the database with initial data
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User, PatientProfile, ProviderProfile
from wellness.models import HealthTip
from health_info.models import HealthArticle, PrivacyPolicy, FAQ


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create Health Tips
        tips = [
            {
                'title': 'Stay Hydrated',
                'content': 'Aim to drink at least 8 glasses of water per day to keep your body hydrated and functioning optimally.',
                'category': 'hydration',
            },
            {
                'title': 'Get Moving',
                'content': 'Try to get at least 30 minutes of moderate exercise daily. Even a brisk walk counts!',
                'category': 'exercise',
            },
            {
                'title': 'Sleep Well',
                'content': 'Adults need 7-9 hours of sleep per night. Maintain a consistent sleep schedule for better rest.',
                'category': 'sleep',
            },
            {
                'title': 'Eat Your Vegetables',
                'content': 'Include a variety of colorful vegetables in your diet. They provide essential vitamins and minerals.',
                'category': 'nutrition',
            },
            {
                'title': 'Take Mental Breaks',
                'content': 'Practice mindfulness or take short breaks throughout the day to reduce stress and improve focus.',
                'category': 'mental_health',
            },
        ]
        
        for tip_data in tips:
            HealthTip.objects.get_or_create(
                title=tip_data['title'],
                defaults=tip_data
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(tips)} health tips'))
        
        # Create Health Articles
        articles = [
            {
                'title': 'COVID-19 Updates',
                'slug': 'covid-19-updates',
                'summary': 'Stay informed about the latest COVID-19 guidelines and vaccination information.',
                'content': '''<h2>Latest COVID-19 Information</h2>
                <p>Stay up to date with the latest guidelines from health authorities.</p>
                <h3>Prevention Tips</h3>
                <ul>
                    <li>Wash hands frequently with soap and water</li>
                    <li>Wear masks in crowded indoor spaces</li>
                    <li>Maintain physical distance when possible</li>
                    <li>Get vaccinated and boosted as recommended</li>
                </ul>''',
                'category': 'covid',
                'is_featured': True,
            },
            {
                'title': 'Seasonal Flu Prevention',
                'slug': 'seasonal-flu-prevention',
                'summary': 'Learn about steps you can take to prevent the seasonal flu and when to get vaccinated.',
                'content': '''<h2>Protecting Yourself from Seasonal Flu</h2>
                <p>The flu season typically runs from October through May.</p>
                <h3>Prevention Strategies</h3>
                <ul>
                    <li>Get your annual flu vaccine</li>
                    <li>Wash hands regularly</li>
                    <li>Avoid close contact with sick individuals</li>
                </ul>''',
                'category': 'flu',
                'is_featured': True,
            },
            {
                'title': 'Mental Health Awareness',
                'slug': 'mental-health-awareness',
                'summary': 'Explore resources and support options for maintaining good mental health.',
                'content': '''<h2>Taking Care of Your Mental Health</h2>
                <p>Mental health is just as important as physical health.</p>
                <h3>Self-Care Tips</h3>
                <ul>
                    <li>Practice regular exercise</li>
                    <li>Maintain social connections</li>
                    <li>Get adequate sleep</li>
                    <li>Seek professional help when needed</li>
                </ul>''',
                'category': 'mental_health',
                'is_featured': True,
            },
        ]
        
        for article_data in articles:
            HealthArticle.objects.get_or_create(
                slug=article_data['slug'],
                defaults=article_data
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(articles)} health articles'))
        
        # Create Privacy Policy
        PrivacyPolicy.objects.get_or_create(
            version='1.0',
            defaults={
                'title': 'Privacy Policy',
                'content': '''Healthcare Portal Privacy Policy - We protect your health data with HIPAA-compliant security measures.''',
                'effective_date': timezone.now().date(),
                'is_active': True,
            }
        )
        self.stdout.write(self.style.SUCCESS('Created privacy policy'))
        
        # Create FAQs
        faqs = [
            {
                'question': 'How do I track my wellness goals?',
                'answer': 'Log in to your dashboard and navigate to the Wellness Goals section.',
                'category': 'wellness',
                'order': 1,
            },
            {
                'question': 'How is my health data protected?',
                'answer': 'We use industry-standard encryption and follow HIPAA guidelines.',
                'category': 'privacy',
                'order': 2,
            },
        ]
        
        for faq_data in faqs:
            FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults=faq_data
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(faqs)} FAQs'))
        
        self.stdout.write(self.style.SUCCESS('Database seeding completed!'))

