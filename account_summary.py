from finance import DB

# Загрузить, посчитать баланс, вывести
DB().filter(lambda t:
        t.place in [
            'Alipay',
            'RMB Наличка',
            'Альфа',
            'Альфа-Инвест',
        ]
    ).balance()
    # ).show()