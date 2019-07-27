import Scrapper
from User import User
import csv
from dateutil.parser import parse

"""User dataset file name"""
user_db = 'ACM BIT Mesra (Coder of the Month) (Responses).csv'

start_date = parse('2019-05-01 00:00:00')
end_date = parse('2019-06-30 23:59:59')

cf_scrapper = Scrapper.CF_Scrapper()
cc_scrapper = Scrapper.CC_Scrapper()
cf_scrapper.scrape_contests(start_date, end_date)
cc_scrapper.scrape_contests(start_date, end_date)

user_list = []
with open(user_db, 'r') as f:
    csv_reader = csv.DictReader(f)
    for entry in csv_reader:
        user = User(entry['Name'], entry['Email Address'], entry['Profile Picture (To be Displayed on ACM Website)'], entry['Codeforces Profile Link'], entry['CodeChef Profile Link'])
        cf_scrapper.scrape_user_submissions(user)
        cc_scrapper.scrape_user_submissions(user)
        user.get_total_sol()
        print(user.name, 'CF: ', user.cf_sol, 'CC: ', user.cc_sol, 'Total: ', user.get_total_sol())
        user_list.insert(len(user_list), user)
    sorted_list = sorted(user_list, key=lambda user: user.total_sol)
    with open('result.csv', 'w') as r:
        label = ['name', 'email', 'CodeForces', 'CodeChef', 'Total', 'imageURL']
        csv_writer = csv.writer(r)
        csv_writer.writerow(label)
        for u in sorted_list:
            csv_writer.writerow([u.name, u.email, u.cf_sol, u.cc_sol, u.total_sol, u.url])
