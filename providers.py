from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json

providers_app = Flask(__name__)
providers_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///providers.sqlite3'
# There was a warning in the logs about SQLALCHEMY_TRACK_MODIFICATIONS adding overhead
providers_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(providers_app)

# Basic index making sure everything works
@providers_app.route('/')
def hello():
    return 'Hello, Bain Challenge!'


# Providers model to give structure for entering data, querying
class Providers(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    drg_definition = db.Column(db.String(100))
    provider_id = db.Column(db.Integer)
    provider_name = db.Column(db.String(100))
    provider_street_address = db.Column(db.String(100))
    provider_city = db.Column(db.String(100))
    provider_state = db.Column(db.String(100))
    provider_zip_code = db.Column(db.Integer)
    hospital_referral_region_description = db.Column(db.String(100))
    total_discharges = db.Column(db.Integer)
    average_covered_charges = db.Column(db.Float)
    average_total_payments = db.Column(db.Float)
    average_medicare_payments = db.Column(db.Float)

    SERIAL_FIELDS = {
            'provider_name': 'Provider Name',
            'provider_street_address': 'Provider Street Address',
            'provider_city': 'Provider City',
            'provider_state': 'Provider State',
            'provider_zip_code': 'Provider Zip Code',
            'hospital_referral_region_description': 'Hospital Referral Region Description',
            'total_discharges': 'Total Discharges',
            'average_covered_charges': 'Average Covered Charges',
            'average_total_payments': 'Average Total Payments',
            'average_medicare_payments': 'Average Medicare Payments',
    }

    def __init__(self, drg_definition, provider_id, provider_name,
                 provider_street_address, provider_city, provider_state,
                 provider_zip_code, hospital_referral_region_description,
                 total_discharges, average_covered_charges,
                 average_total_payments, average_medicare_payments):
        self.drg_definition = drg_definition
        self.provider_id = provider_id
        self.provider_name = provider_name
        self.provider_street_address = provider_street_address
        self.provider_city = provider_city
        self.provider_state = provider_state
        self.provider_zip_code = provider_zip_code
        self.hospital_referral_region_description = hospital_referral_region_description
        self.total_discharges = total_discharges
        self.average_covered_charges = average_covered_charges
        self.average_total_payments = average_total_payments
        self.average_medicare_payments = average_medicare_payments

    def serialize(self):
        serial_dict = {}
        for key in self.__class__.SERIAL_FIELDS.keys():
            if key == 'provider_zip_code':
                serial_dict[self.__class__.SERIAL_FIELDS[key]] = str(getattr(self, key))
            elif key[0:7] == 'average':
                serial_dict[self.__class__.SERIAL_FIELDS[key]] = '${:,.2f}'.format(getattr(self, key))
            else:
                serial_dict[self.__class__.SERIAL_FIELDS[key]] = getattr(self, key)
        return serial_dict


# Route to run the script to load the data
@providers_app.route('/load_data')
def load_csv_data():
    file = './Inpatient_Prospective_Payment_System__IPPS__Provider_Summary_for_the_Top_100_Diagnosis-Related_Groups__DRG__-_FY2011.csv'
    column_names = []
    line_num = 1
    with open(file, 'r') as f:
        for line in f:
            raw_fields = line.split(',')
            # Capture and transform col names
            if 'DRG Definition' == raw_fields[0]:
                column_names = [fi.strip().lower().replace(' ', '_') for fi in raw_fields]
                continue
            # Getting the field values
            fields = []
            i = 0
            while i < len(raw_fields):
                if raw_fields[i][0] == '"':
                    # This means that there was a ',' somewhere in the middle
                    # of this field value and we need to group the rest of
                    # raw fields that were split up
                    concat_str = raw_fields[i]
                    while i < len(raw_fields) - 1:
                        # We're incrementing i here because we don't want to
                        # re-read the concatenated fields
                        i += 1
                        concat_str = concat_str + ',' + raw_fields[i]
                        if raw_fields[i][-1] == '"':
                            break
                    # Strip of quotes for DB storage
                    concat_str = concat_str.replace('"', '')
                    fields.append(concat_str)
                else:
                    fields.append(raw_fields[i])
                i += 1
            # Writing to DB
            try:
                model_values = {column_names[i]: fields[i] for i in range(len(fields))}
                # Data transformations
                model_values['provider_id'] = int(model_values['provider_id'])
                model_values['provider_zip_code'] = int(model_values['provider_zip_code'])
                model_values['total_discharges'] = int(model_values['total_discharges'])
                model_values['average_covered_charges'] = float(model_values['average_covered_charges'].replace('$', ''))
                model_values['average_total_payments'] = float(model_values['average_total_payments'].replace('$', ''))
                model_values['average_medicare_payments'] = float(model_values['average_medicare_payments'].strip().replace('$', ''))
                # Make model instance and write
                new_provider = Providers(**model_values)
                db.session.add(new_provider)
            except Exception as e:
                # If there is an issue, we want to log and continue
                print('Line %s Exception %s on fields: ', str(line_num), e)
                print(fields)
            # Flush to file on every 100th entry
            if line_num % 100 == 0:
                # Logging for my own development purposes
                print('Flush at %{}', str(line_num))
                db.session.commit()
            # Keeping track of line number for logging
            line_num += 1
    # Commit anything left over
    db.session.commit()
    # Helpful return text
    ret_text = "Finished {} lines".format(str(line_num))
    return ret_text


# JSON API route
@providers_app.route('/providers')
def get_data():
    ret_items = None
    # Get and parse query params
    p_query = Providers.query
    if not request.args:
        # If no query params, return first 10 results because there are _a lot_
        p_query = p_query.limit(10)
    else:
        # Query DB for matching providers with query params
        # These filter params are additive
        if request.args.get('max_discharges'):
            p_query = p_query.filter(Providers.total_discharges <= int(request.args.get('max_discharges')))
        if request.args.get('min_discharges'):
            p_query = p_query.filter(Providers.total_discharges >= int(request.args.get('min_discharges')))
        if request.args.get('max_average_covered_charges'):
            p_query = p_query.filter(Providers.average_covered_charges <= int(request.args.get('max_average_covered_charges')))
        if request.args.get('min_average_covered_charges'):
            p_query = p_query.filter(Providers.average_covered_charges >= int(request.args.get('min_average_covered_charges')))
        if request.args.get('max_average_medicare_payments'):
            p_query = p_query.filter(Providers.average_medicare_payments <= int(request.args.get('max_average_medicare_payments')))
        if request.args.get('min_average_medicare_payments'):
            p_query = p_query.filter(Providers.average_medicare_payments >= int(request.args.get('min_average_medicare_payments')))
        if request.args.get('state'):
            p_query = p_query.filter(Providers.provider_state == request.args.get('state'))
        # I added 'limit' for my own testing purposes
        if request.args.get('limit'):
            p_query = p_query.limit(int(request.args.get('limit')))
    # Fetch the models from the DB
    print(p_query)
    models = p_query.all()
    # Return JSON for model values
    serialized = [m.serialize() for m in models]
    response = providers_app.response_class(
        response=json.dumps(serialized),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    db.create_all()
    providers_app.run()
