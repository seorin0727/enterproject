from django.core.management.base import BaseCommand
from userapp.models import Standard
import csv

class Command(BaseCommand):
    help = 'CSV 파일을 데이터베이스에 저장합니다.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV 파일 경로')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                model_instance = Standard(
                    gender = row[0],
                    sugar = int(row[1]),
                    sodium = int(row[2]),
                    fat_min = int(row[3]),
                    fat_max = int(row[4]),
                    protein_min = int(row[5]),
                    protein_max = int(row[6]),
                    carbohydrate_min = int(row[7]),
                    carbohydrate_max = int(row[8]),
                    kcal_min = int(row[9]),
                    kcal_max = int(row[10]),
                    age_min = int(row[11]),
                    age_max = int(row[12]),
            )
                model_instance.save()

        self.stdout.write(self.style.SUCCESS('CSV 파일이 데이터베이스에 저장되었습니다.'))
