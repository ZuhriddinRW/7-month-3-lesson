from rest_framework import serializers
from rest_framework import serializers
from .models import *
from django_app.models import User


class UserSerializer ( serializers.ModelSerializer ) :
    class Meta :
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number',
                  'is_active', 'is_staff', 'is_admin', 'is_manager']
        read_only_fields = ['id']


class UserCreateSerializer ( serializers.ModelSerializer ) :
    password = serializers.CharField ( write_only=True, required=True, style={'input_type' : 'password'} )
    password_confirm = serializers.CharField ( write_only=True, required=True, style={'input_type' : 'password'} )

    class Meta :
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number',
                  'password', 'password_confirm']

    def validate_email(self, value) :
        if not value :
            raise serializers.ValidationError ( "Email is required" )
        if User.objects.filter ( email=value ).exists () :
            raise serializers.ValidationError ( "Email already exists" )
        return value

    def validate_username(self, value) :
        if User.objects.filter ( username=value ).exists () :
            raise serializers.ValidationError ( "Username already exists" )
        return value

    def validate(self, data) :
        if data['password'] != data['password_confirm'] :
            raise serializers.ValidationError ( {"password" : "Passwords do not match"} )
        return data

    def create(self, validated_data) :
        validated_data.pop ( 'password_confirm' )
        password = validated_data.pop ( 'password' )
        user = User.objects.create_user ( password=password, **validated_data )
        return user


class LoginSerializer ( serializers.Serializer ) :
    username = serializers.CharField ()
    password = serializers.CharField ( write_only=True, style={'input_type' : 'password'} )

    def validate(self, data) :
        username = data.get ( 'username' )
        password = data.get ( 'password' )

        if username and password :
            try :
                user = User.objects.get ( username=username )
            except User.DoesNotExist :
                raise serializers.ValidationError ( 'Username or password is invalid' )

            if not user.check_password ( password ) :
                raise serializers.ValidationError ( 'Username or password is invalid' )

            if not user.is_active :
                raise serializers.ValidationError (
                    'Your account is not active. Please contact administrator.'
                )

            data['user'] = user
            return data
        else :
            raise serializers.ValidationError ( 'Must include "username" and "password"' )


class EmployeeSerializer ( serializers.ModelSerializer ) :
    class Meta :
        model = Employee
        fields = ['id', 'full_name', 'birth_date', 'created_at']


class CustomerSerializer ( serializers.ModelSerializer ) :
    class Meta :
        model = Customer
        fields = ['id', 'full_name', 'birth_date', 'created_at']


class ProductSerializer ( serializers.ModelSerializer ) :
    class Meta :
        model = Product
        fields = ['id', 'name', 'quantity', 'price', 'created_at']


class OrderProductSerializer ( serializers.ModelSerializer ) :
    product_name = serializers.CharField ( source='product.name', read_only=True )

    class Meta :
        model = OrderProduct
        fields = ['product', 'product_name', 'quantity', 'price']


class OrderSerializer ( serializers.ModelSerializer ) :
    customer_name = serializers.CharField ( source='customer.full_name', read_only=True )
    employee_name = serializers.CharField ( source='employee.full_name', read_only=True )
    products = OrderProductSerializer ( source='order_products', many=True, read_only=True )

    class Meta :
        model = Order
        fields = [
            'id',
            'customer',
            'customer_name',
            'employee',
            'employee_name',
            'products',
            'total_price',
            'order_date'
        ]