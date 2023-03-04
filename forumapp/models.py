from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import math

class Question(models.Model):
    title = models.CharField(max_length=300)
    desc = models.TextField()
    image = models.ImageField(blank=True, upload_to="images/")
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")

    categories = [
        ("F1", "F1"),
        ("NA", "NASCAR"),
        ("TR", "Trucks"),
        ("EN", "Engines"),
        ("MU", "Muscle Cars")
    ]
    category = models.CharField(
        max_length=2,
        choices=categories,
        default="F1"
    )

    def __str__(self):
        return f"{self.title}, {self.user}, {self.create_date}"
    
    def total_likes(self):
        return self.likes.count()
    
    def total_answers(self):
        return self.answers.count()
    
    def display_category_name(self):
        for short, long in self.categories:
            if short == self.category:
                return long
            
    def display_time(self):
        total = timezone.now() - self.create_date

        if total.days == 0 and total.seconds >= 0 and total.seconds < 60:
            sec = total.seconds
            if sec == 1:
                return f"{sec} second ago"
            else:
                return f"{sec} seconds ago"
        
        elif total.days == 0 and total.seconds >= 60 and total.seconds < 60*60:
            mins = math.floor(total.seconds/60)
            if mins == 1:
                return f"{mins} minute ago"
            else:
                return f"{mins} minutes ago"
            
        elif total.days == 0 and total.seconds >= 3600 and total.seconds < 86400:
            hours = math.floor(total.seconds/3600)
            if hours == 1:
                return f"{hours} hour ago"
            else:
                return f"{hours} hours ago"
            
        elif total.days >=1 and total.days < 30:
            days = total.days
            if days == 1:
                return f"{days} day ago"
            else:
                return f"{days} days ago"
        
        elif total.days >= 30 and total.days < 365:
            months = math.floor(total.days/30)
            if months == 1:
                return f"{months} month ago"
            else:
                return f"{months} months ago"
            
        else:
            years = math.floor(total.days/365)
            if years == 1:
                return f"{years} year ago"
            else:
                return f"{years} years ago"   
                   
class Answer(models.Model):
    desc = models.TextField()
    image = models.ImageField(upload_to = "images/", blank=True)
    create_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="answerLikes")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")

    def __str__(self):
        return f"{self.title}, {self.user}, {self.create_date}"
    
    def total_likes(self):
        return self.likes.count()
    
    def display_time(self):
        total = timezone.now() - self.create_date

        if total.days == 0 and total.seconds >= 0 and total.seconds < 60:
            sec = total.seconds
            if sec == 1:
                return f"{sec} second ago"
            else:
                return f"{sec} seconds ago"
        
        elif total.days == 0 and total.seconds >= 60 and total.seconds < 60*60:
            mins = math.floor(total.seconds/60)
            if mins == 1:
                return f"{mins} minute ago"
            else:
                return f"{mins} minutes ago"
            
        elif total.days == 0 and total.seconds >= 3600 and total.seconds < 86400:
            hours = math.floor(total.seconds/3600)
            if hours == 1:
                return f"{hours} hour ago"
            else:
                return f"{hours} hours ago"
            
        elif total.days >=1 and total.days < 30:
            days = total.days
            if days == 1:
                return f"{days} day ago"
            else:
                return f"{days} days ago"
        
        elif total.days >= 30 and total.days < 365:
            months = math.floor(total.days/30)
            if months == 1:
                return f"{months} month ago"
            else:
                return f"{months} months ago"
            
        else:
            years = math.floor(total.days/365)
            if years == 1:
                return f"{years} year ago"
            else:
                return f"{years} years ago"   

