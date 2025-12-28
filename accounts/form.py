from django import forms
from allauth.account import app_settings as allauth_settings
from allauth.account.forms import SignupForm, LoginForm

from .models import User


class CustomLoginForm(LoginForm):
    """Allauth login form placeholder (extend if you need extra fields)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        input_classes = (
            "block w-full rounded-xl border border-slate-200 bg-white px-4 py-3 "
            "text-slate-900 placeholder:text-slate-400 shadow-sm focus:border-emerald-500 "
            "focus:ring-2 focus:ring-emerald-200 focus:outline-none"
        )
        if "login" in self.fields:
            self.fields["login"].widget.attrs.update(
                {"class": input_classes, "placeholder": "name@example.com"}
            )
        if "password" in self.fields:
            self.fields["password"].widget.attrs.update(
                {"class": input_classes, "placeholder": "•••••"}
            )
        if "remember" in self.fields:
            self.fields["remember"].widget.attrs.setdefault(
                "class",
                "h-5 w-5 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500",
            )

    def login(self, request, *args, **kwargs):
        """Respect the remember checkbox; otherwise expire on browser close."""
        remember = bool(self.cleaned_data.get("remember"))
        response = super().login(request, *args, **kwargs)
        request.session.set_expiry(
            allauth_settings.SESSION_COOKIE_AGE if remember else 0
        )
        return response


class CustomSignupForm(SignupForm):
    """Allauth signup form that captures required User fields."""

    role = forms.ChoiceField(choices=User.Role.choices, label="I am a")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        input_classes = (
            "flex h-10 w-full rounded-md border border-input bg-background px-16 py-2 text-base ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 md:text-sm pl-9"
        )
        select_classes = (
            "block w-full rounded-xl border border-slate-200 bg-white px-4 py-3 pr-10 "
            "text-slate-900 shadow-sm focus:border-emerald-500 focus:ring-2 "
            "focus:ring-emerald-200 focus:outline-none"
        )
        for name, field in self.fields.items():
            base_class = select_classes if isinstance(field.widget, forms.Select) else input_classes
            field.widget.attrs.setdefault("class", base_class)
        if "username" in self.fields:
            self.fields["username"].widget.attrs.setdefault("placeholder", "Username")
        if "email" in self.fields:
            self.fields["email"].widget.attrs.setdefault(
                "placeholder", "name@example.com"
            )
        if "password" in self.fields:
            self.fields["password"].widget.attrs.setdefault("placeholder", "••••••••")
       

    def save(self, request):
        user = super().save(request)
        user.role = self.cleaned_data["role"]
        user.membership_plan = "free"
        user.save()
        return user
