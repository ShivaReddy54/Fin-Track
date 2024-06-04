from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from app.models import Accounts, Comments
import json

def index(request):
    return HttpResponse("This is my first web page ")


def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobil = request.POST.get('phno')
        comnt = request.POST.get('comment')

        entry = Comments.objects.create(
            name = name,
            mobil = mobil,
            comment = comnt
        )
        entry.save()

        return HttpResponse("<center> <h1> Thanks! Have a Good Day </h1> </center>")

    return render(request, "index.html")


def history(request):
    documents = Accounts.objects.all()

    data = []
    for idx, doc in enumerate(documents, start=1):
        data.append({
            's_no': idx,
            'date': doc.date,
            'agent_name': doc.full_name,
            'total_amount': sum([int(amount) for amount in doc.page_amounts.split(',') if amount.strip()])
        })

    return render(request, "history.html", {'data': data})

def account(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        day = request.POST.get('day')
        pages = request.POST.get('pages')
        pages_total = request.POST.get('pages-total').split(',') if request.POST.get('pages-total') else []
        newacnts = request.POST.get('newacnts')
        bf = request.POST.get('bf')
        expenditures = request.POST.get('expenditures')

        pages = sum(map(int, pages_total))
        accounts = []
        acnt_total = acnt_interest = 0
        if newacnts is not None:
            for i in range(1, int(newacnts) + 1):
                account_num = request.POST.get(f'acntnum{i}')
                account_area = request.POST.get(f'acntarea{i}')
                account_amount = request.POST.get(f'acntamount{i}')
                account_interest = request.POST.get(f'acntinterest{i}')
                if account_amount is not None:
                    acnt_total += int(account_amount)
                if account_interest is not None:
                    acnt_interest += int(account_interest)
                accounts.append((account_num, account_area, account_amount, account_interest))

        final = (pages + acnt_total) - int(expenditures)
        data = {
            'date': date,
            'day': day,
            'pages': pages,
            'pages_total': pages_total,
            'newacnts': newacnts,
            'bf': bf,
            'acnt_total': acnt_total,
            'acnt_interest': acnt_interest,
            'expenditures': expenditures,
            'accounts': accounts,
            'final': final
        }

        return render(request, 'sheet.html', data)
    return render(request, "account.html")

def addtodb(request):
    if request.method == 'POST':
        full_name = request.POST.get('Name')
        date = request.POST.get('Date')
        no_of_pages = int(request.POST.get('Pages'))

        amounts_list = []
        for page_number in range(1, no_of_pages + 1):
            page_amounts = [int(amount) for amount in request.POST.get(f'amount_{page_number}').split(',') if
                            amount.strip()]
            summ = sum(page_amounts)
            amounts_list.append(str(summ))

        amount = ', '.join(amounts_list)

        # Debugging: Print page_amounts_data
        print("Page Amounts Data:", amount)

        # Create and save Accounts entry
        entry = Accounts.objects.create(
            full_name=full_name,
            date=date,
            no_of_pages=no_of_pages,
            page_amounts=amount
        )
        entry.save()

        return HttpResponse("<center> <h1> Successful </h1> </center> ")
    else:
        return render(request, 'addtodb.html')

def checkdb(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        documents = Accounts.objects.filter(date=date)

        data = {}
        results = []
        for doc in documents:
            page_amounts_list = [int(amount) for amount in doc.page_amounts.split(',') if amount.strip()]
            summ = sum(page_amounts_list)
            results.append({
                'full_name': doc.full_name,
                'date': doc.date,
                'no_of_pages': doc.no_of_pages,
                'page_amounts': page_amounts_list,  # Pass the list of amounts directly
                'total_amount': summ
            })

        data['results'] = results
        data['input_date'] = date

        return render(request, "checkdb.html", data)

    return render(request, "checkdb.html")




