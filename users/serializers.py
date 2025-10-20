from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from .models import Profile, Address

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["phone", "date_of_birth", "avatar", "bio", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id", "label", "full_name", "phone",
            "address_line_1", "address_line_2",
            "city", "state", "zip_code", "country",
            "is_default", "address_type", "created_at", "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, data):
        user = self.context["request"].user
        is_default = data.get("is_default", False)
        address_type = data.get("address_type", "shipping")

        if is_default and user and user.is_authenticated:
            qs = Address.objects.filter(
                user=user, address_type=address_type, is_default=True
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"is_default": "Ya tienes una dirección por defecto de este tipo."}
                )
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "full_name", "is_admin", "date_joined"]
        read_only_fields = ["id", "date_joined", "is_admin"]


class UserDetailSerializer(UserSerializer):
    profile = ProfileSerializer(read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ["profile", "addresses"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["email", "username", "full_name", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2", None)
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password": "Los campos de contraseña nueva no coinciden."})
        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Contraseña actual incorrecta.")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
