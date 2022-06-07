from flask import Flask, render_template, request, redirect,url_for

import data_manager

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mentors')
def mentors_list():
    mentor_name = request.args.get('mentor-last-name')
    city_name = request.args.get('city_name')

    if mentor_name:
        details = data_manager.get_mentors_by_last_name(mentor_name)
    elif city_name:
        details = data_manager.get_mentors_by_city_name(city_name)
    else:
        details = data_manager.get_mentors()

    # We get back a list of dictionaries from the data_manager (for details check 'data_manager.py')

    return render_template('mentors.html', mentors=details)


@app.route('/applicants')
def applicants():
    data = data_manager.get_applicants()
    return render_template('applicants.html', elements=data)


@app.route('/applicant-phone')
def applicant_phone():
    applicant_name = request.args.get('applicant-name')
    applicant_email = request.args.get('applicant-email')
    if applicant_name:
        data = data_manager.get_applicants_byFirstName(applicant_name)
    elif applicant_email[0] == '@':
        data = data_manager.get_applicants_byEmail(applicant_email)
    else:
        return "mai incearca"

    return render_template('applicant-phone.html', elements=data)


@app.route('/applicants/<int:application_code>')
def get_applicant_byApplicationCode(application_code):
    data = data_manager.get_byApplication_code(application_code)
    return render_template('applicant.html', elements=data)


@app.route('/applicants/<int:application_code>/update', methods=["POST"])
def update_applicant(application_code):
    fPhone = request.form.get('fphone')
    data_manager.update_applicant_byApplication_code(fPhone, application_code)
    return redirect('/applicants')


@app.route('/applicants/add-applicants', methods=["GET", "POST"])
def add_applicants():
    if request.method == "POST":
        first_name = request.form.get("fn")
        last_name = request.form.get("ln")
        phone_number = request.form.get("pn")
        email = request.form.get("em")
        application_code = request.form.get("ac")
        data=data_manager.adding_new_applicant(
            first_name, last_name, phone_number, email, application_code)
        return redirect('/applicants')
    return render_template('add-applicant.html')


@app.route('/applicants/<int:application_code>/deleted')
def delete_applicant(application_code):
    data_manager.delete_applicant(application_code)
    return redirect('/applicants')



if __name__ == '__main__':
    app.run(debug=True)