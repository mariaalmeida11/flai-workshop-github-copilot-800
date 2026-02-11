from djongo import models


class User(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    alias = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    fitness_level = models.CharField(max_length=50)
    goals = models.JSONField(default=list)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.name} ({self.alias})"


class Team(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.JSONField(default=list)
    total_points = models.IntegerField(default=0)
    captain = models.CharField(max_length=24)  # ObjectId as string

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    user_id = models.CharField(max_length=24)  # ObjectId as string
    activity_type = models.CharField(max_length=50)
    duration = models.IntegerField()  # minutes
    distance = models.FloatField()  # km
    calories = models.IntegerField()
    points = models.IntegerField()
    date = models.DateTimeField()
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-date']

    def __str__(self):
        return f"{self.activity_type} - {self.duration} mins"


class Leaderboard(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    type = models.CharField(max_length=20)  # 'team' or 'individual'
    team_id = models.CharField(max_length=24, null=True, blank=True)
    team_name = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.CharField(max_length=24, null=True, blank=True)
    user_name = models.CharField(max_length=100, null=True, blank=True)
    team = models.CharField(max_length=100, null=True, blank=True)
    points = models.IntegerField()
    rank = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']

    def __str__(self):
        if self.type == 'team':
            return f"{self.team_name} - Rank {self.rank}"
        return f"{self.user_name} - Rank {self.rank}"


class Workout(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    duration = models.IntegerField()  # minutes
    exercises = models.JSONField(default=list)
    category = models.CharField(max_length=50)
    recommended_for = models.JSONField(default=list)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return f"{self.name} ({self.difficulty})"
