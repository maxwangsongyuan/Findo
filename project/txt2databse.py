import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
if django.VERSION >= (1, 7):
    django.setup()


def main():
    from app.models import StockInfo
    f = open('StockInfos.txt')
    f1 = f.read().splitlines()
    for line in f1:
        date, symbol, price, id1 = line.split(' ')
        symbol1 = symbol[1:-1]
        StockInfo.objects.create(stock_id=id1, company_name=symbol1, price=price, date = date[1:-1])
    f.close()


if __name__ == "__main__":
    main()
    print('Done!')