from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class ProqodUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_admin, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_admin=is_admin,
                          is_active=True,
                          date_joined=now,
                          **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True,
                                 **extra_fields)


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
        unique=True)
    sid = models.CharField(
        verbose_name='sid',
        max_length=55,
        unique=True,
        help_text="Student or Staff ID"
    )
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True,
        null=True)
    last_name = models.CharField(
        _('last name'),
        max_length=30,
        blank=True,
        null=True)
    school = models.CharField(
        max_length=100,
        null=True,
        blank=True)
    department = models.CharField(
        max_length=100,
        null=True,
        blank=True)

    user_type = models.PositiveSmallIntegerField(
        default=STUDENT,
        choices=USER_TYPE,
        editable=False,
        )
    
    is_admin = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user is admin.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now)

    objects = ProqodUserManager()

    USERNAME_FIELD = 'sid'
    REQUIRED_FIELDS = [
        'email',
        'user_type',
        'first_name',
        'last_name',
        'school',
        'department'
    ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        fullname = "%s %s" % (self.first_name, self.last_name)
        return fullname.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return "%s"%self.id

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
