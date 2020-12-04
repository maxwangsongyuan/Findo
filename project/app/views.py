from django.shortcuts import render
from django.template import loader
from . import adv1
# Create your views here.
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from .models import Test, StockInfo, FinancialProduct, StructuredFinancialInvestment
from .models import Users, UserClicks, UserSaves
from django.db import connection
from django.shortcuts import redirect
import numpy as np

"""
GLOBAL VARIABLES
"""
current_user = ""


def home(request):
    view_Stock = "<a href='http://127.0.0.1:8000/viewStock/'>Stock page</a>"  # link that go to database page
    view_FP = "<a href='http://127.0.0.1:8000/viewFP/'>FP page</a>"  # link that go to database page
    view_SFI = "<a href='http://127.0.0.1:8000/viewSFI/'>SFI page</a>"
    view_User = "<a href='http://127.0.0.1:8000/add_users_page/'>User Login page</a>"
    view_Clicks = "<a href='http://127.0.0.1:8000/all_users/'>Company Popularity page</a>"
    view_Predictions = "<a href='http://127.0.0.1:8000/ad1_page/'>Prediction page</a>"
    return render(request, "home.html", {"view_Stock": view_Stock, "view_FP": view_FP,
                                         "view_SFI": view_SFI, "view_User": view_User,
                                         "view_Clicks": view_Clicks, "view_Predictions": view_Predictions})


##################################################################################################################

# print names
def get_all_user_name(request):
    name = request.path
    tempt_test = Test.objects.raw('SELECT * FROM app_test')
    return HttpResponse(tempt_test)


# redirect to other page
def redirect_to_admin(request):
    return redirect(home)


# click then
def runoob(request):
    # views_insert = "<a href='http://127.0.0.1:8000/insert/'>insert </a>"      #link that go to insert page
    # views_update = "<a href='http://127.0.0.1:8000/update/'>update </a>"       #link that go to update page
    # views_delete = "<a href='http://127.0.0.1:8000/delete/'>delete </a>"      #link that go to delete page
    views_view = "<a href='http://127.0.0.1:8000/view/'>view</a>"  # link that go to view page

    # return render(request, "test.html", {"views_insert": views_insert, "views_update": views_update, "views_delete": views_delete, "views_view": views_view})
    return render(request, "test.html", {"views_view": views_view})


# view
def view(request):
    tempt_test = Test.objects.raw('SELECT * FROM app_test')
    return HttpResponse(tempt_test)


# insert
def insert(request):
    if request.method == 'POST' and request.POST:
        insert1 = request.POST.get('insert')
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO app_test (name) VALUES (%s)",
                [insert1])

    views_view = "<a href='http://127.0.0.1:8000/view/'>view</a>"
    return render(request, "test.html", {"views_view": views_view})


# update
def update(request):
    # if request.method == 'POST' and request.POST:
    #     insert1 = request.POST.get('update_to')
    #     delete1 = request.POST.get('update_from')
    #     with connection.cursor() as cursor:
    #         cursor.execute(
    #             "DELETE FROM app_test WHERE name = %s",
    #             [delete1])
    #         cursor.execute(
    #             "INSERT INTO app_test (name) VALUES (%s)",
    #             [insert1])

    if request.method == 'POST' and request.POST:
        update_f = request.POST.get('update_from')
        update_t = request.POST.get('update_to')
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE app_test SET name = %s where name = %s",
                [update_t, update_f])

    views_view = "<a href='http://127.0.0.1:8000/view/'>view</a>"
    return render(request, "test.html", {"views_view": views_view})


# delete
def delete(request):
    if request.method == 'POST' and request.POST:
        delete1 = request.POST.get('delete')
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM app_test WHERE name = %s",
                [delete1])

    views_view = "<a href='http://127.0.0.1:8000/view/'>view</a>"
    return render(request, "test.html", {"views_view": views_view})


###########################################################################################################################################
# this is dedicated for the stock page
def runStock(request):
    view_stock = "<a href='http://127.0.0.1:8000/viewStockDatabase/'>viewStockDatabase</a>"  # link that go to viewStockDatabase page

    view_FP = "<a href='http://127.0.0.1:8000/viewFP/'>FP page</a>"

    home_page = "<a href='http://127.0.0.1:8000/'>home page</a>"

    view_SFI = "<a href='http://127.0.0.1:8000/viewSFI/'>SFI page</a>"

    return render(request, "stock.html",
                  {"view_stock": view_stock, "view_FP": view_FP, "home_page": home_page, "view_SFI": view_SFI})


# insert
def insertStock(request):
    if request.method == 'POST' and request.POST:
        insert1 = request.POST.get('insertStockid')
        insert2 = request.POST.get('insertStockName')
        insert3 = request.POST.get('insertStockGR')
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO app_stockinfo (stock_id, company_name, growth_rate) VALUES (%s,%s,%s)",
                [insert1, insert2, insert3])

    view_stock = "<a href='http://127.0.0.1:8000/viewStockDatabase/'>viewStockDatabase</a>"  # link that go to viewStockDatabase page
    return render(request, "stock.html", {"view_stock": view_stock})


# search
def searchStockId(request):
    searchstock = request.POST.get('search_Stockid')

    flag = True

    for p in StockInfo.objects.raw('SELECT * FROM app_stockinfo where company_name = %s', [searchstock]):
        flag = False
        tmp = p

    if flag == True:
        return HttpResponse("The name is not found in data base.")
    click = UserClicks(user_id=current_user, company=tmp.company_name)
    click.save(using='mongo')

    return HttpResponse(tmp.stock_id)


def searchStockPrice(request):
    searchstockprice = request.POST.get('search_Stockprice')

    flag = True

    for p in StockInfo.objects.raw('SELECT * FROM app_stockinfo where company_name = %s', [searchstockprice]):
        flag = False
        tmp = p

    click = UserClicks(user_id=current_user, company=p.company_name)
    click.save(using='mongo')

    if flag == True:
        return HttpResponse("The price is not found in data base.")

    return HttpResponse(tmp.price)


def searchStockIdViaSFI(request):

    if request.method == 'POST' and request.POST:
        searchw = request.POST.get('search_StockIdViaSFI')

        with connection.cursor() as cursor:
            cursor.execute(
                'select * from app_stockinfo sto join app_structuredfinancialinvestment str on str.stock_id_id=sto.id where sto.stock_id = %s',
                [searchw])
            results = cursor.fetchall()

    if results == " ":
        return HttpResponse("Stock id not in data base")
    company_name = results[len(results) - 1][2]
    ret = "Company_name: " + str(results[len(results) - 1][2]) + ",  Price: " + str(
        results[len(results) - 1][3]) + ",  Date: " + str(
        results[len(results) - 1][4]) + ",  Knock in price: " + str(
        results[len(results) - 1][7]) + ", knock out price: " + str(
        results[len(results) - 1][8]) + ",  put strike price: " + str(results[len(results) - 1][9])

    click = UserClicks(user_id=current_user, company=company_name)
    click.save(using='mongo')

    return HttpResponse(ret)





# delete
def deleteStock(request):
    if request.method == 'POST' and request.POST:
        delete1 = request.POST.get('deleteStock')
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM app_stockinfo WHERE stock_id = %s",
                [delete1])

    view_stock = "<a href='http://127.0.0.1:8000/viewStockDatabase/'>viewStockDatabase</a>"  # link that go to viewStockDatabase page
    return render(request, "stock.html", {"view_stock": view_stock})


# view stock database
def viewStockDatabase(request):
    tmp = StockInfo.objects.raw('SELECT DISTINCT * FROM app_stockinfo')
    return HttpResponse(tmp)


###################################################################################################################################################################################
# this is dedicated for the structured financial investment page

def insertSFI(request):
    if request.method == 'POST' and request.POST:
        insert1 = request.POST.get('insert_fp_id')
        insert2 = request.POST.get('insert_stock_id')
        insert3 = request.POST.get('insert_SFI_id')
        insert4 = request.POST.get('insert_Knock_in')
        insert5 = request.POST.get('insert_Knock_out')
        insert6 = request.POST.get('insert_put_strike')

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO app_structuredfinancialinvestment (fp_id_id, stock_id_id, SFI_id, Knock_in, Knock_out, put_strike) VALUES (%s,%s, %s,%s,%s,%s)",
                [insert1, insert2, insert3, insert4, insert5, insert6])

    view_SFI = "<a href='http://127.0.0.1:8000/viewSFIDatabase/'>viewSFIDatabase</a>"
    return render(request, "StructuredFinancialInvestment.html", {"view_SFI": view_SFI})


def viewSFIDatabase(request):
    tmp = StructuredFinancialInvestment.objects.raw('SELECT * FROM app_structuredfinancialinvestment')
    return HttpResponse(tmp)


# delete
def deleteSFI(request):
    if request.method == 'POST' and request.POST:
        delete1 = request.POST.get('deleteSFI')
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM app_structuredfinancialinvestment WHERE SFI_id = %s",
                [delete1])

    view_SFI = "<a href='http://127.0.0.1:8000/viewSFIDatabase/'>viewSFIDatabase</a>"
    return render(request, "StructuredFinancialInvestment.html", {"view_SFI": view_SFI})


# update
def updateSFI(request):
    if request.method == 'POST' and request.POST:
        update_f = request.POST.get('update_SFI_from')
        update_t = request.POST.get('update_SFI_to')
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE app_structuredfinancialinvestment SET SFI_id = %s where SFI_id = %s",
                [update_t, update_f])

    view_SFI = "<a href='http://127.0.0.1:8000/viewSFIDatabase/'>viewSFIDatabase</a>"
    return render(request, "StructuredFinancialInvestment.html", {"view_SFI": view_SFI})


# search
def searchSFI(request):
    # if request.method == 'POST' and request.POST:
    #     search1 = request.POST.get('')
    #
    #     with connection.cursor() as cursor:
    #         cursor.execute(
    #             "SELECT * FROM app_structuredfinancialinvestment where SFI_id = %s",
    #             [search1])

    search1 = request.POST.get('search_SFI')

    for p in StructuredFinancialInvestment.objects.raw(
            'SELECT * FROM app_structuredfinancialinvestment where SFI_id = %s', [search1]):
        tmp = p
        company_name = p.stock_id

    click = UserClicks(user_id=current_user, company=company_name)
    click.save(using='mongo')

    return HttpResponse(tmp.Knock_in)

    # view_SFI = "<a href='http://127.0.0.1:8000/searchSFI/'>searchSFI</a>"
    # return render(request, "StructuredFinancialInvestment.html", {"view_SFI": view_SFI})


def runSFI(request):
    view_SFI = "<a href='http://127.0.0.1:8000/viewSFIDatabase/'>viewSFIDatabase</a>"

    view_FP = "<a href='http://127.0.0.1:8000/viewFP/'>FP page</a>"

    home_page = "<a href='http://127.0.0.1:8000/'>home page</a>"

    return render(request, "StructuredFinancialInvestment.html",
                  {"view_SFI": view_SFI, "home_page": home_page, "view_FP": view_FP})


######################################################################################################################
def insertFP(request):
    if request.method == 'POST' and request.POST:
        insert1 = request.POST.get('insert_fp_id')

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO app_financialproduct (fp_id) VALUES (%s)",
                [insert1])

    view_FP = "<a href='http://127.0.0.1:8000/viewFPDatabase/'>viewFPDatabase</a>"  # link that go to viewStockDatabase page
    return render(request, "financial_product.html", {"view_FP": view_FP})


# search
def searchFP(request):
    searchfp = request.POST.get('search_fp')

    for p in FinancialProduct.objects.raw('SELECT * FROM app_financialproduct where product_name = %s', [searchfp]):
        tmp = p

    return HttpResponse(tmp.fp_id)


def viewFPDatabase(request):
    tmp = FinancialProduct.objects.raw('SELECT * FROM app_financialproduct')

    return HttpResponse(tmp)


def runFP(request):
    view_FP = "<a href='http://127.0.0.1:8000/viewFPDatabase/'>view FP Database</a>"

    home_page = "<a href='http://127.0.0.1:8000/'>home page</a>"

    view_SFI = "<a href='http://127.0.0.1:8000/viewSFI/'>SFI page</a>"
    return render(request, "financial_product.html", {"view_FP": view_FP, "home_page": home_page, "view_SFI": view_SFI})


## Carol add## Carol add## Carol add## Carol add## Carol add## Carol add## Carol add
def viewdate(request):
    searchDate = request.POST.get('search_date')
    searchName = request.POST.get('search_name')

    flag = True

    for p in StockInfo.objects.raw('SELECT * FROM app_stockinfo where date = "2016-03-11" AND company_name = %s',
                                   [searchName]):
        flag = False
        tmp = p

    if flag == True:
        return HttpResponse("The date is not found in data base.")

    return HttpResponse(p.price)


## Carol add## Carol add## Carol add## Carol add## Carol add## Carol add## Carol add


"""
MongoDB Section Pages & Functions
"""


def all_users(request):
    users = UserClicks.object.using('mongo').all()
    stringval = "The following are all the company searched made by our users:<br>"
    count = 0
    for u in users:
        count = count + 1
        stringval += str(count) + ":" + u.company + "<br>"
    return HttpResponse(stringval)


def run_add_user(request):
    view_stock = "<a href='http://127.0.0.1:8000/viewStockDatabase/'>viewStockDatabase</a>"  # link that go to viewStockDatabase page
    view_FP = "<a href='http://127.0.0.1:8000/viewFPDatabase/'>view FP Database</a>"
    home_page = "<a href='http://127.0.0.1:8000/'>home page</a>"
    view_SFI = "<a href='http://127.0.0.1:8000/viewSFI/'>SFI page</a>"
    view_saved = "<a href='http://127.0.0.1:8000/mySaves/'>My Saved companies Page</a>"
    log_out = "<a href='http://127.0.0.1:8000/logout/'>Log Out</a>"
    return render(request, "user_login.html", {"view_stock": view_stock, "view_FP": view_FP,
                                      "home_page": home_page, "view_SFI": view_SFI,
                                      "view_saved": view_saved, "log_out": log_out})


@csrf_exempt
def insertUser(request):
    if request.method == 'POST' and request.POST:
        use_name = request.POST.get('username')
        password = request.POST.get('password')
        user = Users(use_name=use_name, password=password)
        user.save(using='mongo')

    return HttpResponse("Inserted User")


def loginUser(request):
    global current_user
    result = "could not log in"

    use_name = request.POST.get('username_login')
    password = request.POST.get('password_login')

    try:
        user = Users.object.using('mongo').get(use_name=use_name)
    except Users.DoesNotExist:
        raise Http404("User has not register")

    if current_user != "":
        return HttpResponse("Someone else is already here! Please log out first.")
    if user.password == password:
        result = "welcome " + use_name
        current_user = use_name

    return HttpResponse(result)


def userSaves(request):
    global current_user
    if current_user == "":
        return HttpResponse("Please log in first before saving")
    if request.method == 'POST' and request.POST:
        company = request.POST.get('company')
        userSave = UserSaves(user_id=current_user, company=company)
        userSave.save(using='mongo')
    return HttpResponse("userSaves")


def mySaves(request):
    global current_user
    saves = UserSaves.object.using('mongo').all()
    stringval = "Here are my favorites:"
    count = 0
    for u in saves:
        count = count + 1
        if current_user == u.user_id:
            stringval += str(count) + ":" + u.company + "<br>"
    return HttpResponse(stringval)


def logout(request):
    global current_user
    current_user = ""
    return HttpResponse("You have been logged out")


"""
Advance function 1
"""


#def ad1(request):

    #price_arr = np.empty(0)
    #year_arr = np.empty(0)
    #flag = True
    #seach_year = request.POST.get('seach_year')
    #seach_company_name = request.POST.get('seach_company_name')

    #for p in StockInfo.objects.raw('SELECT * FROM app_stockinfo where company_name = %s', [seach_company_name]):
    #    flag = False
    #    price_arr = np.append(price_arr, float(p.price))
    #    year_arr = np.append(year_arr, int(p.date[:3]))

    #if flag == True:
    #    return HttpResponse("The date is not found in data base.")
    #print("thisdbflrbafafe")
    #print(type(p.price))
    #result = adv1.price_prediction_model_via_linear_least_square(price_arr, year_arr, seach_year)

    #return HttpResponse(result)

def ad1(request):
    tuning_num = 10
    price_arr = np.empty(0)
    year_arr = np.empty(0)
    flag = True
    seach_year = request.POST.get('seach_year')
    seach_company_name = request.POST.get('seach_company_name')

    for p in StockInfo.objects.raw('SELECT * FROM app_stockinfo where company_name = %s', [seach_company_name]):
        flag = False
        price_arr = np.append(price_arr, float(p.price))
        year_arr = np.append(year_arr, int(p.date[:3]))

    if flag == True:
        return HttpResponse("The date is not found in data base.")
    print("thisdbflrbafafe")
    print(type(p.price))
    result1 = adv1.price_prediction_model_via_linear_least_square(price_arr, year_arr, seach_year)
    result1 = result1 / tuning_num
    result2 = adv1.reg(price_arr, year_arr, seach_year)
    res = "The first model predicts the stock price to be "+ str(result1) + " in " + seach_year +". " + str(result2)
    return HttpResponse(res)


def ad1_page(request):
    home_page = "<a href='http://127.0.0.1:8000/'>home page</a>"
    return render(request, "adv1.html", {"home_page": home_page})
