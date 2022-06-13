from PyQt5.QtWidgets import QVBoxLayout,  QWidget
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import logging
logger = logging.getLogger(__name__)

from InputValidation import InputValidation

class NavigationToolbar(NavigationToolbar):
    """
    Unwanted default buttons in the Navigation Toolbar are removed by creating
    a subclass of the NavigationToolbar class from from 
    matplotlib.backends.backend_qt5agg import NavigationToolbar2QT.
    Only the desired buttons are defined.
    """
    toolitems = [t for t in NavigationToolbar.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]


class LineGraph(QWidget):
    def __init__(self, plotWidth=4, plotHeight=7, 
                 dotsPerInch=300, xLabel='time', 
                 yLabel='signal', title=None,
                 tickLabelSize=2,
                 xyAxisLabelSize=2,
                 titleSize=2,
                 backgroundColour='w'):
        """
        Sets up the graph and its tool bar and places them in a vertical layout,
        which is then added to QWidget.

        If plot width = 4,  plot height = 6 and dots per inch is 75 then
        the plot would be 300 and 450 pixels in size.

        Input arguments.
        ****************
        plotWidth - width of the plot in inches 
        plotHeight - height of the plot in inches 
        dotsPerInch - number of pixels per inch 
        xLabel - string containing the X axis label  
        yLabel - string containing the Y axis label  
        title  - string containing the title of the graph displayed above the graph.
        tickLabelSize - size of the axis ticks.
        xyAxisLabelSize - size of the X & Y axis labels.
        titleSize - size of the title.
        backgroundColour - optional parameter for selecting the plot background colour.
                            default value is 'w' for white
        """
        try:
            InputValidation.validatePositiveNumericVariable(plotWidth, "plotWidth")
            InputValidation.validatePositiveNumericVariable(plotWidth, "plotWidth")
            InputValidation.validatePositiveNumericVariable(plotHeight, "plotHeight")
            InputValidation.validatePositiveNumericVariable(dotsPerInch, "dotsPerInch")
            InputValidation.validatePositiveNumericVariable(tickLabelSize, "tickLabelSize")
            InputValidation.validatePositiveNumericVariable(xyAxisLabelSize, "xyAxisLabelSize")
            InputValidation.validatePositiveNumericVariable(titleSize, "titleSize")
            InputValidation.validateStringVariable(xLabel, "xLabel")
            InputValidation.validateStringVariable(yLabel, "yLabel")
            InputValidation.validateStringVariable(title, "title")
            InputValidation.validateStringVariable(backgroundColour, "title")

            super().__init__()
            self.figure = plt.figure(figsize=(plotWidth, plotHeight), dpi=dotsPerInch)
            self.figure.set_visible(True)
            #Move the plot up to make room for the x axis label
            self.figure.subplots_adjust(bottom=0.2)
            self.figure.tight_layout()
            # this is the Canvas Widget that displays the `figure`
            # it takes the `figure` instance as a parameter 
            # to its __init__ function
            self.canvas = FigureCanvas(self.figure)
            self.backgroundColour = backgroundColour
            self.xLabel = xLabel
            self.yLabel = yLabel
            self.title = title
            self.tickLabelSize = tickLabelSize
            self.xyAxisLabelSize = xyAxisLabelSize
            self.titleSize = titleSize
            self._setUpSubPlot()
            self.plotLayout =  QVBoxLayout()
            self.toolbar = NavigationToolbar(self.canvas, None)
            self.plotLayout.addWidget(self.toolbar)
            self.plotLayout.addWidget(self.canvas)
            self.setLayout(self.plotLayout)
        except Exception as e:
            print('Error creating LineGraph object: ' + str(e)) 
            logger.error('Error creating LineGraph object: ' + str(e))


    def clearPlot(self):
        """
        Removes the existing plots from the graph
        """
        self.figure.clear()
        self._setUpSubPlot()


    def _setUpSubPlot(self):
        """
        This function sets up the grid and the axes of the graph
        """
        try:
            logger.info('function _setUpSubPlot called.')
            
            #Position a sub plot in the graph's grid.
            # "111" means "1x1 grid, first subplot"
            self.subPlot = self.figure.add_subplot(111)
            
            # Set size of the x,y axis tick labels
            self.subPlot.tick_params(axis='both', 
                                   which='major', 
                                   labelsize=self.tickLabelSize)
            self.subPlot.set_facecolor(self.backgroundColour)
            self.subPlot.set_xlabel(self.xLabel, loc='center', 
                                    fontsize=self.xyAxisLabelSize)
            self.subPlot.set_ylabel(self.yLabel, loc='center', 
                                    fontsize=self.xyAxisLabelSize)
            if self.title is not None:
                self.subPlot.set_title(self.title, fontsize=self.titleSize)
            #add a grid to the sub plot
            self.subPlot.grid()
        except Exception as e:
            print('Error in function LineGraph _setUpSubPlot: ' + str(e))
            logger.error('Error in function LineGraph _setUpSubPlot: ' + str(e))


    def _setUpLegendBox(self):
        """
        This function draws the legend box holding the key
        to the MR signal/time curves on the plot.
        """
        try:
            logger.info('function _setUpLegendBox called.')
            # Put a legend to the top right-hand corner of the plot
            self.subPlot.legend(loc='upper right', 
                                bbox_to_anchor=(0.8, 1.0), 
                                labelspacing = 2,
                                fontsize=self.xyAxisLabelSize,
                                ncol=1,
                                handlelength=1.0,
                                handleheight=1.0)
        except Exception as e:
            print('Error in function LineGraph _setUpLegendBox: ' + str(e))
            logger.error('Error in function LineGraph _setUpLegendBox: ' + str(e))


    def plotData(self, xData, yData, lineStyle, labelText):
        """
        Plots a line through the data points on the graph.

        Input Arguments
        ***************
        xData - List of X data points 
        yData - List of Y data points
        lineStyle - String containing the style (solid or dashed) and colour of the plot line
        labelText - String containing the label for this plot displayed in the legend box
        """
        try:
            InputValidation.validateNumpyArrayVariable(xData, "xData")
            InputValidation.validateNumpyArrayVariable(yData, "yData")
            InputValidation.validateStringVariable(lineStyle, "lineStyle")
            InputValidation.validateStringVariable(labelText, "labelText")
            self.subPlot.plot(xData, yData, lineStyle, label=labelText)
            self._setUpLegendBox()
            # Redraw the canvas to show the above line
            self.canvas.draw()
        except Exception as e:
            print('Error in function LineGraph plotData: ' + str(e))
            logger.error('Error in function LineGraph plotData: ' + str(e))


    def savePlotToPDF(self, imageName):
        """
        Saves a copy of the graph as a PDF file to disc.
        """
        self.figure.savefig(fname=imageName, dpi=300)