from rest_framework.serializers import ModelSerializer
from models import Users


class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'name', 'username', 'short_bio', 'email', 'location', 'created_on', 'updated_on')

