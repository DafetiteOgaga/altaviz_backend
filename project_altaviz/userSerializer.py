from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'phone',
            'email', 'username', 'wphone',
            ]  # add field desired
        # add date of birth, gender and role

        # fields = [
        #     'id', 'first_name', 'last_name', 'middle_name', 'phone',
        #     'email', 'username', 'wphone', 'profile_picture', 'aboutme',
        #     'is_deleted', 'last_login', 'date_joined',
        #     ]  # add field desired
        # # add date of birth, gender and role