# from fastapi.testclient import TestClient
# from app.main import app

# from app.database import get_db

# from sqlalchemy.orm import sessionmaker
# from app.config import settings
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from app.database import Base
# import pytest

# SQLALCHEMY_DATABASE_URL =f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# TestSessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = engine )

# @pytest.fixture(scope="module")
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @pytest.fixture(scope="module")
# def client(session):
#     def override_get_db():
#         db = TestSessionLocal()
#         try:
#             yield session
#         finally:
#             session.close()
        
#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app) #run our code before we return our test


