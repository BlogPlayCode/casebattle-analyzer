import json
from colorama import Fore, Style, init
init(autoreset=True)

def load_data(filename):
    """Загрузка данных из файла"""
    if not filename.endswith('.txt'):
        filename += ".txt"
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().strip()

def parse_items(data, case_price):
    """Парсинг предметов и подсчет статистики"""
    items = {}
    fatal_count = fail_count = bad_count = okay_count = 0
    good_count = very_count = nice_count = impossible_count = 0

    for i in data.split('<span class="__currency">')[1:]:
        price = float(i.split('</span>')[0].replace(" ", ""))
        name = i.split('<div class="unit-title">')[1].split('</div>')[0].strip().replace('<br>', ' | ').strip()
        status = round(price/case_price, 3)
        
        if status >= 2:
            status = int(round(status, 0))
        
        if status < 0.4:
            status = "fatal fail"
            fatal_count += 1
        elif status < 0.75:
            status = "fail"
            fail_count += 1
        elif status < 1:
            status = "bad"
            bad_count += 1
        elif status < 1.25:
            status = "okay..."
            okay_count += 1
        elif status < 1.7:
            status = "good"
            good_count += 1
        elif status < 2:
            status = "very good"
            very_count += 1
        elif status < 5:
            status = "NIIICE"
            nice_count += 1
        else:
            status = "IMPOSSIBLE"
            impossible_count += 1

        items[name] = (status, price)
    
    return items, {
        'fatal_count': fatal_count,
        'fail_count': fail_count,
        'bad_count': bad_count,
        'okay_count': okay_count,
        'good_count': good_count,
        'very_count': very_count,
        'nice_count': nice_count,
        'impossible_count': impossible_count
    }

def calculate_additional_stats(items, counts):
    """Расчет дополнительной статистики"""
    real_count = len(items) - counts['nice_count'] - counts['impossible_count']
    bad_cases = counts['fatal_count'] + counts['fail_count'] + counts['bad_count']
    good_cases = counts['okay_count'] + counts['good_count'] + counts['very_count']
    return real_count, bad_cases, good_cases

def print_main_stats(items, counts):
    """Печать основной статистики"""
    total = len(items)
    print(f"Total: {total}\n")
    
    print(Fore.RED + Style.BRIGHT + 
          f"Fatal fail: {counts['fatal_count']} ({int(counts['fatal_count']*100/total)}%)")
    
    print(Fore.RED + 
          f"Fail: {counts['fail_count']} ({int(counts['fail_count']*100/total)}%)")
    
    print(Fore.YELLOW + 
          f"Bad: {counts['bad_count']} ({int(counts['bad_count']*100/total)}%)")
    
    print(f"Okay: {counts['okay_count']} ({int(counts['okay_count']*100/total)}%)")
    
    print(Fore.GREEN + 
          f"Good: {counts['good_count']} ({int(counts['good_count']*100/total)}%)")
    
    print(Fore.GREEN + Style.BRIGHT + 
          f"Very good: {counts['very_count']} ({int(counts['very_count']*100/total)}%)")
    
    print(Fore.GREEN + Style.BRIGHT + 
          f"NICE: {counts['nice_count']} ({int(counts['nice_count']*100/total)}%)")
    
    print(Fore.MAGENTA + 
          f"IMPOSSIBLE: {counts['impossible_count']} ({int(counts['impossible_count']*100/total)}%)")
    
    print("\n" + "-"*32)

def print_real_stats(real_count, counts):
    """Печать реальной статистики"""
    print("\nReal stats:")
    print(f"Total: {real_count}")
    print(f"Fakes: {real_count - counts['nice_count'] - counts['impossible_count']}\n")
    
    print(Fore.RED + Style.BRIGHT + 
          f"Fatal fail: {counts['fatal_count']} ({int(counts['fatal_count']*100/real_count)}%)")
    
    print(Fore.RED + 
          f"Fail: {counts['fail_count']} ({int(counts['fail_count']*100/real_count)}%)")
    
    print(Fore.YELLOW + 
          f"Bad: {counts['bad_count']} ({int(counts['bad_count']*100/real_count)}%)")
    
    print(Fore.CYAN + 
          f"Okay: {counts['okay_count']} ({int(counts['okay_count']*100/real_count)}%)")
    
    print(Fore.GREEN + 
          f"Good: {counts['good_count']} ({int(counts['good_count']*100/real_count)}%)")
    
    print(Fore.GREEN + Style.BRIGHT + 
          f"Very good: {counts['very_count']} ({int(counts['very_count']*100/real_count)}%)")
    
    print("\n" + "-"*32)

def print_final_stats(real_count, bad_cases, good_cases):
    """Печать финальных показателей и вердикта"""
    print(f"\nBAD DROPS: {bad_cases} ({int(bad_cases*100/real_count)}%)" + Fore.RED)
    print(f"GOOD DROPS: {good_cases} ({int(good_cases*100/real_count)}%)" + Fore.GREEN)
    print("\n" + "-"*32 + "\n")
    
    if good_cases*100/real_count > 50:
        print(Fore.GREEN + Style.BRIGHT + "✅ GOOD CASE")
    else:
        print(Fore.RED + Style.BRIGHT + "❌ BAD CASE")

def main():
    """Главная функция управления программой"""
    filename = input("Enter filename:\n> ").strip()
    case_price = int(input("Enter case price:\n> "))
    
    data = load_data(filename)
    items, counts = parse_items(data, case_price)
    real_count, bad_cases, good_cases = calculate_additional_stats(items, counts)
    
    print_main_stats(items, counts)
    print_real_stats(real_count, counts)
    print_final_stats(real_count, bad_cases, good_cases)

if __name__ == "__main__":
    main()
    