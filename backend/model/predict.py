from django.conf import settings

import os
import sys
import pandas as pd

sys.path.append(
    os.path.join(os.path.dirname(__file__), '..')
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ucl_project.settings")

UCL_Finals_1955_2023_csv = os.path.join(settings.BASE_DIR, 'model', 'data', 'historical', 'UCL_Finals_1955-2023.csv')
UCL_AllTime_Performance_csv = os.path.join(settings.BASE_DIR, 'model', 'data', 'historical', 'UCL_AllTime_Performance_Table.csv')

df = pd.read_csv(UCL_AllTime_Performance_csv)
print(df.shape)
