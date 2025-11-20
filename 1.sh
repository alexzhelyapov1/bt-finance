# 10. 2025-10-25
python3 -B main.py add "Купил MOP (500 RMB)" 500 -t TRANSFER -p "RMB Наличка" -c CNY -r 11.8788 -d "2025-10-25"

python3 -B main.py add "Купил HKD (200 RMB)" 200 -t TRANSFER -p "RMB Наличка" -c CNY -r 11.8788 -d "2025-10-25"

# 11. 2025-10-26
python3 -B main.py add "Отдал 1000 АА (долг)" 1000 -t SPEND -p "RMB Наличка" -c CNY -r 11.8788 --cat "Duty" -d "2025-10-26" --tags "Duty"

# 12. 2025-10-27
python3 -B main.py add "Отдал 1000 АА для перевода на алипей" 1000 -t TRANSFER -p "RMB Наличка" -c CNY -r 11.8788 -d "2025-10-27"