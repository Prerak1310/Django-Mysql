from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import mysql.connector

con = mysql.connector.connect(
    host="localhost", user="root", password="12345", database="prac"
)
cursor = con.cursor()


def main(request):
    return render(request, "main.htm")


def home(request):
    if request.user.is_authenticated:
        return redirect("main")
    else:
        if request.method == "POST":
            uname = request.POST["username"]
            email = request.POST["email"]
            pass1 = request.POST["password"]
            prerak = 1
            cursor.execute(
                "select * from users where Name='{}' and Email='{}'".format(
                    uname, email
                )
            )
            a = cursor.fetchall()
            t = tuple(a)
            print(t)
            if t == ():
                messages.info(request, "No account kindly signup")
            if t != ():
                if pass1 in t[0]:
                    user = authenticate(request, username=uname, password=pass1)
                    print(user)
                    if user is not None:
                        login(request, user)
                        return redirect("main")
                    else:
                        User.objects.create_user(uname, email, pass1)
                        user = authenticate(request, username=uname, password=pass1)
                        login(request, user)
                        return redirect("main")

                else:
                    messages.info(request, "incorrect password")
                    return redirect("home")

    return render(request, "home.html")


def signup(request):
    if request.method == "POST":
        d = request.POST
        for key, value in d.items():
            if key == "username":
                uname = value
            if key == "email":
                email = value.lower()
            if key == "password":
                pass1 = value
            if key == "password1":
                pass2 = value
        cursor.execute(
            "select * from users where Name='{}' or Email='{}'".format(uname, email)
        )
        a = cursor.fetchall()
        t = tuple(a)
        print(t)

        if pass1 == pass2:
            if t == ():
                cursor.execute(
                    "INSERT INTO USERS VALUES('{}','{}','{}','{}')".format(
                        email, uname, pass1, pass2
                    )
                )
                con.commit()
                messages.success(request, "REGISTRATION SUCCESSFUL!!Kindly login")
                return redirect("home")

            if t != ():
                if f"{uname}" in t[0]:
                    messages.info(request, "Username Taken")
                    return redirect("signup")

                elif f"{email}" in t[0]:
                    messages.info(request, "Email Taken")
                    return redirect("signup")
        else:
            messages.info(request, "Passwords dont match!!!")
            return redirect("signup")

    return render(request, "signup.htm")


def logoutpage(request):
    logout(request)
    messages.success(request, "You have been logged out!!")
    return redirect("home")
