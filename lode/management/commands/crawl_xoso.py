from django.core.management.base import BaseCommand
from scripts.crawl_xoso import crawl_xoso_full_table, filter_last_n_digits

class Command(BaseCommand):
    help = 'Crawl toàn bộ bảng xổ số và hiển thị tất cả các số, 2 số cuối, 3 số cuối'

    def handle(self, *args, **kwargs):
        all_numbers = crawl_xoso_full_table()
        last_2_digits = filter_last_n_digits(all_numbers, 2)
        last_3_digits = filter_last_n_digits(all_numbers, 3)
        self.stdout.write(self.style.SUCCESS(f'Tất cả các số xổ số: {all_numbers}'))
        self.stdout.write(self.style.SUCCESS(f'2 số cuối: {last_2_digits}'))
        self.stdout.write(self.style.SUCCESS(f'3 số cuối: {last_3_digits}')) 