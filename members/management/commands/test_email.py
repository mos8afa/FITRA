"""
Django management command to test email configuration
Usage: python manage.py test_email your-email@example.com
"""

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import smtplib


class Command(BaseCommand):
    help = 'Test email configuration by sending a test email'

    def add_arguments(self, parser):
        parser.add_argument(
            'recipient',
            nargs='?',
            type=str,
            help='Email address to send test email to'
        )
        parser.add_argument(
            '--check-only',
            action='store_true',
            help='Only check configuration without sending email',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO("=" * 60))
        self.stdout.write(self.style.HTTP_INFO("FITRA EMAIL CONFIGURATION TEST"))
        self.stdout.write(self.style.HTTP_INFO("=" * 60))
        
        # Display current configuration
        self.stdout.write("\n" + self.style.HTTP_INFO("Current Email Configuration:"))
        self.stdout.write(f"  Backend: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"  Host: {settings.EMAIL_HOST}")
        self.stdout.write(f"  Port: {settings.EMAIL_PORT}")
        self.stdout.write(f"  Use TLS: {settings.EMAIL_USE_TLS}")
        self.stdout.write(f"  From Email: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"  Host User: {settings.EMAIL_HOST_USER}")
        
        # Check if using console backend
        if 'console' in settings.EMAIL_BACKEND.lower():
            self.stdout.write(self.style.WARNING(
                "\n⚠️  Using console backend - emails will print to console, not send"
            ))
            if not options['check_only']:
                self.stdout.write(
                    "To send real emails, change EMAIL_BACKEND in settings.py to:\n"
                    "EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'"
                )
            return
        
        # Test SMTP connection
        self.stdout.write("\n" + self.style.HTTP_INFO("Testing SMTP Connection..."))
        
        try:
            if settings.EMAIL_USE_TLS:
                server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10)
            
            self.stdout.write(self.style.SUCCESS("✓ Connected to SMTP server"))
            
            # Try authentication
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                self.stdout.write(self.style.SUCCESS("✓ SMTP authentication successful"))
            
            server.quit()
            self.stdout.write(self.style.SUCCESS("✓ SMTP connection test passed"))
            
        except smtplib.SMTPAuthenticationError as e:
            self.stdout.write(self.style.ERROR(f"✗ SMTP Authentication failed: {e}"))
            self.stdout.write(self.style.WARNING("\nPossible solutions:"))
            self.stdout.write("  1. Check if email and password are correct")
            self.stdout.write("  2. For Gmail, use an App Password")
            self.stdout.write("  3. Enable 2-Step Verification and create App Password")
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ SMTP Connection failed: {e}"))
            self.stdout.write(self.style.WARNING("\nPossible solutions:"))
            self.stdout.write("  1. Check your internet connection")
            self.stdout.write("  2. Check if firewall is blocking the port")
            self.stdout.write("  3. Verify SMTP server address")
            return
        
        # Stop here if check-only
        if options['check_only']:
            self.stdout.write(self.style.SUCCESS("\n✓ Configuration check passed"))
            return
        
        # Send test email
        recipient = options.get('recipient')
        
        if not recipient:
            self.stdout.write(self.style.WARNING(
                "\nNo recipient email provided. Use: python manage.py test_email your-email@example.com"
            ))
            return
        
        self.stdout.write(f"\n" + self.style.HTTP_INFO(f"Sending test email to: {recipient}"))
        
        try:
            # Test plain email
            result = send_mail(
                subject='FITRA Email Test',
                message='This is a plain text test email from FITRA.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            
            if result == 1:
                self.stdout.write(self.style.SUCCESS("✓ Plain text email sent successfully"))
            
            # Test HTML email (like activation email)
            html_message = render_to_string(
                "members/activation_email.html",
                {
                    "name": "Test User",
                    "activation_link": "http://localhost:8000/register/activate/test-token/",
                    "language": "en",
                },
            )
            
            result = send_mail(
                subject='FITRA Activation Email Test',
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                html_message=html_message,
                fail_silently=False,
            )
            
            if result == 1:
                self.stdout.write(self.style.SUCCESS("✓ HTML activation email sent successfully"))
                self.stdout.write(self.style.SUCCESS(f"\n✓ Check {recipient} inbox (and spam folder)"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Failed to send email: {e}"))
            self.stdout.write("\nFull error:")
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
        
        self.stdout.write("\n" + self.style.HTTP_INFO("=" * 60))
