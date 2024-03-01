"""
Problems: 
Improvements: 
1. We can create two seperate files one for image and other for video to improve readability.
"""


import cv2 
from ultralytics import YOLO
from base.com.vo.detection_vo import FilesVO, GarbageVO, PotholeVO, CattleVO
from base.com.dao.detection_dao import FilesDAO, GarbageDAO, PotholeDAO, CattleDAO
import os
from werkzeug.utils import secure_filename
from base import app


def validate_login(username, password):
    """
    This function will validate the input credentials.
    """
    try:
        if username == 'admin' and password == 'darsh@29':
            return True  
        return False
    except Exception as e:
        raise e
    
def garbage_count_save(garbage_file_id, frame_id, counts):
    garbage_vo = GarbageVO()
    garbage_vo.garbage_file_id = garbage_file_id
    garbage_vo.frame_id = frame_id
    garbage_vo.garbage_counts = counts
    garbage_dao = GarbageDAO()
    garbage_dao.insert_counts(garbage_vo)
    
    
def pothole_count_save(pothole_file_id, frame_id, counts):
    pothole_vo = PotholeVO()
    pothole_vo.pothole_file_id = pothole_file_id
    pothole_vo.frame_id = frame_id
    pothole_vo.pothole_counts = counts
    pothole_dao = PotholeDAO()
    pothole_dao.insert_counts(pothole_vo)
    
    
def cattle_count_save(cattle_file_id, frame_id, counts):
    cattle_vo = CattleVO()
    cattle_vo.cattle_file_id = cattle_file_id
    cattle_vo.frame_id = frame_id
    cattle_vo.cattle_counts = counts
    cattle_dao = CattleDAO()
    cattle_dao.insert_counts(cattle_vo)
    

def perform_inference(uploaded_file, model_name):
    """
    This function will take a file and perform detection and store the output.
    """
    try:
        files_vo = FilesVO()
        files_dao = FilesDAO()
        filename = secure_filename(uploaded_file.filename)
        
        # handling files with same name
        if files_dao.check_file_exists(filename):
            name, ext = os.path.splitext(filename)
            index = 1
            while True:
                new_filename = f"{name} ({index}){ext}"
                if not files_dao.check_file_exists(new_filename):
                    filename = new_filename
                    break 
                index += 1
                
        # model loading
        model_path = os.path.join(app.config['MODEL_PATH'], f'{model_name}.pt')
        model = YOLO(model_path)
        
        # saving filename in database
        files_vo.file_name = filename 
        files_dao.insert_file(files_vo)
        filename_lower = filename.lower()
        
        # select classes according to the model 
        if model_name == 'cattle':
            classes = [15, 16, 17, 18, 19, 20, 21, 22, 23]
        elif model_name == 'pothole':
            classes = [1]
        else:
            classes = [0]
        
        # if uploaded file is an image
        if filename_lower.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_save_path = os.path.join(app.config['UPLOAD_PATH'], 'images', filename)
            output_save_path = os.path.join(app.config['OUTPUT_PATH'], 'images', filename)
            uploaded_file.save(file_save_path)
            image = cv2.imread(file_save_path)
            results = model.predict(image, classes=classes)
            counts = len(results[0])
            annotated_frame = results[0].plot()
            cv2.imwrite(output_save_path, annotated_frame)
            frame_id = 1
            file_id = files_dao.get_file_id(filename)
            if model_name == 'garbage':
                garbage_count_save(file_id, frame_id, counts)
            elif model_name == 'pothole':
                pothole_count_save(file_id, frame_id, counts)
            elif model_name == 'cattle':
                cattle_count_save(file_id, frame_id, counts)
            return {'file_id': file_id, 'type': 'image', 'model_name': model_name}
            
        
        # if uploaded file is an video
        elif filename_lower.endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv')):
            file_save_path = os.path.join(app.config['UPLOAD_PATH'], 'videos', filename)
            output_save_path = os.path.join(app.config['OUTPUT_PATH'], 'videos', filename)
            uploaded_file.save(file_save_path)
            cap = cv2.VideoCapture(file_save_path)
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            codec = int(cap.get(cv2.CAP_PROP_FOURCC))
            fourcc = cv2.VideoWriter_fourcc(*chr(codec & 0xFF), chr((codec >> 8) & 0xFF), chr((codec >> 16) & 0xFF), chr((codec >> 24) & 0xFF))
            save_fps = 1
            out = cv2.VideoWriter(output_save_path, fourcc, save_fps, (frame_width, frame_height))
            frame_count = 0
            frame_id = -1
            file_id = files_dao.get_file_id(filename)
            while cap.isOpened():
                success, frame = cap.read()
                if success:
                    frame_count += 1
                    if frame_count % fps == 0:
                        frame_id += 1
                        results = model.predict(frame, classes=classes)
                        counts = len(results[0])
                        annotated_frame = results[0].plot()
                        out.write(annotated_frame)
                        if model_name == 'garbage':
                            garbage_count_save(file_id, frame_id, counts)
                        elif model_name == 'pothole':
                            pothole_count_save(file_id, frame_id, counts)
                        elif model_name == 'cattle':
                            cattle_count_save(file_id, frame_id, counts)
                    else:
                        continue
                else:
                    break
            cap.release()
            out.release()
            return {'file_id': file_id, 'type': 'video', 'model_name': model_name}
            
        # other file formats are not allowed
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        raise e
    
    
def get_file_data(file_id, model_name):
    """
    This function calls function of DAO to fetch data for particular file.
    """
    if model_name == 'garbage':
        garbage_dao = GarbageDAO()
        garbage_vo_list = garbage_dao.get_file_data(file_id)
        return garbage_vo_list
    
    elif model_name == 'cattle':
        cattle_dao = CattleDAO()
        cattle_vo_list = cattle_dao.get_file_data(file_id)
        return cattle_vo_list

    elif model_name == 'pothole':
        pothole_dao = PotholeDAO()
        pothole_vo_list = pothole_dao.get_file_data(file_id)
        return pothole_vo_list
    