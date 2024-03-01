from flask import redirect, render_template, flash, request
from base.com.service.detection_service import validate_login, perform_inference, get_file_data
from base import app
import os


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errorPage.html', error=error)


@app.route('/')
def load_admin_login_page():
    try:
        return render_template('admin/loginPage.html')
    except Exception as e:
        return render_template('errorPage.html', error=e)
    
    
@app.route('/login', methods=['POST'])
def verify_admin_login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        allow_login = validate_login(username, password)
        if allow_login:
            return redirect('/dashboard')
        return redirect('/')
    except Exception as e:
        return render_template('errorPage.html', error=e)


@app.route('/dashboard')
def load_admin_dashboard():
    try:
        return render_template('admin/dashboardPage.html')
    except Exception as e:
        return render_template('errorPage.html', error=e)
    
    
@app.route('/upload_file', methods=['POST'])
def admin_upload_file():
    try:
        uploaded_file = request.files.get('filename')
        selected_model = request.form.get('selectModel')
        result = perform_inference(uploaded_file, selected_model)
        file_id = result.get('file_id')
        file_type = result.get('type')
        model_name = result.get('model_name')
        return redirect(f'/results?file_id={file_id}&file_type={file_type}&model_name={model_name}')
    except Exception as e:
        return render_template('errorPage.html', error=e)
    
    
@app.route('/results')
def load_admin_results_page():
    try:
        file_id = request.args.get('file_id')
        file_type = request.args.get('file_type')
        model_name = request.args.get('model_name')
        vo_list = get_file_data(file_id, model_name)
        return render_template('admin/resultsPage.html', vo_list=vo_list, file_type=file_type, model_name=model_name)
    except Exception as e:
        return render_template('errorPage.html', error=e)


    