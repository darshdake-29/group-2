from base import db
from base import app


class FilesVO(db.Model):
    __tablename__ = 'files_table'
    file_id = db.Column('file_id', db.Integer, primary_key=True,
                        autoincrement=True)
    file_name = db.Column('file_name', db.String(255), nullable=False, unique=True)
    

    def as_dict(self):
        return {
            'file_id': self.file_id,
            'file_name': self.file_name,
        }
        
        
class CattleVO(db.Model):
    __tablename__ = 'cattle_table'
    result_id = db.Column('result_id', db.Integer, primary_key=True,
                        autoincrement=True)
    cattle_file_id = db.Column('cattle_file_id', db.Integer, db.ForeignKey(FilesVO.file_id,
                                                      ondelete='CASCADE',
                                                      onupdate='CASCADE'), nullable=False)
    frame_id = db.Column('frame_id', db.Integer, nullable=False)
    cattle_counts = db.Column('cattle_counts', db.Integer, nullable=False)
    

    def as_dict(self):
        return {
            'result_id': self.result_id,
            'cattle_file_id': self.cattle_file_id,
            'frame_id': self.frame_id,
            'cattle_counts': self.cattle_counts,
        }


        
class GarbageVO(db.Model):
    __tablename__ = 'garbage_table'
    result_id = db.Column('result_id', db.Integer, primary_key=True,
                        autoincrement=True)
    garbage_file_id = db.Column('garbage_file_id', db.Integer, db.ForeignKey(FilesVO.file_id,
                                                      ondelete='CASCADE',
                                                      onupdate='CASCADE'), nullable=False)
    frame_id = db.Column('frame_id', db.Integer, nullable=False)
    garbage_counts = db.Column('garbage_counts', db.Integer, nullable=False)
    

    def as_dict(self):
        return {
            'result_id': self.result_id,
            'garbage_file_id': self.garbage_file_id,
            'frame_id': self.frame_id,
            'garbage_counts': self.garbage_counts,
        }


        
class PotholeVO(db.Model):
    __tablename__ = 'pothole_table'
    result_id = db.Column('result_id', db.Integer, primary_key=True,
                        autoincrement=True)
    pothole_file_id = db.Column('pothole_file_id', db.Integer, db.ForeignKey(FilesVO.file_id,
                                                      ondelete='CASCADE',
                                                      onupdate='CASCADE'), nullable=False)
    frame_id = db.Column('frame_id', db.Integer, nullable=False)
    pothole_counts = db.Column('pothole_counts', db.Integer, nullable=False)
    

    def as_dict(self):
        return {
            'result_id': self.result_id,
            'pothole_file_id': self.pothole_file_id,
            'frame_id': self.frame_id,
            'pothole_counts': self.pothole_counts,
        }




with app.app_context():
    db.create_all()