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
    print("Got call From Client to process genetic files")
    geneticFile = request.FILES['geneticFile']
    requestBody = request.data
    geneticFileCompanyType = requestBody['geneticFileCompanyType']#"23AndMe" #  "Ancestry"
    geneticReportType = requestBody['geneticReportType'] # NGX and PGX
    fs = FileSystemStorage()
    geneticFileDestination = 'genetic_data_files'
    if geneticFileCompanyType == "23AndMe" :
        print("23AndMe")
        geneticFileDestination = 'genetic_data_files/23_and_me'
    elif geneticFileCompanyType == "Ancestry" :
        print("Ancestry")
        geneticFileDestination = 'genetic_data_files/ancestry'
    else :
        print("Param passing issues choose either 23AndMe or Ancestry")
        geneticFileDestination = 'genetic_data_files'
    savedGenecticFileName = fs.save(geneticFileDestination + geneticFile.name, geneticFile)
    genecticFilePath=fs.path(savedGenecticFileName)
    geneDataAnalyzer = GeneticDataAnalyzer()
    geneDataAnalyzer.initMySqlDb()

    #genecticFilePath = fs.path(filename)
    if geneticFileCompanyType == "23AndMe" :
        if geneticReportType == "NGX" :
            print("NGX")
            geneReportData = geneDataAnalyzer.getNgx23AndMeReportData(genecticFilePath)
        elif geneticReportType == "PGX" :
            print("PGX")
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
    print(editedGeneticData)
    reportMetaData = requestBody['reportMetaData']
    print(reportMetaData)
    pdfReport = pdfReportGenerator.convertHtmlToPdf(editedGeneticData, reportMetaData)
    print("cp3")
    response = HttpResponse(pdfReport,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response

@api_view(['POST'])
def generateReport2(request):
    pdfReportGenerator = PdfReportGenerator()
    requestBody = request.data

    editedGeneticData = requestBody['geneticEditedReportData']
    print(editedGeneticData)
    reportMetaData = requestBody['reportMetaData']
    print(reportMetaData)
    pdfReport = pdfReportGenerator.convertHtmlToPdf2(editedGeneticData, reportMetaData)
    print("cp3")
    response = HttpResponse(pdfReport,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response

@api_view(['POST'])
def generateReport3(request):
    pdfReportGenerator = PdfReportGenerator()
    requestBody = request.data

    editedGeneticData = requestBody['geneticEditedReportData']
    print(editedGeneticData)
    reportMetaData = requestBody['reportMetaData']
    print(reportMetaData)
    pdfReport = pdfReportGenerator.convertHtmlToPdf3(editedGeneticData, reportMetaData)
    print("cp3")
    response = HttpResponse(pdfReport,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response


@parser_classes((MultiPartParser, ))
@api_view(['POST'])
def processGeneticFileReport(request):
    print("processGeneticFileReport")
    geneticFile = request.FILES['geneticFile']
    requestBody = request.data
    geneticFileCompanyType = requestBody['geneticFileCompanyType'] #"23AndMe" "Ancestry"
    geneticReportType = requestBody['geneticReportType'] # NGX and PGX
    referenceNumber = requestBody['referenceNumber'] # patient number

    fs = FileSystemStorage()
    geneticFileDestination = 'genetic_data_files'
    if geneticFileCompanyType == "23AndMe" :
        print("Given data is 23AndMe")
        geneticFileDestination = 'genetic_data_files/23_and_me'
    elif geneticFileCompanyType == "Ancestry" :
        print("Given data is Ancestry")
        geneticFileDestination = 'genetic_data_files/ancestry'
    else :
        print("Please pass either 23andme or Ancestry")
        geneticFileDestination = 'genetic_data_files'
    savedGenecticFileName = fs.save(geneticFileDestination + geneticFile.name, geneticFile)
    genecticFilePath = fs.path(savedGenecticFileName)
    geneDataAnalyzer = GeneticDataAnalyzer()
    geneDataAnalyzer.initMySqlDb()
    print("DB initialised Successfully")
    #genecticFilePath = fs.path(filename)
    if geneticFileCompanyType == "23AndMe" :
        if geneticReportType == "NGX" :
            print("Report for NGX")
            geneReportData = geneDataAnalyzer.getNgx23AndMeReportData2(genecticFilePath)
        elif geneticReportType == "PGX" :
            print("Report for PGX")
            geneReportData = geneDataAnalyzer.getPgx23AndMeReportData(genecticFilePath)
        else :
            print("Add New Type")
    elif geneticFileCompanyType == "Ancestry" :
        if geneticReportType == "NGX":
            print("Report for NGX")
            geneReportData = geneDataAnalyzer.getNgxAncestryReportData2(genecticFilePath)
        elif geneticReportType == "PGX":
            print("Report for PGX")
            geneReportData = geneDataAnalyzer.getPgxAncestryReportData(genecticFilePath)
        else:
            print("Add New Type")
    else :
        geneReportData = geneDataAnalyzer.getReportData(genecticFilePath)
    print("geneReportData is")
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
