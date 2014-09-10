from django.db import models

class Attraction(models.Model):
    # Categories possible 
    ADVENTUROUS = 'ADV'
    CULTURAL = 'CUL'
    EDUCATION = 'EDU'
    FUN = 'FUN'
    HISTORICAL = 'HIS' 
    HUNGRY = 'HUN'
    LAZY = 'LAZ'
    LUXURIOUS = 'LUX'
    NATURAL = 'NAT'
    SOCIAL = 'SOC'
    CATEGORY_CHOICES = (
        (ADVENTUROUS,'Adventurous'),
        (CULTURAL,'Cultural'),
        (EDUCATION,'Education'),
        (FUN,'Fun'),
        (HISTORICAL,'Historical'),
        (HUNGRY,'Hungry'),
        (LAZY,'Lazy'),
        (LUXURIOUS,'Luxurious'),
        (NATURAL,'Natural'),
        (SOCIAL,'Social'),
    )

    name = models.CharField(max_length=200,unique=True)
    opening_hours = models.CharField(max_length=200,blank=True)
    description = models.TextField()
    url = models.URLField(max_length=200,blank=True)
    location = models.CharField(max_length=200)
    image = models.ImageField(blank=True) 
    category = models.CharField(max_length=3,choices=CATEGORY_CHOICES)
    vote_adventurous = models.PositiveIntegerField(default=0)
    vote_cultural = models.PositiveIntegerField(default=0)
    vote_education = models.PositiveIntegerField(default=0)
    vote_fun = models.PositiveIntegerField(default=0)
    vote_historical = models.PositiveIntegerField(default=0)
    vote_hungry = models.PositiveIntegerField(default=0)
    vote_lazy = models.PositiveIntegerField(default=0)
    vote_luxurious = models.PositiveIntegerField(default=0)
    vote_natural = models.PositiveIntegerField(default=0)
    vote_social = models.PositiveIntegerField(default=0)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Review(models.Model):
    attraction = models.ForeignKey(Attraction)
    review_text = models.TextField() 
    reviewer_name = models.CharField(max_length=200,blank=True)
    review_title = models.CharField(max_length=200)
    review_rating = models.FloatField(default=0.0)
    review_date = models.DateTimeField(auto_now_add=True)
