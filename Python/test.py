from datetime import datetime, timedelta

date1 = datetime.today()
date2 = datetime(2020, 1, 24)

print((date2 - date1) < timedelta())
