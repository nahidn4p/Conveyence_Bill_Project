from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session storage

def number_to_words(n):
    """Convert a number into words."""
    units = (
        "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
        "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
        "Seventeen", "Eighteen", "Nineteen"
    )
    tens = (
        "", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"
    )
    if n < 20:
        return units[n]
    elif n < 100:
        return tens[n // 10] + ('' if n % 10 == 0 else ' ' + units[n % 10])
    elif n < 1000:
        return units[n // 100] + " Hundred" + ('' if n % 100 == 0 else ' and ' + number_to_words(n % 100))
    elif n < 10000:
        return units[n // 1000] + " Thousand" + ('' if n % 1000 == 0 else ' ' + number_to_words(n % 1000))

    return str(n)  # Return as string if the number is larger than 9999


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        designation = request.form['designation']
        id_card = request.form['id_card']
        department = request.form['department']
        fr = request.form['from']
        to = request.form['to']
        rate = request.form['rate']
        total_days = int(request.form['total_days'])
        remarks = request.form['remarks']

        trips = []
        total = 0
        for i in range(total_days):
            trip_date = request.form.get(f'trip_date_{i}')
            in_time = request.form.get(f'in_time_{i}')
            out_time = request.form.get(f'out_time_{i}')
            way = int(request.form.get(f'way_{i}'))
            amount = int(rate) * way
            trips.append({
                "date": trip_date,
                "from": fr,
                "to": to,
                "in_time": in_time,
                "out_time": out_time,
                "days": 1,
                "way": way,
                "rate": rate,
                "amount": amount,
                "remarks": remarks
            })
            total += amount

        bill_date = datetime.now().strftime('%Y-%m-%d')
        if trips:
            first_trip_date = datetime.strptime(trips[0]['date'], '%Y-%m-%d')
            month_year = first_trip_date.strftime('%B %Y')
        else:
            month_year = datetime.now().strftime('%B %Y')

        # Store data in session
        session['form_data'] = {
            'name': name,
            'designation': designation,
            'id_card': id_card,
            'department': department,
            'bill_date': bill_date,
            'trips': trips,
            'total': total,
            'remarks': remarks,
            'month_year': month_year,
            'total_days': total_days
        }

        return redirect(url_for('print_bill'))

    return render_template('index.html')
@app.route('/print_bill')
def print_bill():
    form_data = session.get('form_data')
    if not form_data:
        return redirect(url_for('index'))

    total_in_words = number_to_words(int(form_data['total']))

    return render_template('print_bill.html',
                           name=form_data['name'],
                           designation=form_data['designation'],
                           id_card=form_data['id_card'],
                           department=form_data['department'],
                           bill_date=form_data['bill_date'],
                           month_year=form_data['month_year'],
                           trips=form_data['trips'],
                           total=form_data['total'],
                           total_in_words=total_in_words,
                           remarks=form_data['remarks'],
                           total_days=form_data['total_days'])
