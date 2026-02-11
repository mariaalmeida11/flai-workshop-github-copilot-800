from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'alias', 'team', 'fitness_level', 'created_at']
    list_filter = ['team', 'fitness_level', 'created_at']
    search_fields = ['name', 'email', 'alias']
    readonly_fields = ['_id', 'created_at']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_points', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['_id', 'created_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'activity_type', 'duration', 'distance', 'calories', 'points', 'date']
    list_filter = ['activity_type', 'date']
    search_fields = ['user_id', 'notes']
    readonly_fields = ['_id']
    ordering = ['-date']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['rank', 'type', 'get_name', 'points', 'updated_at']
    list_filter = ['type', 'updated_at']
    search_fields = ['user_name', 'team_name']
    readonly_fields = ['_id', 'updated_at']
    ordering = ['rank']

    def get_name(self, obj):
        """Return the appropriate name based on leaderboard type"""
        if obj.type == 'team':
            return obj.team_name
        return obj.user_name
    get_name.short_description = 'Name'


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'difficulty', 'duration', 'category']
    list_filter = ['difficulty', 'category']
    search_fields = ['name', 'description']
    readonly_fields = ['_id']
