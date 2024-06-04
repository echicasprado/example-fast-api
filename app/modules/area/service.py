from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc, desc
from typing import List

from modules.estado import EstadoEnum, EstadoModel
from .model import AreaModel
from .shema import Area, AreaCreate

class AreaServices():

    def get_all_areas(db: Session) -> List[Area]:
        areas = (
            db.query(AreaModel)
            .options(joinedload(AreaModel.estado))
            ).all()
        return areas
    
    def get_available_areas(db:Session) -> List[Area]:
        areas = (
            db.query(AreaModel)
            .filter(AreaModel.id_estado == EstadoEnum.ACTIVO)
            .options(joinedload(AreaModel.estado))
            ).all()
        return areas
    
    def get_area_by_parameters(db:Session, skip:int, limit:int, sort_by:str, order:str)->List[AreaModel]:
        order_by_column = getattr(AreaModel,sort_by)
 
        query = (
            db.query(AreaModel)
            .filter(AreaModel.id_estado == EstadoEnum.ACTIVO)
            .options(joinedload(AreaModel.estado))
            )

        if order == "desc":
            query = query.order_by(desc(order_by_column))
        else:
            query = query.order_by(asc(order_by_column))
        
        areas = query.offset(skip).limit(limit).all()
        return areas

    def get_area_by_id(db:Session, id_area:int) -> Area:
        return db.query(AreaModel).filter_by(id_estado = EstadoEnum.ACTIVO, id_area = id_area).options(joinedload(AreaModel.estado)).first()
    
    def get_area_by_descripcion(db:Session, descripcion:str) -> Area:
        return db.query(AreaModel).filter_by(id_estado = EstadoEnum.ACTIVO, descripcion = descripcion).options(joinedload(AreaModel.estado)).first()
    
    def create_area(db:Session, area:AreaCreate) -> Area:
        db_area = AreaModel(descripcion = area.descripcion, id_estado = EstadoEnum.ACTIVO)
        db.add(db_area)
        db.commit()
        db.refresh(db_area)
        db_area = db.query(AreaModel).filter_by(id_area = db_area.id_area).options(joinedload(AreaModel.estado)).first()
        return db_area
    
    def update_area(db:Session, id_area:int, area:AreaCreate) -> Area:
        db_area = db.query(AreaModel).filter_by(id_estado = EstadoEnum.ACTIVO, id_area = id_area).options(joinedload(AreaModel.estado)).first()

        if db_area != None:
            db_area.descripcion = area.descripcion
            db.commit()
            db.refresh(db_area)

        return db_area
    
    def delete_area(db:Session, id_area:int) -> Area:
        db_area = db.query(AreaModel).filter_by(id_estado = EstadoEnum.ACTIVO, id_area = id_area).options(joinedload(AreaModel.estado)).first()

        if db_area != None:
            db_area.id_estado = EstadoEnum.INACTIVO
            db.commit()
            db.refresh(db_area)

        return db_area