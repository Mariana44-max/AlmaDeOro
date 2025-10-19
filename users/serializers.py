from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Profile, Address


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["phone", "date_of_birth", "avatar", "bio", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id", "label", "full_name", "phone", "address_line_1",
            "address_line_2", "city", "state", "zip_code", "country",
            "is_default", "address_type", "created_at", "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, data):
        # Validar que si se marca como default, el usuario no tenga otra dirección default del mismo tipo
        user = self.context['request'].user
        is_default = data.get('is_default', False)
        address_type = data.get('address_type', 'shipping')

        if is_default:
            # Si es actualización, excluir la dirección actual
            queryset = Address.objects.filter(
                user=user,
                address_type=address_type,
                is_default=True
            )
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            # Ya se maneja en el modelo save(), pero validamos aquí también
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "full_name", "is_admin", "date_joined"]
        read_only_fields = ["id", "date_joined", "is_admin"]


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer completo con profile y addresses para el usuario autenticado"""
    profile = ProfileSerializer(read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "email", "username", "full_name", "is_admin",
            "date_joined", "profile", "addresses"
        ]
        read_only_fields = ["id", "date_joined", "is_admin"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para registro de nuevos usuarios"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ["email", "username", "full_name", "password", "password2"]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Los campos de contraseña no coinciden."
            })
        return attrs

    def create(self, validated_data):
        # Remover password2 antes de crear el usuario
        validated_data.pop('password2')

        # Crear el usuario con create_user para hashear la contraseña
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', '')
        )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambiar contraseña"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                "new_password": "Los campos de contraseña nueva no coinciden."
            })
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Contraseña actual incorrecta.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
