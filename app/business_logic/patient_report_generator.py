from jinja2 import Template
from io import StringIO
import pdfkit
from collections import defaultdict
import json
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
from jinja2 import Environment, FileSystemLoader
import pandas as pd


class PdfReportGenerator:

    def __init__(self):
        print('Constructor: PdfReportGenerator')

    def convertHtmlToPdf3(self, geneticModifiedReportData, reportMetaData):
        print("convertHtmlToPdf3")
        pdfTemplateDir = os.getcwd() + '/app/business_logic/template3'
        genecticReportType = reportMetaData['geneticReportType']
        geneticFileCompanyType = reportMetaData['geneticFileCompanyType']
        geneticReportReferenceNumber = reportMetaData['referenceNumber']
        self.saveProcessedHeader3(genecticReportType, geneticFileCompanyType, geneticReportReferenceNumber)

        template = ''
        if geneticFileCompanyType == "23AndMe" and genecticReportType == "NGX":
            print("Set template for Ngx23AndMeTemplate")
            template = open(pdfTemplateDir + "/NgxBody.html")

        # geneticData = json.loads(geneticModifiedReportData)
        print("cp8")
        jinjaTemplater = Template(template.read())
        print("cp9")
        reportBodyHtml = jinjaTemplater.render(reportingData = geneticModifiedReportData)
        print("cp10")
        wkhtmltopdf_options = {
            'enable-local-file-access': None,
            'javascript-delay': 2000000
        }
        pdf = pdfkit.from_string(reportBodyHtml, False, {'--header-html': pdfTemplateDir + '/processed-header.html',
                                                         '--footer-html': pdfTemplateDir + '/footer.html','enable-local-file-access':None})

        return pdf

    def convertHtmlToPdf2(self, geneticModifiedReportData, reportMetaData):
        print("convertHtmlToPdf2")
        pdfTemplateDir = os.getcwd() + '/app/business_logic/templates'
        genecticReportType = reportMetaData['geneticReportType']
        geneticFileCompanyType = reportMetaData['geneticFileCompanyType']
        geneticReportReferenceNumber = reportMetaData['referenceNumber']
        self.saveProcessedHeader(genecticReportType, geneticFileCompanyType, geneticReportReferenceNumber)

        template = ''
        if geneticFileCompanyType == "23AndMe" and genecticReportType == "NGX":
            print("Set template for Ngx23AndMeTemplate")
            template = open(pdfTemplateDir + "/Ngx23AndMeTemplate.html")

        if geneticFileCompanyType == "23AndMe" and genecticReportType == "PGX":
            template = open(pdfTemplateDir + "/Pgx23AndMeTemplate.html")

        if geneticFileCompanyType == "Ancestry" and genecticReportType == "NGX":
            template = open(pdfTemplateDir + "/NgxAncestryTemplate.html")

        if geneticFileCompanyType == "Ancestry" and genecticReportType == "PGX":
            template = open(pdfTemplateDir + "/PgxAncestryTemplate.html")

        geneticData = json.loads(geneticModifiedReportData)
        print("cp8")
        jinjaTemplater = Template(template.read())
        print("cp9")
        reportBodyHtml = jinjaTemplater.render(reportingData = geneticData)
        print("cp10")
        wkhtmltopdf_options = {
            'enable-local-file-access': None,
            'javascript-delay': 2000000
        }
        pdf = pdfkit.from_string(reportBodyHtml, False, {'--header-html': pdfTemplateDir + '/processed-header.html',
                                                         '--footer-html': pdfTemplateDir + '/footer.html','enable-local-file-access':None})

        return pdf

    def convertHtmlToPdf(self, geneticModifiedReportData, reportMetaData):
        print("cp5")
        pdfTemplateDir = os.getcwd() + '/app/business_logic/templates'
        genecticReportType = reportMetaData['geneticReportType']
        geneticFileCompanyType = reportMetaData['geneticFileCompanyType']
        geneticReportReferenceNumber = reportMetaData['referenceNumber']
        print("cp6")
        self.saveProcessedHeader(genecticReportType, geneticFileCompanyType, geneticReportReferenceNumber)

        groupedGeneticReportData = ''
        template = ''
        print("cp7")
        if geneticFileCompanyType == "23AndMe" and genecticReportType == "NGX":
            print("cp8")
            template = open(pdfTemplateDir + "/Ngx23AndMeTemplate.html")
            print("cp9")
            groupedGeneticReportData = self.getGrouped23AndMeNgxReportData(geneticModifiedReportData)

        if geneticFileCompanyType == "23AndMe" and genecticReportType == "PGX":
            template = open(pdfTemplateDir + "/Pgx23AndMeTemplate.html")
            groupedGeneticReportData = self.getGrouped23AndMePgxReportData(geneticModifiedReportData)

        if geneticFileCompanyType == "Ancestry" and genecticReportType == "NGX":
            template = open(pdfTemplateDir + "/NgxAncestryTemplate.html")
            groupedGeneticReportData = self.getGroupedAncestryNgxReportData(geneticModifiedReportData)

        if geneticFileCompanyType == "Ancestry" and genecticReportType == "PGX":
            template = open(pdfTemplateDir + "/PgxAncestryTemplate.html")
            groupedGeneticReportData = self.getGroupedAncestryPgxReportData(geneticModifiedReportData)
        print("cp9")
        geneticData = json.loads(groupedGeneticReportData)

        jinjaTemplater = Template(template.read())

        reportBodyHtml = jinjaTemplater.render(reportingData = geneticData)
        print("cp7")
        pdf = pdfkit.from_string(reportBodyHtml, False, {'--header-html': pdfTemplateDir + '/processed-header.html',
                                                         '--footer-html': pdfTemplateDir + '/footer.html'})

        return pdf

    def getGrouped23AndMeNgxReportData(self, geneticModifiedReportData):
        print("cp10")
        p1 = pd.DataFrame(geneticModifiedReportData, columns=['snpRsid', 'geneAndVarient', 'category', 'pathway', 'variantMeaning', 'riskAllele', 'genoType'])
        print("cp11")
        genectic23AndMeNgxReportData = (p1.groupby(['category'], as_index=True).apply(lambda x: x[['snpRsid', 'geneAndVarient', 'pathway', 'variantMeaning', 'riskAllele', 'genoType']].to_dict('r')).reset_index().rename(columns={0: 'value'}).to_json(orient='records'))
        print("cp12")
        return genectic23AndMeNgxReportData

    def getGrouped23AndMePgxReportData(self, geneticModifiedReportData):
        p1 = pd.DataFrame(geneticModifiedReportData, columns=['snpRsid', 'snpName', 'category', 'riskAllele', 'genoType'])
        genectic23AndMePgxReportData = (p1.groupby(['category'], as_index=True).apply(
            lambda x: x[['snpRsid', 'snpName', 'riskAllele', 'genoType']]
                .to_dict('r')).reset_index()
                                        .rename(columns={0: 'value'})
                                        .to_json(orient='records'))
        return genectic23AndMePgxReportData

    def getGroupedAncestryNgxReportData(self, geneticModifiedReportData):
        p1 = pd.DataFrame(geneticModifiedReportData, columns=['snpRsid', 'snpName', 'category', 'riskAllele', 'genoType'])
        genecticAncestryNgxReportData = (p1.groupby(['category'], as_index=True).apply(
            lambda x: x[['snpRsid', 'snpName', 'riskAllele', 'genoType']].to_dict('r')).reset_index()
                                         .rename(columns={0: 'value'}).to_json(orient='records'))
        return genecticAncestryNgxReportData

    def getGroupedAncestryPgxReportData(self, geneticModifiedReportData):
        p1 = pd.DataFrame(geneticModifiedReportData, columns=['snpRsid', 'snpName', 'category', 'riskAllele', 'genoType'])
        genecticAncestryPgxReportData = (p1.groupby(['category'], as_index=True).apply(
            lambda x: x[['snpRsid', 'snpName', 'riskAllele', 'genoType']]
                .to_dict('r')).reset_index()
                                         .rename(columns={0: 'value'})
                                         .to_json(orient='records'))
        return genecticAncestryPgxReportData

    def saveProcessedHeader(self, reportType, companyType, reportReferenceNumber):
        pdfTemplateDir = os.getcwd() + '/app/business_logic/templates'
        with open(pdfTemplateDir + "/header.html", "rt") as fin:
            with open(pdfTemplateDir + "/processed-header.html", "wt") as fout:
                for line in fin:
                    line = line.replace('companyType', companyType)
                    line = line.replace('reportType', reportType)
                    line = line.replace('reportReferenceNumber', reportReferenceNumber)
                    fout.write(line)

    def saveProcessedHeader3(self, reportType, companyType, reportReferenceNumber):
        pdfTemplateDir = os.getcwd() + '/app/business_logic/template3'
        with open(pdfTemplateDir + "/header.html", "rt") as fin:
            with open(pdfTemplateDir + "/processed-header.html", "wt") as fout:
                for line in fin:
                    line = line.replace('companyType', companyType)
                    line = line.replace('reportType', reportType)
                    line = line.replace('reportReferenceNumber', reportReferenceNumber)
                    fout.write(line)
