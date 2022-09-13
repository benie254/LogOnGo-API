from rest_framework import serializers
from log_app.models import MyUser, Site, Profile, Site


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'employee_id', 'username', 'email', 'first_name', 'last_name', 'petrol_station', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile 
        fields = ('id','first_name','last_name','username','email')

class PetrolStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ('id','user_id','petrol_station')