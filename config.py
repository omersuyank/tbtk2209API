from flask_sqlalchemy import SQLAlchemy

DATABASE_URI = (
    "mssql+pyodbc://huseyi98_tbtk2209db:zm3Y49k!1"
    "@104.247.167.130\\mssqlserver2022"
    "/huseyi98_tbtk2209db"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&TrustServerCertificate=yes"
    "&Encrypt=yes"
)

db = SQLAlchemy()
