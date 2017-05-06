from rest_framework.serializers import ModelSerializer
from models import Users, Movie, Review


class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'name', 'username', 'short_bio', 'email', 'location', 'created_on', 'updated_on')


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'name', 'duration_in_minutes', 'release_date', 'overall_rating', 'censor_board_rating', 'poster_picture_url')


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'rating', 'review')
