from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from recipes.models import User, Tag, Ingredient, Recipe
from api.validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователей."""
    username = serializers.CharField(
        max_length=150,
        validators=[
            validate_username,
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
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
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


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для инградиентов."""
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения рецептов."""
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = Recipe
        exclude = ['author']


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения рецептов."""
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
    author = UserSerializer()

    class Meta:
        model = Recipe
        fields = '__all__'
