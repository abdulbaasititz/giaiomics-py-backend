from collections import defaultdict
import mysql.connector
import csv
from difflib import SequenceMatcher
import pdfkit
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import dask.dataframe as dd


# To Compare given genomic data into predefined data in db
# To generate Customize PDF

class GeneticDataAnalyzer:
    def getNgxAncestryReportData2(self, genecticFilePath):
        print('getReportData')
        exe_qry = "SELECT * from NgxAncestry"
        res_db_val = self.getAllDataFromSampleDB(self.conn, exe_qry)
        exeColumnName = ['snpRsid', 'snpName', 'riskAllele', 'genoType']
        if res_db_val != -1:
            def dateparse(gt1, gt2):
                return gt1 + gt2

            p2 = pd.read_csv(genecticFilePath, skiprows=19, usecols=[0, 3, 4],
                             names=['snpRsid', 'genoType1', 'genoType2'],
                             sep='\t', parse_dates={'genoType': ['genoType1', 'genoType2']},
                             date_parser=dateparse)
            p1 = pd.DataFrame(res_db_val, columns=['snpRsid', 'snpName', 'category', 'riskAllele'])
            p3 = p1.merge(p2, on=['snpRsid'], how='left').fillna("--")
            categorisedData = (p3.groupby(['category'], as_index=True)
                               .apply(lambda x: x[exeColumnName].to_dict('r'))
                               .reset_index()
                               .rename(columns={0: 'value'})
                               .to_json(orient='records'))
            return categorisedData
        else:
            print("No data in given sample DB")
            return -1
        print("DB closed")

    def getNgx23AndMeReportData2(self, genecticFilePath):
        exe_qry = "SELECT * from Ngx23AndMe"
        res_db_val = self.getAllDataFromSampleDB(self.conn, exe_qry)
        exeColumnName = ['snpRsid', 'geneAndVarient',
                         'pathway', 'variantMeaning', 'riskAllele', 'genoType']
        if res_db_val != -1:
            print("to compare sample data with patients data")
            dbColumnName = ['snpRsid', 'geneAndVarient', 'category',
                            'pathway', 'variantMeaning', 'riskAllele']

            exeColumnName = ['snpRsid', 'geneAndVarient',
                             'pathway', 'variantMeaning', 'riskAllele', 'genoType']
            p1 = pd.DataFrame(res_db_val, columns=dbColumnName)
            p2 = pd.read_csv(genecticFilePath, skiprows=20, usecols=[0, 3], names=['snpRsid', 'genoType'], sep='\t',
                             low_memory=True)
            df = pd.merge(p1, p2, on=['snpRsid'], how='left').fillna("--")
            # print(df.head())
            categorisedData = (df.groupby(['category'], as_index=True)
                               .apply(lambda x: x[exeColumnName].to_dict('r'))
                               .reset_index()
                               .rename(columns={0: 'value'})
                               .to_json(orient='records'))
            return categorisedData
        else:
            print("No data in given sample DB")
            return -1
        print("DB closed")

    def getNgx23AndMeReportData(self, genecticFilePath):
        exe_qry = "SELECT * from Ngx23AndMe"
        res_db_val = self.getAllDataFromSampleDB(self.conn, exe_qry)
        if res_db_val != -1:
            p2 = pd.read_csv(genecticFilePath, skiprows=20, usecols=[0, 3], names=['snpRsid', 'genoType'], sep='\t',
                             low_memory=True)
            p1 = pd.DataFrame(res_db_val, columns=['snpRsid', 'geneAndVarient', 'category', 'pathway', 'variantMeaning',
                                                   'riskAllele'])
            p3 = p1.merge(p2, on=['snpRsid'], how='left').fillna('--')
            finalValue = p3.to_json(orient='records')
            return finalValue
        else:
            print("No data in given sample DB")
            return -1
        print("DB closed")

    def getPgx23AndMeReportData(self, genecticFilePath):
        print('getReportData')
        exe_qry = "SELECT * from Pgx23AndMe"
        res_db_val = self.getAllDataFromSampleDB(self.conn, exe_qry)
        if res_db_val != -1:
            p2 = pd.read_csv(genecticFilePath, skiprows=20, usecols=[0, 3], names=['snpRsid', 'genoType'], sep='\t',
                             low_memory=True)
            p1 = pd.DataFrame(res_db_val, columns=['snpRsid', 'snpName', 'category', 'riskAllele'])
            p3 = p1.merge(p2, on=['snpRsid'], how='left').fillna("--")
            finalValue = p3.to_json(orient='records')
            return finalValue
        else:
            print("No data in given sample DB")
            return -1
        print("DB closed")



    def getNgxAncestryReportData(self, genecticFilePath):
        print('getReportData')
        exe_qry = "SELECT * from NgxAncestry"
        res_db_val = self.getAllDataFromSampleDB(self.conn, exe_qry)
        if res_db_val != -1:
            def dateparse(gt1, gt2):
                return gt1 + gt2

            p2 = pd.read_csv(genecticFilePath, skiprows=19, usecols=[0, 3, 4],
                             names=['snpRsid', 'genoType1', 'genoType2'],
                             sep='\t', parse_dates={'genoType': ['genoType1', 'genoType2']},
                             date_parser=dateparse)
            p1 = pd.DataFrame(res_db_val, columns=['snpRsid', 'snpName', 'category', 'riskAllele'])
            p3 = p1.merge(p2, on=['snpRsid'], how='left').fillna("--")
            finalValue = p3.to_json(orient='records')
            return finalValue
        else:
            print("No data in given sample DB")
            return -1
        print("DB closed")

    def getPgxAncestryReportData(self, genecticFilePath):
        print('getReportData')
        exe_qry = "SELECT * from PgxAncestry"
        res_db_val = self.getAllDataFromSampleDB(self.conn, exe_qry)
        if res_db_val != -1:
            def dateparse(gt1, gt2):
                return gt1 + gt2

            p2 = pd.read_csv(genecticFilePath, skiprows=19, usecols=[0, 3, 4],
                             names=['snpRsid', 'genoType1', 'genoType2'],
                             sep='\t', parse_dates={'genoType': ['genoType1', 'genoType2']}, date_parser=dateparse)
            p1 = pd.DataFrame(res_db_val, columns=['snpRsid', 'snpName', 'category', 'riskAllele'])
            p3 = p1.merge(p2, on=['snpRsid'], how='left').fillna("--")
            finalValue = p3.to_json(orient='records')
            return finalValue
        else:
            print("No data in given sample DB")
            return -1
        print("DB closed")

    # Main method to initilise
    def __init__(self):
        print('Constructor: PatientGenoComparator')

    def initMySqlDb(self):
        self.conn = self.createDBConnection()
        if self.conn == None:
            print('Connection Failed')
        else:
            print("DB connected")

    # Connect the localDB
    def createDBConnection(self):
        conn = None
        try:
            # conn = mysql.connector.connect(user='abdul', password='password',
            #                                host='localhost', database='genome')
            conn = mysql.connector.connect(user='root', password='password',
                                           host='207.180.233.17',port='9031', database='genomics')
        except Exception as e:
            print(e)
        return conn

    # Method to execute the query and return those data in list
    def getAllDataFromSampleDB(self, db_con, exe_qry):
        db_cur = db_con.cursor(buffered=True)
        print("get data from sample db")
        try:
            db_cur.execute(exe_qry)
            content = db_cur.fetchall()
        except Exception as e:
            print(e)
            return -1
        return content

    def closeDbConnection(self):
        self.conn.close()


# django celery
init = GeneticDataAnalyzer()
