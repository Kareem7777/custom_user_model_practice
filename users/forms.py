from dataclasses import fields
from urllib import request
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth import get_user_model ,authenticate


User = get_user_model()

