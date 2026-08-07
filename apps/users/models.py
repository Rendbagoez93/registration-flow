import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.shared.models import TimeStampedModel


class UserRole(models.TextChoices): 
    SYSTEM_ADMIN = "SYSTEM_ADMIN", "System_Admin"
    BUSINESS_OWNER = "BUSINESS_OWNER", "Business_Owner"
    CUSTOMER = "CUSTOMER", "Customer"
    
class User(AbstractUser, TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
        db_index=True,
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    @property
    def is_business_owner(self) -> bool:
        return self.role == UserRole.BUSINESS_OWNER

    def __str__(self):
        return f"{self.email or self.username} ({self.get_role_display()})"
    
