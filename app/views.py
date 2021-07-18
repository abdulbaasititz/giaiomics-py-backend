from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
import pandas as pd

from .business_logic.gene_data_analyzer import GeneticDataAnalyzer

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .business_logic.patient_report_generator import PdfReportGenerator
import os

def home(request):
    return HttpResponse('hello')

@parser_classes((MultiPartParser, ))
@api_view(['POST'])
def processGeneticFile(request):
    print("cp1")
    geneticFile = request.FILES['geneticFile']
    requestBody = request.data
    geneticFileCompanyType = requestBody['geneticFileCompanyType']#"23AndMe" #  "Ancestry"
    geneticReportType = requestBody['geneticReportType'] # NGX and PGX
    print("cp2")
    fs = FileSystemStorage()
    geneticFileDestination = 'genetic_data_files'
    if geneticFileCompanyType == "23AndMe" :
        geneticFileDestination = 'genetic_data_files/23_and_me'
    elif geneticFileCompanyType == "Ancestry" :
        geneticFileDestination = 'genetic_data_files/ancestry'
    else :
        geneticFileDestination = 'genetic_data_files'
    savedGenecticFileName = fs.save(geneticFileDestination + geneticFile.name, geneticFile)
    genecticFilePath=fs.path(savedGenecticFileName)
    geneDataAnalyzer = GeneticDataAnalyzer()
    geneDataAnalyzer.initMySqlDb()
    print("cp3")
    #genecticFilePath = fs.path(filename)
    if geneticFileCompanyType == "23AndMe" :
        if geneticReportType == "NGX" :
            geneReportData = geneDataAnalyzer.getNgx23AndMeReportData(genecticFilePath)
        elif geneticReportType == "PGX" :
            geneReportData = geneDataAnalyzer.getPgx23AndMeReportData(genecticFilePath)
        else :
            print("Add New Type")
    elif geneticFileCompanyType == "Ancestry" :
        if geneticReportType == "NGX":
            geneReportData = geneDataAnalyzer.getNgxAncestryReportData(genecticFilePath)
        elif geneticReportType == "PGX":
            geneReportData = geneDataAnalyzer.getPgxAncestryReportData(genecticFilePath)
        else:
            print("Add New Type")
    else :
        geneReportData = geneDataAnalyzer.getReportData(genecticFilePath)
    print("cp4")
    return HttpResponse(geneReportData)

@api_view(['POST'])
def generateReport(request):
    pdfReportGenerator = PdfReportGenerator()
    requestBody = request.data

    editedGeneticData = requestBody['geneticEditedReportData']
    print("cp1")
    reportMetaData = requestBody['reportMetaData']
    print("cp2")
    pdfReport = pdfReportGenerator.convertHtmlToPdf(editedGeneticData, reportMetaData)
    print("cp3")
    response = HttpResponse(pdfReport,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response


@parser_classes((MultiPartParser, ))
@api_view(['POST'])
def processGeneticFileReport(request):
    print("cp1")
    geneticFile = request.FILES['geneticFile']
    requestBody = request.data
    geneticFileCompanyType = requestBody['geneticFileCompanyType']#"23AndMe" #  "Ancestry"
    geneticReportType = requestBody['geneticReportType'] # NGX and PGX
    referenceNumber = requestBody['referenceNumber'] # patient number
    print("cp2")
    fs = FileSystemStorage()
    geneticFileDestination = 'genetic_data_files'
    if geneticFileCompanyType == "23AndMe" :
        geneticFileDestination = 'genetic_data_files/23_and_me'
    elif geneticFileCompanyType == "Ancestry" :
        geneticFileDestination = 'genetic_data_files/ancestry'
    else :
        geneticFileDestination = 'genetic_data_files'
    savedGenecticFileName = fs.save(geneticFileDestination + geneticFile.name, geneticFile)
    genecticFilePath=fs.path(savedGenecticFileName)
    geneDataAnalyzer = GeneticDataAnalyzer()
    geneDataAnalyzer.initMySqlDb()
    print("cp3")
    #genecticFilePath = fs.path(filename)
    if geneticFileCompanyType == "23AndMe" :
        if geneticReportType == "NGX" :
            print("cp3")
            geneReportData = geneDataAnalyzer.getNgx23AndMeReportData2(genecticFilePath)
        elif geneticReportType == "PGX" :
            geneReportData = geneDataAnalyzer.getPgx23AndMeReportData(genecticFilePath)
        else :
            print("Add New Type")
    elif geneticFileCompanyType == "Ancestry" :
        if geneticReportType == "NGX":
            geneReportData = geneDataAnalyzer.getNgxAncestryReportData2(genecticFilePath)
        elif geneticReportType == "PGX":
            geneReportData = geneDataAnalyzer.getPgxAncestryReportData(genecticFilePath)
        else:
            print("Add New Type")
    else :
        geneReportData = geneDataAnalyzer.getReportData(genecticFilePath)
    print("cp4")
    pdfReportGenerator = PdfReportGenerator()
    reportMetaData={"geneticReportType":geneticReportType,
                    "geneticFileCompanyType":geneticFileCompanyType,
                    "referenceNumber":referenceNumber}
    print(geneReportData)
    # pdfReport = pdfReportGenerator.convertHtmlToPdf(geneReportData, reportMetaData)
    pdfReport = pdfReportGenerator.convertHtmlToPdf2(geneReportData, reportMetaData)
    response = HttpResponse(pdfReport, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response


def storeDataInLocal(myfile,tempFilePath): 
    fs = FileSystemStorage(location=tempFilePath)
    filename=fs.save(myfile.name, myfile)
    return filename



#https://grokonez.com/django/django-how-to-upload-file-using-modelform-tutorial-mysql
