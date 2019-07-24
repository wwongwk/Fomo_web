import os

class Config:
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'fomochen51@gmail.com'
    MAIL_PASSWORD = 'f@123456'
    SECRET_KEY = 'c9970460fc2c3ad324add53c94e3bc2a'
    SQLALCHEMY_DATABASE_URI = 'postgres://bobby:zmq,bs2008@localhost:5432/app0'