from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        self.stdout.write(self.style.SUCCESS('Connected to octofit_db'))

        # Delete existing data
        self.stdout.write('Deleting existing data...')
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email field
        db.users.create_index([('email', 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('Created unique index on email field'))

        # Sample superhero data
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'alias': 'Tony Stark'},
            {'name': 'Captain America', 'email': 'captainamerica@marvel.com', 'alias': 'Steve Rogers'},
            {'name': 'Thor', 'email': 'thor@marvel.com', 'alias': 'Thor Odinson'},
            {'name': 'Black Widow', 'email': 'blackwidow@marvel.com', 'alias': 'Natasha Romanoff'},
            {'name': 'Hulk', 'email': 'hulk@marvel.com', 'alias': 'Bruce Banner'},
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'alias': 'Peter Parker'},
        ]

        dc_heroes = [
            {'name': 'Batman', 'email': 'batman@dc.com', 'alias': 'Bruce Wayne'},
            {'name': 'Superman', 'email': 'superman@dc.com', 'alias': 'Clark Kent'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'alias': 'Diana Prince'},
            {'name': 'Flash', 'email': 'flash@dc.com', 'alias': 'Barry Allen'},
            {'name': 'Aquaman', 'email': 'aquaman@dc.com', 'alias': 'Arthur Curry'},
            {'name': 'Green Lantern', 'email': 'greenlantern@dc.com', 'alias': 'Hal Jordan'},
        ]

        # Insert users
        marvel_user_ids = []
        dc_user_ids = []

        for hero in marvel_heroes:
            user = {
                'name': hero['name'],
                'email': hero['email'],
                'alias': hero['alias'],
                'team': 'Team Marvel',
                'created_at': datetime.now(),
                'fitness_level': random.choice(['beginner', 'intermediate', 'advanced']),
                'goals': ['strength', 'endurance', 'flexibility']
            }
            result = db.users.insert_one(user)
            marvel_user_ids.append(result.inserted_id)

        for hero in dc_heroes:
            user = {
                'name': hero['name'],
                'email': hero['email'],
                'alias': hero['alias'],
                'team': 'Team DC',
                'created_at': datetime.now(),
                'fitness_level': random.choice(['beginner', 'intermediate', 'advanced']),
                'goals': ['strength', 'endurance', 'flexibility']
            }
            result = db.users.insert_one(user)
            dc_user_ids.append(result.inserted_id)

        self.stdout.write(self.style.SUCCESS(f'Inserted {len(marvel_user_ids) + len(dc_user_ids)} users'))

        # Insert teams
        team_marvel = {
            'name': 'Team Marvel',
            'description': 'Avengers assemble for fitness!',
            'created_at': datetime.now(),
            'members': marvel_user_ids,
            'total_points': 0,
            'captain': marvel_user_ids[0]
        }

        team_dc = {
            'name': 'Team DC',
            'description': 'Justice League fighting for health!',
            'created_at': datetime.now(),
            'members': dc_user_ids,
            'total_points': 0,
            'captain': dc_user_ids[0]
        }

        marvel_team_id = db.teams.insert_one(team_marvel).inserted_id
        dc_team_id = db.teams.insert_one(team_dc).inserted_id

        self.stdout.write(self.style.SUCCESS('Inserted 2 teams'))

        # Insert activities
        activity_types = ['running', 'cycling', 'swimming', 'weightlifting', 'yoga', 'crossfit']
        activities = []

        for user_id in marvel_user_ids + dc_user_ids:
            for i in range(random.randint(3, 8)):
                activity = {
                    'user_id': user_id,
                    'activity_type': random.choice(activity_types),
                    'duration': random.randint(20, 120),  # minutes
                    'distance': round(random.uniform(1.0, 15.0), 2),  # km
                    'calories': random.randint(100, 800),
                    'points': random.randint(10, 100),
                    'date': datetime.now() - timedelta(days=random.randint(0, 30)),
                    'notes': 'Great workout session!'
                }
                activities.append(activity)

        db.activities.insert_many(activities)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(activities)} activities'))

        # Calculate and insert leaderboard data
        marvel_total = sum([act['points'] for act in activities if act['user_id'] in marvel_user_ids])
        dc_total = sum([act['points'] for act in activities if act['user_id'] in dc_user_ids])

        # Update team points
        db.teams.update_one({'_id': marvel_team_id}, {'$set': {'total_points': marvel_total}})
        db.teams.update_one({'_id': dc_team_id}, {'$set': {'total_points': dc_total}})

        # Create leaderboard entries
        leaderboard_entries = []
        
        # Team leaderboard
        leaderboard_entries.append({
            'type': 'team',
            'team_id': marvel_team_id,
            'team_name': 'Team Marvel',
            'points': marvel_total,
            'rank': 1 if marvel_total > dc_total else 2,
            'updated_at': datetime.now()
        })

        leaderboard_entries.append({
            'type': 'team',
            'team_id': dc_team_id,
            'team_name': 'Team DC',
            'points': dc_total,
            'rank': 1 if dc_total > marvel_total else 2,
            'updated_at': datetime.now()
        })

        # Individual leaderboard
        user_points = {}
        for activity in activities:
            user_id = activity['user_id']
            if user_id not in user_points:
                user_points[user_id] = 0
            user_points[user_id] += activity['points']

        sorted_users = sorted(user_points.items(), key=lambda x: x[1], reverse=True)
        
        for rank, (user_id, points) in enumerate(sorted_users, 1):
            user = db.users.find_one({'_id': user_id})
            leaderboard_entries.append({
                'type': 'individual',
                'user_id': user_id,
                'user_name': user['name'],
                'team': user['team'],
                'points': points,
                'rank': rank,
                'updated_at': datetime.now()
            })

        db.leaderboard.insert_many(leaderboard_entries)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(leaderboard_entries)} leaderboard entries'))

        # Insert workout suggestions
        workout_suggestions = [
            {
                'name': 'Super Soldier Training',
                'description': 'Full body workout inspired by Captain America',
                'difficulty': 'advanced',
                'duration': 60,
                'exercises': [
                    {'name': 'Push-ups', 'sets': 4, 'reps': 25},
                    {'name': 'Pull-ups', 'sets': 4, 'reps': 15},
                    {'name': 'Squats', 'sets': 4, 'reps': 30},
                    {'name': 'Planks', 'sets': 3, 'duration': '90 seconds'},
                ],
                'category': 'strength',
                'recommended_for': ['intermediate', 'advanced']
            },
            {
                'name': 'Web-Slinger Cardio',
                'description': 'High-intensity cardio like Spider-Man swinging through the city',
                'difficulty': 'intermediate',
                'duration': 30,
                'exercises': [
                    {'name': 'Jumping Jacks', 'sets': 3, 'reps': 50},
                    {'name': 'Burpees', 'sets': 3, 'reps': 20},
                    {'name': 'Mountain Climbers', 'sets': 3, 'duration': '60 seconds'},
                    {'name': 'Jump Rope', 'sets': 3, 'duration': '120 seconds'},
                ],
                'category': 'cardio',
                'recommended_for': ['beginner', 'intermediate']
            },
            {
                'name': 'Amazonian Warrior Workout',
                'description': 'Combat-ready training inspired by Wonder Woman',
                'difficulty': 'advanced',
                'duration': 45,
                'exercises': [
                    {'name': 'Deadlifts', 'sets': 4, 'reps': 12},
                    {'name': 'Battle Ropes', 'sets': 3, 'duration': '60 seconds'},
                    {'name': 'Box Jumps', 'sets': 3, 'reps': 15},
                    {'name': 'Medicine Ball Slams', 'sets': 3, 'reps': 20},
                ],
                'category': 'strength',
                'recommended_for': ['advanced']
            },
            {
                'name': 'Speedster Sprint Training',
                'description': 'Fast-paced running workout like The Flash',
                'difficulty': 'intermediate',
                'duration': 40,
                'exercises': [
                    {'name': 'Sprint Intervals', 'sets': 8, 'duration': '30 seconds'},
                    {'name': 'High Knees', 'sets': 4, 'reps': 30},
                    {'name': 'Butt Kicks', 'sets': 4, 'reps': 30},
                    {'name': 'Cool Down Jog', 'sets': 1, 'duration': '10 minutes'},
                ],
                'category': 'cardio',
                'recommended_for': ['intermediate', 'advanced']
            },
            {
                'name': 'Zen Warrior Yoga',
                'description': 'Flexibility and balance training',
                'difficulty': 'beginner',
                'duration': 30,
                'exercises': [
                    {'name': 'Sun Salutations', 'sets': 3, 'reps': 5},
                    {'name': 'Warrior Poses', 'sets': 2, 'duration': '60 seconds each'},
                    {'name': 'Tree Pose', 'sets': 2, 'duration': '45 seconds each side'},
                    {'name': 'Savasana', 'sets': 1, 'duration': '5 minutes'},
                ],
                'category': 'flexibility',
                'recommended_for': ['beginner', 'intermediate', 'advanced']
            },
        ]

        db.workouts.insert_many(workout_suggestions)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(workout_suggestions)} workout suggestions'))

        # Close connection
        client.close()

        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'Collections created:')
        self.stdout.write(f'  - users: {len(marvel_user_ids) + len(dc_user_ids)} documents')
        self.stdout.write(f'  - teams: 2 documents')
        self.stdout.write(f'  - activities: {len(activities)} documents')
        self.stdout.write(f'  - leaderboard: {len(leaderboard_entries)} documents')
        self.stdout.write(f'  - workouts: {len(workout_suggestions)} documents')
