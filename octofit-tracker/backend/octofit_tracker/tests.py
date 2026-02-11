from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import datetime
from .models import User, Team, Activity, Leaderboard, Workout


class UserModelTest(TestCase):
    """Test cases for User model"""

    def setUp(self):
        self.user = User.objects.create(
            name='Test Hero',
            email='testhero@test.com',
            alias='Test Alias',
            team='Test Team',
            fitness_level='intermediate',
            goals=['strength', 'endurance']
        )

    def test_user_creation(self):
        """Test user is created successfully"""
        self.assertEqual(self.user.name, 'Test Hero')
        self.assertEqual(self.user.email, 'testhero@test.com')
        self.assertEqual(self.user.fitness_level, 'intermediate')

    def test_user_string_representation(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'Test Hero (Test Alias)')


class TeamModelTest(TestCase):
    """Test cases for Team model"""

    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            members=[],
            total_points=100
        )

    def test_team_creation(self):
        """Test team is created successfully"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.total_points, 100)

    def test_team_string_representation(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""

    def setUp(self):
        self.activity = Activity.objects.create(
            user_id='507f1f77bcf86cd799439011',
            activity_type='running',
            duration=30,
            distance=5.0,
            calories=300,
            points=50,
            date=datetime.now(),
            notes='Great run!'
        )

    def test_activity_creation(self):
        """Test activity is created successfully"""
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.points, 50)


class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""

    def setUp(self):
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='A test workout routine',
            difficulty='intermediate',
            duration=45,
            exercises=[{'name': 'Push-ups', 'sets': 3, 'reps': 15}],
            category='strength',
            recommended_for=['intermediate']
        )

    def test_workout_creation(self):
        """Test workout is created successfully"""
        self.assertEqual(self.workout.name, 'Test Workout')
        self.assertEqual(self.workout.difficulty, 'intermediate')
        self.assertEqual(self.workout.duration, 45)


class UserAPITest(APITestCase):
    """Test cases for User API endpoints"""

    def setUp(self):
        self.user = User.objects.create(
            name='API Test Hero',
            email='apitest@test.com',
            alias='API Alias',
            team='API Team',
            fitness_level='beginner',
            goals=['flexibility']
        )

    def test_get_users_list(self):
        """Test retrieving list of users"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail(self):
        """Test retrieving a single user"""
        url = reverse('user-detail', args=[str(self.user._id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'API Test Hero')


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints"""

    def setUp(self):
        self.team = Team.objects.create(
            name='API Test Team',
            description='Team for API testing',
            members=[],
            total_points=0
        )

    def test_get_teams_list(self):
        """Test retrieving list of teams"""
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_team_detail(self):
        """Test retrieving a single team"""
        url = reverse('team-detail', args=[str(self.team._id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'API Test Team')


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""

    def setUp(self):
        self.activity = Activity.objects.create(
            user_id='507f1f77bcf86cd799439011',
            activity_type='cycling',
            duration=60,
            distance=15.0,
            calories=500,
            points=75,
            date=datetime.now()
        )

    def test_get_activities_list(self):
        """Test retrieving list of activities"""
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_activity_detail(self):
        """Test retrieving a single activity"""
        url = reverse('activity-detail', args=[str(self.activity._id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activity_type'], 'cycling')


class WorkoutAPITest(APITestCase):
    """Test cases for Workout API endpoints"""

    def setUp(self):
        self.workout = Workout.objects.create(
            name='API Test Workout',
            description='Workout for API testing',
            difficulty='advanced',
            duration=90,
            exercises=[],
            category='cardio',
            recommended_for=['advanced']
        )

    def test_get_workouts_list(self):
        """Test retrieving list of workouts"""
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_workout_detail(self):
        """Test retrieving a single workout"""
        url = reverse('workout-detail', args=[str(self.workout._id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'API Test Workout')


class LeaderboardAPITest(APITestCase):
    """Test cases for Leaderboard API endpoints"""

    def setUp(self):
        self.leaderboard_entry = Leaderboard.objects.create(
            type='individual',
            user_id='507f1f77bcf86cd799439011',
            user_name='Test Champion',
            team='Test Team',
            points=1000,
            rank=1
        )

    def test_get_leaderboard_list(self):
        """Test retrieving leaderboard"""
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_team_rankings(self):
        """Test retrieving team rankings"""
        # Create a team leaderboard entry
        Leaderboard.objects.create(
            type='team',
            team_id='507f1f77bcf86cd799439012',
            team_name='Champion Team',
            points=5000,
            rank=1
        )
        url = reverse('leaderboard-team-rankings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_individual_rankings(self):
        """Test retrieving individual rankings"""
        url = reverse('leaderboard-individual-rankings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIRootTest(APITestCase):
    """Test cases for API root endpoint"""

    def test_api_root(self):
        """Test API root returns all endpoint links"""
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)
