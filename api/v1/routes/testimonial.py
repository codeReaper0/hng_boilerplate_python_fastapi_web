#!/usr/bin/env python3
"""
Module contains CRUD routes for testimonial
"""
from fastapi.encoders import jsonable_encoder
from api.db.database import get_db
from sqlalchemy.orm import Session
from api.v1.models.user import User
from fastapi import Depends, APIRouter, status,Query
from api.utils.success_response import success_response
from api.v1.services.testimonial import testimonial_service
from api.v1.services.user import user_service

testimonial = APIRouter(prefix='/testimonials', tags=['Testimonial'])


@testimonial.get('', status_code=status.HTTP_200_OK)
def get_testimonials(
    db: Session = Depends(get_db),
    page : int = Query(1, gt=0),
    page_size : int = Query(10, gt=0)
):
    """End point to Query Testimonials with pagination"""

    testimonials = testimonial_service.fetch_all(page= page , page_size=page_size, db=db)
    return {
        'status_code' :  status.HTTP_200_OK,
        'message' : 'Testimonials fetched Successfully',
        'data': [jsonable_encoder(testimonial) for testimonial in testimonials]
        }


@testimonial.get('/{testimonial_id}', status_code=status.HTTP_200_OK)
def get_testimonial(
    testimonial_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user)
):
    '''Endpoint to get testimonial by id'''

    testimonial = testimonial_service.fetch(db, testimonial_id)

    return success_response(
        status_code=200,
        message=f'Testimonial {testimonial_id} retrieved successfully',
        data=jsonable_encoder(testimonial)
    )


@testimonial.delete("/{testimonial_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_testimonial(
    testimonial_id: str,
    current_user: User = Depends(user_service.get_current_super_admin),
    db: Session = Depends(get_db)
):
    """
    Function for deleting a testimonial based on testimonial id
    """

    testimonial_service.delete(db, testimonial_id)


@testimonial.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_testimonials(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_super_admin),
):
    """
    Deletes all testimonials
    """

    testimonial_service.delete_all(db)
