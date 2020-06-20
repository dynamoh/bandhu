from django.db import models

from bandhuapp.models import Profile

# Create your models here.

class Ashram(models.Model):
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    address = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.name} - {self.locality}'

class ActivityCategory(models.Model):
    ashram = models.ForeignKey(Ashram, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Activity Categories'

    def __str__(self):
        return f'{self.ashram.name} - {self.name}'

class Activity(models.Model):
    ashram = models.ForeignKey(Ashram, on_delete=models.CASCADE)
    category = models.ForeignKey(ActivityCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f'{self.ashram.name} - {self.name} ({self.category.name})'

class Meeting(models.Model):
    ashram = models.ForeignKey(Ashram, on_delete=models.CASCADE)
    schedule = models.DateTimeField()
    topic = models.CharField(max_length=250)
    location = models.CharField(max_length=100)
    minutes = models.FileField(upload_to='ashram/meeting/%Y-%m-%d')

    def __str__(self):
        return f'{self.ashram.name} - {self.topic} ({self.schedule})'

class Attendee(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    contact_no = models.CharField(verbose_name="Contact Number", max_length=13)
    # or
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.meeting.ashram.name} - {self.meeting.schedule} - {self.name}'

    def save(self, *args, **kwargs):
        if self.profile is not None:
            self.name = f'{self.profile.first_name} {self.profile.first_name}'
            self.email = self.profile.user.email
            self.contact_no = self.profile.contact_no
        super(Guest, self).save(*args, **kwargs)

def picture_upload_path(instance, filname):
    return f'ashram/{instance.ashram.name}/{filename}'

class Photo(models.Model):
    ashram = models.ForeignKey(Ashram, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=picture_upload_path)
    category = models.ForeignKey(ActivityCategory, on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.ashram.name} - {self.category.name} - {self.activity.name} - {self.meeting.schedule}'
