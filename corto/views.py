from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, redirect,render_to_response
from django.core.mail import send_mail
from corto.forms import *
from .models import *
from django.contrib.messages import get_messages
import string, random
from django.core.exceptions import ObjectDoesNotExist

username = ""
email = ""
urls = {}
site = "http://cortos.herokuapp.com/"

#generates random string
def id(size=6, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#dashboard data
def dash_data(obj):
    username = str(obj.fname) + " " + str(obj.lname)
    email = str(obj.email)
    urls = Urls.objects.filter(id=obj.id)
    return {
        "username":username,
        "email": email,
        "urls": urls
    }

# def user_logged_in(req):
#     if "corto_user" in req.COOKIES:
#         eq_token = request.COOKIES['corto_user']
#         try:
#             db_token = User.objects.get(id=req_token)
#             data = dash_data(db_token)
#             return True
#         except ObjectDoesNotExist:
#             return False
#     return False

#main view
def index(request):
    con = None
    is_data = 0
    response = ""
    req_browser = None
    #check if user already logged in or not
    if "corto_user" in request.COOKIES:
        req_token = request.COOKIES['corto_user']
        try:
            db_token = User.objects.get(id=req_token)
            return redirect("/dashboard/")
        except ObjectDoesNotExist:
            error = ""
            response =  render(request, "corto/index.html", {"error":error})
            response.delete_cookie('corto_user')
    elif "corto_browser" in request.COOKIES:
        req_browser = request.COOKIES['corto_browser']
        try:
            br_token = Browser_url.objects.filter(browser_token=req_browser)
            is_data = 0
            #get all url shortan in browser and show
            temp = list(br_token)
            if len(temp) >= 1:
                is_data = 1
            br_token = br_token
            con = {
                "is_data":is_data,
                "data":br_token
            }
        except ObjectDoesNotExist:
            is_data = 0
            con = {
            "is_data":is_data
            }
    else:
        brs_token = id(20)
        response = render(request, 'corto/index.html', {})
        response.set_cookie("corto_browser", brs_token, max_age=2592000)
        return response


    #check if form to short url is submitted
    if request.method == "POST":
        MyForm = Shorten(request.POST)
        #form validation by django
        if MyForm.is_valid():
            url = MyForm.cleaned_data['url']
            short = id()
            #prepend http ot https
            if url[:7] == "http://" or url[:8] == "https://":
                pass
            else:
                url = "http://"+url
            short = site+short
            # new = Urls(original=url,shortan=short)
            # new.save()

            while True:
                try:
                    exs = Urls.objects.get(shortan=short)
                    short = id()
                except ObjectDoesNotExist:
                    new = Urls(original=url,shortan=short)
                    new.save()
                    u = Urls.objects.get(shortan=short)
                    new_browser = Browser_url(browser_token=req_browser, url_id=u)
                    new_browser.save()
                    break
            if "corto_browser" in request.COOKIES:
                req_browser = request.COOKIES['corto_browser']
                try:
                    br_token = Browser_url.objects.filter(browser_token=req_browser)
                    is_data = 0
                    #get all url shortan in browser and show
                    temp = list(br_token)
                    if len(temp) >= 1:
                        is_data = 1
                    br_token = br_token
                    con = {
                        "title":"Your Short URL",
                        "shorted": short,
                        "original": url,
                        "is_data":is_data,
                        "data":br_token
                    }
                except ObjectDoesNotExist:
                    is_data = 0
                    con = {
                    "title":"Your Short URL",
                    "shorted": short,
                    "original": url,
                    "is_data":is_data
                    }
            return render(request, "corto/index.html", con)
        #url is not valid
        else:
            con = {
                "error": "Url is not valid"
            }
    return render(request, "corto/index.html", con)

def dashboard(request):
    is_data = 0
    con = {}

    if "corto_user" in request.COOKIES:
        req_token = request.COOKIES['corto_user']
        try:
            db_token = User.objects.get(id=req_token)
            try:
                url_data = User_urls.objects.filter(user_id=db_token)
                is_data = 1
            except ObjectDoesNotExist:
                is_data = 0
                con = {
                    "is_data":is_data,
                    "details": dash_data(db_token)
                 }
            con = {
                "is_data":is_data,
                "data":url_data,
                "details": dash_data(db_token)
             }
        except ObjectDoesNotExist:
            return redirect("../")
    else:
        return redirect("../")

    if request.method == "POST":
        MyForm = Shorten(request.POST)
        #form validation by django
        if MyForm.is_valid():
            url = MyForm.cleaned_data['url']
            short = id()
            #prepend http ot https
            if url[:7] == "http://" or url[:8] == "https://":
                pass
            else:
                url = "http://"+url
            short = site + short
            # new = Urls(original=url,shortan=short)
            # new.save()

            while True:
                try:
                    exs = Urls.objects.get(shortan=short)
                    short = site + id()
                except ObjectDoesNotExist:
                    new = Urls(original=url,shortan=short)
                    new.save()
                    try:
                        new1 = Urls.objects.get(shortan=short)
                        new_user_url = User_urls(url_id=new1, user_id=db_token)
                        new_user_url.save()
                    except ObjectDoesNotExist:
                        con = {
                            "is_data":is_data,
                            "data":url_data,
                            "details": dash_data(db_token),
                            "error": "Something went wrong!"
                        }
                    con = {
                        "is_data":is_data,
                        "data":url_data,
                        "details": dash_data(db_token),
                        "title":"Your Short URL",
                        "shorted": short,
                        "original": url
                    }
                    break
            return render(request, "corto/dashboard.html", con)
        #url is not valid
        else:
            con = {
                "details": dash_data(db_token),
                "error": "Url is not valid"
            }
        con = {
            "is_data":is_data,
            "data":url_data,
            "details": dash_data(db_token),
        }


    return render(request, "corto/dashboard.html", con)
    # data = {}
    # con = {}
    #
    # return render(request, "corto/dashboard.html", con)


# def shorten(request):
#     if request.method == "POST":
#         MyForm = Shorten(request.POST)
#         if MyForm.is_valid():
#             url = MyForm.cleaned_data['url']
#             short = id()
#             if url[:7] == "http://" or url[:8] == "https://":
#                 pass
#             else:
#                 url = "http://"+url
#             short = site+short
#             new = Urls(original=url,shortan=short)
#             new.save()
#     return HttpResponse(url + "<br />New link : " + short)

def redirecting(request, short_url):
    try:
        c = site+short_url
        a = Urls.objects.get(shortan=c)
        a.clicks = a.clicks + 1
        a.save()
        try:
            if request.user_agent.is_mobile:
                device = "mobile"
            elif request.user_agent.is_tablet:
                device = "tablet"
            elif request.user_agent.is_pc:
                device = "pc"
            else:
                device = "other"
            new_click = Click(urlId=a, platform=request.user_agent.os.family, browser=request.user_agent.browser.family, device=device)
            new_click.save()
        except Exception as e:
            return HttpResponse(e)
        return redirect(str(a.original))
    except ObjectDoesNotExist:
        HttpResponse("Url not exists")
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("<h1>Oops, page you are looking for not found</h1>")


def sign_in(request):
    if request.method == "POST":
        login_form = Login(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']

            try:
                get_mail = User.objects.get(email=email)
            except ObjectDoesNotExist:
                error = "Email not exists"
                return render(request, "corto/index.html", {"error":error})

            try:
                get_pass = User.objects.get(email=email ,password=password)
            except ObjectDoesNotExist:
                error = "Incorrect Password"
                return render(request, "corto/index.html", {"error":error})

            temp_id = get_pass.id
            response = redirect(site)
            response.set_cookie("corto_user", temp_id)
            return response
        else:
            error = "Form is not valid"
            return render(request, "corto/index.html", {"error":error})
    #return render(request, "corto/index.html", {})
    return HttpResponse("oops")

def sign_up(request):
    if request.method == "POST":
        new_sign = Signup(request.POST)
        if new_sign.is_valid():
            fname = new_sign.cleaned_data['fname']
            lname = new_sign.cleaned_data['lname']
            email = new_sign.cleaned_data['email']
            password = new_sign.cleaned_data['password']
            repass = new_sign.cleaned_data['repassword']
            if password == repass:
                #check if email exists
                try:
                    b_email = User.objects.get(email=email)
                except ObjectDoesNotExist:
                    new_user = User(fname=fname,lname=lname,email=email,password=password)
                    new_user.save()
                    return HttpResponse("<h2>Registered successfully</h2><h3>Now you can login to your account</h3>")
                error = "Email alerady exists"
                return render(request, "corto/index.html", {"error":error})
            else:
                error = "Password not matching"
                return render(request, "corto/index.html", {"error":error})
    return redirect(site)

def forgot(request):
    if request.method == 'POST':
        if 'email' in request.POST:
            mail = request.POST['email']
            
            try:
                Ur = User.objects.get(email=mail)
            except ObjectDoesNotExist:
                con = {
                    "error": "User not found"
                }
                return render(request, "corto/index.html", con)
            subject = "Forgot Password - CORTO URL SHORTNER"
            message = "\n\nDear " + str(Ur.fname) + " " + str(Ur.lname) + ",\nYour Login credentials for CORTO URL SHORTNER are as under :\n"
            message += "\nEmail : " + str(Ur.email) + "\nPassword : " + str(Ur.password) + "\n\nThank you for using CORTO"
            Sender = "Corto URL Shortner"
            to = [ str(Ur.email) ]
            send_mail(subject, message, Sender, to, fail_silently=True)
            return HttpResponse(mail)
    return redirect(site)

def analyse(request, url_id):
    con = {
        "id":url_id
    }
    try:
        url = Urls.objects.get(id=url_id)
        con = {
            "id":url_id,
            "url":url
        }
    except ObjectDoesNotExist:
        return HttpResponse("Url not found")
    except Exception as e:
        return HttpResponse(e)
    if "corto_user" in request.COOKIES:
        req_token = request.COOKIES['corto_user']
        try:
            db_token = User.objects.get(id=req_token)
            con = {
                "id":url_id,
                "url":url,
                "details": dash_data(db_token)
             }
        except ObjectDoesNotExist:
            return redirect("../")
    else:
        return redirect("../")
    devices_filter = Click.objects.filter(urlId=url)
    pc = devices_filter.filter(device="pc").count()
    tablet = devices_filter.filter(device="tablet").count()
    mobile = devices_filter.filter(device="mobile").count()
    other = devices_filter.filter(device="other").count()

    devices = {
        "pc":pc,
        "mobile":mobile,
        "tablet":tablet,
        "other":other
    }

    android = Click.objects.filter(urlId=url, platform__icontains="android").count()
    linux = Click.objects.filter(urlId=url, platform__icontains="linux").count()
    windows = Click.objects.filter(urlId=url, platform__icontains="windows").count()
    ios = Click.objects.filter(urlId=url, platform__icontains="ios").count()
    mac = Click.objects.filter(urlId=url, platform__icontains="mac").count()
    other = Click.objects.filter(urlId=url, platform__icontains="other").count()

    platforms = {
        "android": android,
        "linux":linux,
        "windows":windows,
        "ios":ios,
        "mac":mac,
        "other":other
    }

    chrome = Click.objects.filter(urlId=url, browser__icontains="Chrome").count()
    safari = Click.objects.filter(urlId=url, browser__icontains="Safari").count()
    opera = Click.objects.filter(urlId=url, browser__icontains="Opera").count()
    uc = Click.objects.filter(urlId=url, browser__icontains="UC").count()
    samsung = Click.objects.filter(urlId=url, browser__icontains="Samsung").count()
    android = Click.objects.filter(urlId=url, browser__icontains="Android").count()
    bot = Click.objects.filter(urlId=url, browser__icontains="bot").count()
    other = Click.objects.filter(urlId=url, browser__icontains="Other").count()

    browsers = {
        "chrome": chrome,
        "safari": safari,
        "opera": opera,
        "uc": uc,
        "samsung": samsung,
        "android": android,
        "bot": bot,
        "other": other
    }

    con = {
        "id":url_id,
        "url":url,
        "details": dash_data(db_token),
        "devices": devices,
        "platforms": platforms,
        "browser": browsers
    }
    # return HttpResponse(con.browser.android)
    return render(request, "corto/analyse.html", con)

def analyse_red(request):
    return redirect("../")

def logout(request):
    if "corto_user" in request.COOKIES:
        response = redirect(site)
        response.delete_cookie('corto_user')
        return response
