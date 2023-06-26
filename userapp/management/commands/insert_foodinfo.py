from django.core.management.base import BaseCommand
from userapp.models import Foodinfo
import csv

class Command(BaseCommand):
    help = 'CSV 파일을 데이터베이스에 저장합니다.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV 파일 경로')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                model_instance = Foodinfo(
                foodname = row[0],
                kcal = float(row[2]),
                carbohydrate = float(row[3]),
                sugar = float(row[4]),
                fat = float(row[5]),
                protein = float(row[6]),
                sodium = float(row[7])
            )
                model_instance.save()

        self.stdout.write(self.style.SUCCESS('CSV 파일이 데이터베이스에 저장되었습니다.'))
