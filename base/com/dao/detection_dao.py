from base import db
from base.com.vo.detection_vo import FilesVO, PotholeVO, GarbageVO, CattleVO


class FilesDAO:
    def insert_file(self, files_vo):
        db.session.add(files_vo)
        db.session.commit()

    def check_file_exists(self, filename):
        existing_file = FilesVO.query.filter_by(file_name=filename).first()
        return existing_file is not None
    
    def get_file_id(self, filename):
        file_vo = FilesVO.query.filter_by(file_name=filename).first()
        return file_vo.file_id


class CattleDAO:
    def insert_counts(self, cattle_vo):
        db.session.add(cattle_vo)
        db.session.commit()
        
    def get_file_data(self, file_id):
        cattle_vo_list = db.session.query(
            CattleVO, FilesVO).filter(
                CattleVO.cattle_file_id == FilesVO.file_id, 
                FilesVO.file_id == file_id).all()
        return cattle_vo_list


class GarbageDAO:
    def insert_counts(self, garbage_vo):
        db.session.add(garbage_vo)
        db.session.commit()
        
    def get_file_data(self, file_id):
        garbage_vo_list = db.session.query(
            GarbageVO, FilesVO).filter(
                GarbageVO.garbage_file_id == FilesVO.file_id, 
                FilesVO.file_id == file_id).all()
        return garbage_vo_list
  
    
class PotholeDAO:
    def insert_counts(self, pothole_vo):
        db.session.add(pothole_vo)
        db.session.commit()
        
    def get_file_data(self, file_id):
        pothole_vo_list = db.session.query(
            PotholeVO, FilesVO).filter(
                PotholeVO.pothole_file_id == FilesVO.file_id, 
                FilesVO.file_id == file_id).all()
        return pothole_vo_list
    
    
