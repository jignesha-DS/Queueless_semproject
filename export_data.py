
import pandas as pd
from database import get_connection

connection = get_connection()

if connection:
    tables = [
        "users",
        "patients",
        "doctors",
        "tokens",
        "appointments",
        "notifications",
        "token_history",
        "doctor_breaks",
        "daily_analytics",
        "admins"
    ]

    try:
        with pd.ExcelWriter(
            "QueueLess_Database.xlsx",
            engine="openpyxl"
        ) as writer:

            for table in tables:
                try:
                    df = pd.read_sql(
                        f"SELECT * FROM `{table}`",
                        connection
                    )

                    df.to_excel(
                        writer,
                        sheet_name=table[:31],
                        index=False
                    )

                    print(f"{table}: {len(df)} records exported")

                except Exception as e:
                    print(f"{table}: Could not export - {e}")

        print("Excel export finished.")

    finally:
        connection.close()

else:
    print("Database connection failed.")
