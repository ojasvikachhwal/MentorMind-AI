"""
Email Service for Automated Weekly Progress Reports
Handles sending weekly progress reports and notifications to students.
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.models.progress import WeeklyReport
from app.services.progress_service import ProgressService

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending emails to users."""
    
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_USERNAME or "noreply@mentormind.com"
    
    def send_weekly_progress_report(self, user: User, report: WeeklyReport) -> bool:
        """Send weekly progress report email to user."""
        try:
            if not self.smtp_username or not self.smtp_password:
                logger.warning("SMTP credentials not configured. Skipping email send.")
                return False
            
            # Create email content
            subject = f"Weekly Progress Report - {report.week_start.strftime('%B %d, %Y')}"
            html_content = self._generate_weekly_report_html(user, report)
            text_content = self._generate_weekly_report_text(user, report)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = user.email
            
            # Add text and HTML parts
            text_part = MIMEText(text_content, 'plain')
            html_part = MIMEText(html_content, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Weekly progress report sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending weekly progress report: {e}")
            return False
    
    def send_achievement_notification(self, user: User, achievement: str) -> bool:
        """Send achievement notification email to user."""
        try:
            if not self.smtp_username or not self.smtp_password:
                logger.warning("SMTP credentials not configured. Skipping email send.")
                return False
            
            subject = "🎉 Achievement Unlocked!"
            html_content = self._generate_achievement_html(user, achievement)
            text_content = self._generate_achievement_text(user, achievement)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = user.email
            
            # Add text and HTML parts
            text_part = MIMEText(text_content, 'plain')
            html_part = MIMEText(html_content, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Achievement notification sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending achievement notification: {e}")
            return False
    
    def send_reminder_notification(self, user: User, message: str) -> bool:
        """Send reminder notification email to user."""
        try:
            if not self.smtp_username or not self.smtp_password:
                logger.warning("SMTP credentials not configured. Skipping email send.")
                return False
            
            subject = "📚 Learning Reminder from MentorMind"
            html_content = self._generate_reminder_html(user, message)
            text_content = self._generate_reminder_text(user, message)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = user.email
            
            # Add text and HTML parts
            text_part = MIMEText(text_content, 'plain')
            html_part = MIMEText(html_content, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Reminder notification sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending reminder notification: {e}")
            return False
    
    def _generate_weekly_report_html(self, user: User, report: WeeklyReport) -> str:
        """Generate HTML content for weekly progress report."""
        user_name = user.full_name or user.username
        
        achievements_html = ""
        if report.achievements:
            achievements_html = "<ul>"
            for achievement in report.achievements:
                achievements_html += f"<li>✅ {achievement}</li>"
            achievements_html += "</ul>"
        
        improvements_html = ""
        if report.areas_for_improvement:
            improvements_html = "<ul>"
            for improvement in report.areas_for_improvement:
                improvements_html += f"<li>📈 {improvement}</li>"
            improvements_html += "</ul>"
        
        goals_html = ""
        if report.next_week_goals:
            goals_html = "<ul>"
            for goal in report.next_week_goals:
                goals_html += f"<li>🎯 {goal}</li>"
            goals_html += "</ul>"
        
        courses_html = ""
        if report.recommended_courses:
            courses_html = "<ul>"
            for course in report.recommended_courses:
                courses_html += f"<li><a href='{course.get('url', '#')}'>{course.get('title', 'Course')}</a> - {course.get('level', 'Level')}</li>"
            courses_html += "</ul>"
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Weekly Progress Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 10px 10px; }}
                .section {{ margin: 20px 0; }}
                .section h3 {{ color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 5px; }}
                ul {{ margin: 10px 0; }}
                li {{ margin: 5px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                a {{ color: #667eea; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Weekly Progress Report</h1>
                    <p>Hello {user_name}!</p>
                    <p>Week of {report.week_start.strftime('%B %d')} - {report.week_end.strftime('%B %d, %Y')}</p>
                </div>
                
                <div class="content">
                    <div class="section">
                        <h3>📝 Summary</h3>
                        <p>{report.summary}</p>
                    </div>
                    
                    <div class="section">
                        <h3>🏆 Achievements</h3>
                        {achievements_html if achievements_html else "<p>Keep up the great work!</p>"}
                    </div>
                    
                    <div class="section">
                        <h3>📈 Areas for Improvement</h3>
                        {improvements_html if improvements_html else "<p>You're doing great across all areas!</p>"}
                    </div>
                    
                    <div class="section">
                        <h3>🎯 Next Week's Goals</h3>
                        {goals_html if goals_html else "<p>Continue your current learning pace!</p>"}
                    </div>
                    
                    <div class="section">
                        <h3>📚 Recommended Courses</h3>
                        {courses_html if courses_html else "<p>No specific recommendations this week.</p>"}
                    </div>
                    
                    <div class="section">
                        <h3>💡 Keep Learning!</h3>
                        <p>Remember, consistent practice is the key to success. Keep up the excellent work!</p>
                    </div>
                </div>
                
                <div class="footer">
                    <p>This report was generated by MentorMind AI Learning Platform</p>
                    <p>Visit <a href="{settings.FRONTEND_URL}">MentorMind</a> to continue your learning journey</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _generate_weekly_report_text(self, user: User, report: WeeklyReport) -> str:
        """Generate text content for weekly progress report."""
        user_name = user.full_name or user.username
        
        text = f"""
WEEKLY PROGRESS REPORT
=====================

Hello {user_name}!

Week of {report.week_start.strftime('%B %d')} - {report.week_end.strftime('%B %d, %Y')}

SUMMARY:
{report.summary}

ACHIEVEMENTS:
"""
        
        if report.achievements:
            for achievement in report.achievements:
                text += f"✅ {achievement}\n"
        else:
            text += "Keep up the great work!\n"
        
        text += "\nAREAS FOR IMPROVEMENT:\n"
        if report.areas_for_improvement:
            for improvement in report.areas_for_improvement:
                text += f"📈 {improvement}\n"
        else:
            text += "You're doing great across all areas!\n"
        
        text += "\nNEXT WEEK'S GOALS:\n"
        if report.next_week_goals:
            for goal in report.next_week_goals:
                text += f"🎯 {goal}\n"
        else:
            text += "Continue your current learning pace!\n"
        
        text += "\nRECOMMENDED COURSES:\n"
        if report.recommended_courses:
            for course in report.recommended_courses:
                text += f"📚 {course.get('title', 'Course')} - {course.get('level', 'Level')}\n"
                if course.get('url'):
                    text += f"   Link: {course['url']}\n"
        else:
            text += "No specific recommendations this week.\n"
        
        text += f"""
KEEP LEARNING!
Remember, consistent practice is the key to success. Keep up the excellent work!

---
This report was generated by MentorMind AI Learning Platform
Visit {settings.FRONTEND_URL} to continue your learning journey
"""
        
        return text
    
    def _generate_achievement_html(self, user: User, achievement: str) -> str:
        """Generate HTML content for achievement notification."""
        user_name = user.full_name or user.username
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Achievement Unlocked!</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); color: #333; padding: 20px; border-radius: 10px 10px 0 0; text-align: center; }}
                .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 10px 10px; text-align: center; }}
                .achievement {{ font-size: 24px; font-weight: bold; color: #ff6b6b; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                a {{ color: #667eea; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Achievement Unlocked!</h1>
                    <p>Congratulations {user_name}!</p>
                </div>
                
                <div class="content">
                    <div class="achievement">
                        {achievement}
                    </div>
                    
                    <p>Your dedication and hard work are paying off! Keep up the excellent progress.</p>
                    
                    <p><a href="{settings.FRONTEND_URL}">Continue Learning →</a></p>
                </div>
                
                <div class="footer">
                    <p>MentorMind AI Learning Platform</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _generate_achievement_text(self, user: User, achievement: str) -> str:
        """Generate text content for achievement notification."""
        user_name = user.full_name or user.username
        
        return f"""
ACHIEVEMENT UNLOCKED!
====================

Congratulations {user_name}!

🎉 {achievement}

Your dedication and hard work are paying off! Keep up the excellent progress.

Continue Learning: {settings.FRONTEND_URL}

---
MentorMind AI Learning Platform
"""
    
    def _generate_reminder_html(self, user: User, message: str) -> str:
        """Generate HTML content for reminder notification."""
        user_name = user.full_name or user.username
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Learning Reminder</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 10px 10px; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                a {{ color: #4ecdc4; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📚 Learning Reminder</h1>
                    <p>Hello {user_name}!</p>
                </div>
                
                <div class="content">
                    <p>{message}</p>
                    
                    <p><a href="{settings.FRONTEND_URL}">Start Learning Now →</a></p>
                </div>
                
                <div class="footer">
                    <p>MentorMind AI Learning Platform</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _generate_reminder_text(self, user: User, message: str) -> str:
        """Generate text content for reminder notification."""
        user_name = user.full_name or user.username
        
        return f"""
LEARNING REMINDER
================

Hello {user_name}!

{message}

Start Learning Now: {settings.FRONTEND_URL}

---
MentorMind AI Learning Platform
"""

class WeeklyReportScheduler:
    """Scheduler for sending weekly progress reports."""
    
    def __init__(self, db: Session):
        self.db = db
        self.email_service = EmailService()
        self.progress_service = ProgressService(db)
    
    def send_weekly_reports(self) -> Dict[str, int]:
        """Send weekly reports to all active users."""
        try:
            # Get all active users
            users = self.db.query(User).filter(User.is_active == True).all()
            
            sent_count = 0
            failed_count = 0
            
            for user in users:
                try:
                    # Generate weekly report
                    report = self.progress_service.generate_weekly_report(user.id)
                    
                    # Send email if not already sent
                    if not report.email_sent:
                        success = self.email_service.send_weekly_progress_report(user, report)
                        
                        if success:
                            report.email_sent = True
                            report.email_sent_at = datetime.now()
                            self.db.commit()
                            sent_count += 1
                        else:
                            failed_count += 1
                    else:
                        logger.info(f"Weekly report already sent to {user.email}")
                        
                except Exception as e:
                    logger.error(f"Error processing weekly report for user {user.id}: {e}")
                    failed_count += 1
            
            logger.info(f"Weekly reports sent: {sent_count}, failed: {failed_count}")
            return {"sent": sent_count, "failed": failed_count}
            
        except Exception as e:
            logger.error(f"Error in weekly report scheduler: {e}")
            return {"sent": 0, "failed": 0}