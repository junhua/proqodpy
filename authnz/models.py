from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, User
)

class ProqodUserManager(BaseUserManager):

    def create_user(self, email, sid, password, is_active=True, user_type=0,
                    school=None, department=None, is_admin=False):
        """
        Creates and saves a User with the given information.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not sid:
            raise ValueError('Users must have an id')

        user = self.model(
            email=self.normalize_email(email),
            sid=sid,
        )

        user.set_password(password)
        user.is_admin = is_admin
        user.user_type = user_type
        user.school = school
        user.department = department
        user.save(using=self._db)
        return user

    def which_type(self):
        return self.user_type


class ProqodUser(AbstractBaseUser):
    STUDENT, TEACHER = range(2)
    USER_TYPE = (
        (STUDENT, 'student'),
        (TEACHER, 'teacher')
    )
    # Fields
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    sid = models.CharField(
        verbose_name='sid',
        max_length=55,
        unique=True,
    )

    school = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    user_type = models.PositiveSmallIntegerField(
        default=STUDENT, choices=USER_TYPE)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = ProqodUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['sid', 'user_type','is_admin', 'is_active', 'school', 'department', ]

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always

        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
