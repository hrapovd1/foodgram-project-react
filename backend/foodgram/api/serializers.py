from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from recipes.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователей."""
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    first_name = serializers.CharField(
        max_length=150,
    )
    last_name = serializers.CharField(
        max_length=150,
    )
    password = serializers.CharField(
        max_length=150,
        write_only=True
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'id'
        ]
        lookup_field = 'username'

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class PasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля."""
    new_password = serializers.CharField(
        max_length=150,
        write_only=True,
        required=True
    )
    current_password = serializers.CharField(
        max_length=150,
        write_only=True,
        required=True
    )

    def create(self, validated_data):
        user = self.instance
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = instance
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        user = self.instance
        try:
            _ = data['current_password']
        except KeyError:
            raise serializers.ValidationError(
                "Требуется поле current_password"
            )
        try:
            _ = data['new_password']
        except KeyError:
            raise serializers.ValidationError(
                "Требуется поле new_password"
            )
        if not user.check_password(data['current_password']):
            raise serializers.ValidationError(
                "Неверно имя пользователя или пароль"
            )
        return data
