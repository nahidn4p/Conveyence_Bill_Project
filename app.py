from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

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


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        designation = request.form['designation']
        id_card = request.form['id_card']
        department = request.form['department']
        to = request.form['to']
        rate = request.form['rate']
        total_days = int(request.form['total_days'])
        overall_remarks = request.form['remarks']  # Capture single remarks input

        # Collect trips based on dynamic dates
        trips = []
        for i in range(total_days):
            trip_date = request.form.get(f'trip_date_{i}')
            trips.append({
                "date": trip_date,
                "from": "NHTE",
                "to": to,
                "days": 1,
                "way": 1,
                "rate": rate,
                "amount": rate,
                "remarks": overall_remarks  # Use the single remarks for all trips
            })

        # Create data dictionary
        total = int(rate) * total_days
        bill_date = datetime.now().strftime('%Y-%m-%d')

        # Determine month and year from the first trip date
        if trips:  # Check if trips is not empty
            first_trip_date = datetime.strptime(trips[0]['date'], '%Y-%m-%d')
            month_year = first_trip_date.strftime('%B %Y')  # Format to "October 2024"
        else:
            month_year = datetime.now().strftime('%B %Y')  # Fallback to current month if no trips

        # Redirect to the print_bill route
        return redirect(url_for('print_bill',
                                name=name,
                                designation=designation,
                                id_card=id_card,
                                department=department,
                                bill_date=bill_date,
                                trips=trips,
                                total=total,
                                remarks=overall_remarks,
                                month_year=month_year))  # Pass the new month_year

    return render_template('index.html')

@app.route('/print_bill')
def print_bill():
    name = request.args.get('name')
    designation = request.args.get('designation')
    id_card = request.args.get('id_card')
    department = request.args.get('department')
    bill_date_str = request.args.get('bill_date')

    # Ensure the date is in 'YYYY-MM-DD' format for parsing
    try:
        bill_date = datetime.strptime(bill_date_str, '%Y-%m-%d')
    except ValueError:
        return "Invalid date format", 400  # Handle invalid date format

    # Get the month and year passed from the redirect
    month_year = request.args.get('month_year')
    
    total = request.args.get('total')
    trips = request.args.getlist('trips')
    overall_remarks = request.args.get('remarks')

    # Convert total to words
    total_in_words = number_to_words(int(total))

    # Convert trips data from string to dictionary
    trips_data = [eval(trip) for trip in trips]  # Be cautious with eval; consider safer alternatives

    return render_template('print_bill.html', name=name, designation=designation, 
                           id_card=id_card, department=department, 
                           month_year=month_year, trips=trips_data, 
                           total=total, total_in_words=total_in_words,
                           overall_remarks=overall_remarks)

if __name__ == '__main__':
    app.run(debug=True)
