from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager ( BaseUserManager ) :
    def create_user(self, username, email=None, password=None, **extra_fields) :
        if not username :
            raise ValueError ( 'Username is required!' )

        email = self.normalize_email ( email ) if email else None
        user = self.model ( username=username, email=email, **extra_fields )
        user.set_password ( password )
        user.save ( using=self._db )
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields) :
        extra_fields.setdefault ( 'is_staff', True )
        extra_fields.setdefault ( 'is_superuser', True )
        extra_fields.setdefault ( 'is_active', True )
        extra_fields.setdefault ( 'is_admin', False )
        extra_fields.setdefault ( 'is_manager', False )

        if extra_fields.get ( 'is_staff' ) is not True :
            raise ValueError ( "Superuser's property is_staff must be True" )
        if extra_fields.get ( 'is_superuser' ) is not True :
            raise ValueError ( "Superuser's property is_superuser must be True" )

        return self.create_user ( username, email, password, **extra_fields )


class User ( AbstractBaseUser, PermissionsMixin ) :
    username = models.CharField ( max_length=150, unique=True )
    email = models.EmailField ( blank=True, null=True, unique=True )
    first_name = models.CharField ( max_length=150, blank=True )
    last_name = models.CharField ( max_length=150, blank=True )
    phone_number = models.CharField ( unique=True, max_length=15, blank=True, null=True )

    is_active = models.BooleanField ( default=True )
    is_staff = models.BooleanField ( default=False )
    is_admin = models.BooleanField ( default=False )
    is_manager = models.BooleanField ( default=False )

    objects = UserManager ()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self) :
        return self.username


class BaseModel ( models.Model ) :
    created_at = models.DateTimeField ( auto_now_add=True )
    updated_at = models.DateTimeField ( auto_now=True )

    class Meta :
        abstract = True


class Employee ( models.Model ) :
    full_name = models.CharField ( max_length=255, verbose_name="Full name" )
    birth_date = models.DateField ( verbose_name="Birth date" )
    created_at = models.DateTimeField ( auto_now_add=True )
    updated_at = models.DateTimeField ( auto_now=True )

    class Meta :
        db_table = 'employees'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self) :
        return self.full_name


class Customer ( models.Model ) :
    full_name = models.CharField ( max_length=255, verbose_name="Full name" )
    birth_date = models.DateField ( verbose_name="Birth date" )
    created_at = models.DateTimeField ( auto_now_add=True )
    updated_at = models.DateTimeField ( auto_now=True )

    class Meta :
        db_table = 'customers'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self) :
        return self.full_name


class Product ( models.Model ) :
    name = models.CharField ( max_length=255, verbose_name="Name" )
    quantity = models.IntegerField ( default=0, verbose_name="Quantity" )
    price = models.DecimalField ( max_digits=12, decimal_places=2, verbose_name="Price" )
    created_at = models.DateTimeField ( auto_now_add=True )
    updated_at = models.DateTimeField ( auto_now=True )

    class Meta :
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self) :
        return f"{self.name} - {self.price} UZS"


class Order ( models.Model ) :
    customer = models.ForeignKey (
        Customer,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Customer"
    )
    employee = models.ForeignKey (
        Employee,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Employee"
    )
    total_price = models.DecimalField (
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Total price"
    )
    order_date = models.DateTimeField ( verbose_name="Order date" )
    created_at = models.DateTimeField ( auto_now_add=True )
    updated_at = models.DateTimeField ( auto_now=True )

    class Meta :
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self) :
        return f"Order #{self.id} - {self.total_price} UZS"


class OrderProduct ( models.Model ) :
    order = models.ForeignKey (
        Order,
        on_delete=models.CASCADE,
        related_name='order_products'
    )
    product = models.ForeignKey (
        Product,
        on_delete=models.CASCADE,
        related_name='order_products'
    )
    quantity = models.IntegerField ( verbose_name="Quantity" )
    price = models.DecimalField (
        max_digits=12,
        decimal_places=2,
        verbose_name="Price"
    )

    class Meta :
        db_table = 'order_products'
        verbose_name = 'Order product'
        verbose_name_plural = 'Order products'

    def __str__(self) :
        return f"{self.product.name} x {self.quantity}"