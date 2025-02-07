from sqlalchemy.orm import Session
from api.core.base.services import Service
from api.utils.db_validators import check_model_existence
from api.v1.models.testimonial import Testimonial



class TestimonialService(Service):
    '''Product service functionality'''

    def create(self, db: Session,  schema):
        '''Create testimonial'''
        pass


    def fetch_all(self, page :int , page_size : int, db: Session):
        '''Fetch all testimonial with pagination'''
        offset = (page - 1) * page_size
        testimonials = db.query(Testimonial).offset(offset).limit(page_size).all()

        return testimonials
    

    def fetch(self, db: Session, id: str):
        '''Fetches a single testimonial id'''

        return check_model_existence(db, Testimonial, id)

    def update(self, db: Session, id: str, schema):
        '''Updates a testimonial'''
        pass

    def delete(self, db: Session, id: str):
        '''Deletes a specific testimonial'''

        testimonial = check_model_existence(db, Testimonial, id)
        
        db.delete(testimonial)
        db.commit()

    def delete_all(self, db: Session):
        '''Delete all testimonials'''
        try:
            db.query(Testimonial).delete()
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
 
testimonial_service = TestimonialService()