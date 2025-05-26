                                                =========Inventory and Sales Tracking System (CLI APP)=========

Welcome to the Inventory & Sales Tracking System! This is a simple, menu-driven command-line application built with Python and Microsoft SQL Server. It helps retail businesses keep track of products, customers, and sales — with features like invoice generation, CSV export/import, and stock alerts.

## Features:
    -> Product Management (Add, Update, Delete, Search, Import/Export CSV)

    -> Customer Management with Validation and CSV Import/Export

    -> Sales Recording with Auto-Invoice Generation

    -> Low Stock Alerts

    -> Daily and Monthly Sales Reports

    -> CSV Backup (import and export)

    -> Clean CLI Dashboard Navigation


## Techincal Requirements:
        -> Programming Language: Python 3.x

        -> Database: Microsoft SQL Server

        -> Libraries:
            > pyodbc – for SQL Server connection
            > csv, datetime, decimal, os, re – core modules


## Project Structure:
        inventory_sales/
        ├── billing.py          # Generates text invoice files
        ├── customers.py        # Customer management operations
        ├── db_config.py        # SQL Server connection setup
        ├── main.py             # CLI entry point with menu-driven dashboard
        ├── products.py         # Product management functions
        ├── sales.py            # Handles sale logic like create a sale, view sales....
        ├── utils.py            # Input handling helpers
        └── data/, reports/     # To store Exported CSV's and generated invoices (created at runtime)
## Setup Instructions:
        1. Install Dependencies:
            Ensure Python 3 is installed, then install pyodbc:
                -> pip install pyodbc        #run this in CLI

        2. Configure SQL Server:
            -> Create a database named retailstores in SQL Server.

            -> Set up the required tables (Products, Customers, Sales).

            -> Ensure Trusted_Connection=yes is configured for local integrated authentication and it will be connected with windows user       credentials.

        3. connect sql server with python using pyodbc library 

        4. Run the application in CLI and Use the CLI dashboard to manage products, customers, and sales


## CSV and Invoice Files:
        -> CSV exports and imports are saved in:
            path = C:\Users\YourName\Desktop\inventory_sales\data\

        -> Invoices are stored in:
            path = C:\Users\YourName\Desktop\inventory_sales\reports\invoices\

        These are my path directories (if we want you can defaultly update the paths)


## Smart Features:
        -> Auto-generates IDs for customers and products

        -> Validates names and phone numbers

        -> Auto-calculates tax and totals during checkout

        -> Saves every invoice as a receipt

        -> gives warning when stock is low

        -> handles CSV imports/exports easily by giving filename or path

