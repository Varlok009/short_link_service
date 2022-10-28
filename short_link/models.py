from sqlalchemy import Column, Integer, String
from short_link.db import Base, db_session
from short_link.builder_short_link import build_short_postfix


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    original_link = Column(String())
    short_postfix = Column(String())

    class Config:
        orm_mode = True

    @staticmethod
    def check_short_postfix_in_db(original_link: str):
        return db_session.query(Link).filter(Link.original_link == original_link).first()

    @staticmethod
    def add_link(original_link: str) -> str:
        if x := Link.check_short_postfix_in_db(original_link):
            return x.short_postfix

        link = Link(**{
            'original_link': original_link,
            'short_postfix': build_short_postfix(),
        })
        try:
            db_session.add(link)
            db_session.commit()
        except:
            print(f'error for add {link.original_link}')
            db_session.rollback()
        return link.short_postfix

    @staticmethod
    def get_original_link(short_postfix: str) -> str:
        link = db_session.query(Link).filter(Link.short_postfix == short_postfix).first()
        return link.original_link

    def __repr__(self) -> str:
        return f'link {self.id}, {self.short_postfix} / {self.original_link}'
