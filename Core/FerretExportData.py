from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QMessageBox, QGroupBox, QPushButton, QApplication
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from FileDialogButton import SaveFileButton
from FileDialogButton import FileFilters
from PDFWriter import PDF
import os
import pathlib
import sys
import csv
import logging
logger = logging.getLogger(__name__)

pathToFerretFolder = pathlib.Path(__file__).parent.parent.absolute()
IMAGE_NAME = 'model.png'
DEFAULT_REPORT_FILE_PATH_NAME = 'report.pdf'
DEFAULT_PLOT_DATA_FILE_PATH_NAME = 'plot.csv'
FERRET_LOGO = os.path.join(pathToFerretFolder, 'images\FERRET_LOGO.png')
REPORT_TITLE = 'FERRET - Model-fitting of dynamic contrast-enhanced MRI'


class FerretExportData(QWidget):
    """
    This class creates a group of buttons contained in a group box 
    as a custom widget that are used for the export of Ferret data.

    The buttons are:
    1. 'Save plot data to CSV file' - Saves all the current graph plots to a CSV file,
            so that the current plots can be reproduced in an external application.
    2. 'Save plot data to DICOM' - Saves the plot data as a DICOM series. Currently
            this is not working.
    3. 'Save Report in PDF Format' - Creates a PDF report containing a graphic of the
            current plot and output from the model.
    """

    #signal to Ferret to prepare data for export
    sigPrepareForDataExport = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.fileFilter = FileFilters()
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.setUpExportGroupBox()
        self._longModelName = None
        self._modelName = None
        self._dataFileName = None
        self._parameterDict ={}
        self._signalData = None
        self._listModelValues = []   #list of values predicted by the model
        self._listModelVariableValues = [] #list of values of each model variable
        
    def setListModelVariableValues(self, listModelVariableValues):
        self._listModelVariableValues = listModelVariableValues

    def setListModelValues(self, listModelValues):
        self._listModelValues = listModelValues

    def setSignalData(self, signalData):
        self._signalData = signalData

    def setParameterDictionary(self, dictParams):
        self._parameterDict = dictParams

    def setDataFileName(self, dataFileName):
        self._dataFileName = dataFileName

    def setLongModelName(self, name):
        self._longModelName = name

    def setModelName(self, name):
        self._modelName = name


    def setUpExportGroupBox(self):
        """
        This function creates three push buttons contained within 
        the Export Data group box.
        """
        self.groupBoxExport = QGroupBox('Export Data')
        # The group box is hidden until a model is selected.
        self.groupBoxExport.setVisible(False)
        self.groupBoxExport.setAlignment(QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(self.groupBoxExport)
        self.exportHorizontalLayout = QHBoxLayout()
        self.exportHorizontalLayout.setSpacing(0)
        self.groupBoxExport.setLayout(self.exportHorizontalLayout)
        self.setUpSaveCSVButton()
        self.setUpButtonSaveDICOM()
        self.setUpSaveReportButton()


    def setExportGroupBoxVisible(self, bool):
        self.groupBoxExport.setVisible(bool)
        self.btnSaveCSV.setVisible(bool)
        self.btnSaveReport.setVisible(bool)
        self.btnSaveDICOM.setVisible(bool)


    def setUpSaveCSVButton(self):
        """
        Sets up the button for saving plot data to a CSV file.
        """
        self.btnSaveCSV = SaveFileButton(buttonLabel='Save plot data to CSV file', 
                 showButton=False,
                 toolTip='Save the data plotted on the graph to a CSV file',
                 shortCut="Ctrl+S",
                 xMaxSize = 400,
                 yMaxSize = 45,
                 defaultDialogCaption='Enter CSV file name',
                 defaultDirectory=DEFAULT_PLOT_DATA_FILE_PATH_NAME,
                 filesFilter = self.fileFilter.csvFiles)
        self.exportHorizontalLayout.addWidget(self.btnSaveCSV)
        self.btnSaveCSV.sigFileSaved.connect(lambda filePath: self.saveCSVFile(filePath))


    def setUpSaveReportButton(self):
        """
        Sets up the button for creating a PDF report.
        """
        self.btnSaveReport = SaveFileButton(buttonLabel='Save Report in PDF Format',
                 showButton=False,
                 toolTip='Insert an image of the graph opposite and associated data in a PDF file',
                 shortCut="Ctrl+R",
                 xMaxSize = 400,
                 yMaxSize = 45,
                 defaultDialogCaption='Enter PDF file name',
                 defaultDirectory=DEFAULT_REPORT_FILE_PATH_NAME,
                 filesFilter = self.fileFilter.pdfFiles )
        self.btnSaveReport.sigFileSaved.connect(lambda  reportFileName: self.createPDFReport(reportFileName))
        self.exportHorizontalLayout.addWidget(self.btnSaveReport)


    def setUpButtonSaveDICOM(self):
        """
        Sets up the button for saving plot data to a DICOM series.
        Currently this button has no functionality attached to it.
        """
        self.btnSaveDICOM = QPushButton('Save plot data to DICOM')
        self.btnSaveDICOM.hide()
        self.btnSaveDICOM.setMaximumSize(QtCore.QSize(350,45))
        self.btnSaveDICOM.setToolTip('Save the data plotted TO DICOM')
        self.exportHorizontalLayout.addWidget(self.btnSaveDICOM)


    def saveCSVFile(self, CSVFileName):
        """Saves in CSV format the data in the plot on the GUI """ 
        try:
            logger.info('Function ExportFerretData.saveCSVFile called.')
            self.sigPrepareForDataExport.emit()
            #Get model name
            modelName = self._modelName
            modelName.replace(" ", "-")

           # Check that the user did not press Cancel on the
           # create file dialog
            if CSVFileName:
                logger.info('Function ExportFerretData.saveCSVFile - csv file name = ' + 
                            CSVFileName)
                # If CSVFileName already exists, delete it
                if os.path.exists(CSVFileName):
                    os.remove(CSVFileName)

                with open(CSVFileName, 'w',  newline='') as csvfile:
                    writeCSV = csv.writer(csvfile,  delimiter=',')
                    #write header row
                    headerRow =['Time (min)']
                    for value in self._listModelVariableValues:
                        headerRow.append(value)
                    headerRow.append(modelName + ' model')
                    writeCSV.writerow(headerRow)

                    # Write rows of data
                    for i, time in enumerate(self._signalData['time']):
                        rowIterator = [time]
                        for value in self._listModelVariableValues:
                            rowIterator.append(self._signalData[value][i])
                        rowIterator.append(self._listModelValues[i])
                        writeCSV.writerow(rowIterator)
                    csvfile.close()
        except csv.Error:
            print('CSV Writer error in function ExportFerretData.saveCSVFile: file %s, line %d: %s' % (CSVFileName, writeCSV.line_num, csv.Error))
            logger.error('CSV Writer error in function ExportFerretData.saveCSVFile: file %s, line %d: %s' % (CSVFileName, writeCSV.line_num, csv.Error))
        except IOError as IOe:
            print ('IOError in function ExportFerretData.saveCSVFile: cannot open file ' + CSVFileName + ' or read its data: ' + str(IOe))
            logger.error ('IOError in function ExportFerretData.saveCSVFile: cannot open file ' + CSVFileName + ' or read its data; ' + str(IOe))
        except RuntimeError as re:
            print('Runtime error in function ExportFerretData.saveCSVFile: ' + str(re))
            logger.error('Runtime error in function ExportFerretData.saveCSVFile: ' + str(re))
        except Exception as e:
            print('Error in function ExportFerretData.saveCSVFile: ' + str(e) + ' at line in CSV file ', writeCSV.line_num)
            logger.error('Error in function ExportFerretData.saveCSVFile: ' + str(e) + ' at line in CSV file ', writeCSV.line_num)


    def createPDFReport(self, reportFileName):
        """Creates and saves a report of model fitting in PDF format. 
        It includes the name of the model, the current values
        of its input parameters and a copy of the current plot.
        
        Input Parameter:
        ****************
            reportFileName - file path and name of the PDF file 
            in which the report will be saved.
            Used during batch processing.

        Return:
        -------
            parameterDict - A dictionary of parameter short name:value pairs
                used during batch processing to create the overall results
                summary, in an Excel spreadsheet, from all the data input files.
        """
        try:
            pdf = PDF(REPORT_TITLE, FERRET_LOGO) 
            if reportFileName:
                # If the user has entered the name of a new file, 
                # then we will have to add the .pdf extension
                # If the user has decided to overwrite an existing file, 
                # then will not have to add the .pdf extension
                name, ext = os.path.splitext(reportFileName)
                if ext != '.pdf':
                    # Need to add .pdf extension to reportFileName
                    reportFileName = reportFileName + '.pdf'
                if os.path.exists(reportFileName):
                    # delete existing copy of PDF called reportFileName
                    os.remove(reportFileName) 

                # Save a png of the concentration/time plot for display 
                # in the PDF report and collect data for inclusion in the
                #report
                self.sigPrepareForDataExport.emit()
                             
                QApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))

                pdf.CreateAndSavePDFReport(reportFileName, self._dataFileName, 
                       self._longModelName, IMAGE_NAME, self._parameterDict)
                
                QApplication.restoreOverrideCursor()

                # Delete image file
                os.remove(IMAGE_NAME)
                logger.info('PDF Report created called ' + reportFileName)
        except Exception as e:
            print('Error in function ExportFerretData createPDFReport: ' + str(e))
            logger.error('Error in function ExportFerretData createPDFReport: ' + str(e))


    
