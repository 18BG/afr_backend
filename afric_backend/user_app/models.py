# auth_app/models.py
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone number must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)

class User(AbstractBaseUser):
    phone = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def generate_otp(self):
        self.otp = f"{random.randint(100000, 999999)}"
        self.otp_created_at = timezone.now()
        self.save()

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser



class Pret(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,to_field="phone")
    montant = models.DecimalField(max_digits=20, decimal_places=2,default=0.0)
    taux_interet = models.FloatField(default=0.0)
    solde_total= models.DecimalField(max_digits=20, decimal_places=2,default=0.0)
    encours = models.FloatField(default=0.0)
    delais = models.DateTimeField(blank=True, null=True)
    rembourser = models.DecimalField(max_digits=20, decimal_places=2,default=0.0)
    solde_payer = models.DecimalField(max_digits=20, decimal_places=2,default=0.0)
    
    def CalculerInteret(self):
        self.taux_interet = float(self.montant) * 0.2
    def CalculerEncours(self):
        self.encours = float(self.montant) + self.taux_interet
        self.solde_total = float(self.montant) + self.taux_interet
    def CalculerEncourRestant(self):
        self.encours = self.encours - float(self.solde_payer)
        self.rembourser = float(self.solde_total) - self.encours
    
    def set_delais(self):
        if float(self.montant) >=0 and float(self.montant) <= 10000:
            self.delais = timezone.now() + timedelta(days=10)
        elif  float(self.montant) > 10000  and float(self.montant) <= 50000:
            self.delais = timezone.now() + timedelta(days=30)
        else:
            self.delais = None  # Or set to another value if required
    
    def save(self, *args, **kwargs):
        self.CalculerInteret()
        self.CalculerEncours()
        self.CalculerEncourRestant()
        self.set_delais()
        super(Pret, self).save(*args, **kwargs)