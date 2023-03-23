from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import search_profiles, paginate_profiles


def loginUser(request):
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else "account")
        else:
            messages.error(request, "Username OR password is incorrect")

    return render(request, "users/login_register.html")


def logoutUser(request):
    logout(request)
    messages.info(request, "User was logged out.")
    return redirect("login")


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created!")

            login(request, user)
            return redirect("edit-account")
        else:
            messages.success(request, "Failed to register due to error.")

    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)


def profiles(request):
    profiles, search_query = search_profiles(request)

    custom_range, profiles = paginate_profiles(request, profiles, 3)

    context = {
        "profiles": profiles,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, "users/profiles.html", context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {"profile": profile, "topSkills": topSkills, "otherSkills": otherSkills}
    return render(request, "users/user-profile.html", context)


@login_required(login_url="login")
def userAccount(request):
    # 1:1
    profile = request.user.profile

    skills = profile.skill_set.all()
    artworks = profile.artwork_set.all()

    context = {"profile": profile, "skills": skills, "artworks": artworks}
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    # prefill the fields
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect("account")

    context = {"form": form}
    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect("account")

    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was added successfully!")
            return redirect("account")

    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted.")
        return redirect("account")

    context = {"object": skill}
    return render(request, "delete_template.html", context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    message_requests = profile.messages.all()
    unread_count = message_requests.filter(is_read=False).count()
    context = {"message_requests": message_requests, "unread_count": unread_count}
    return render(request, "users/inbox.html", context)


@login_required(login_url="login")
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read is False:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, "users/message.html", context)


@login_required(login_url="login")
def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except User.DoesNotExist:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, "Message sent.")
            return redirect("user-profile", pk=recipient.id)

    context = {"recipient": recipient, "form": form}
    return render(request, "users/message_form.html", context)
