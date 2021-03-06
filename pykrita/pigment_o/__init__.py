# Imports
from krita import *
from PyQt5 import *
from .pigment_o import *

# Information
__version__ = ' 1.0.0 '
__license__ = ' GPLv3+ LGPLv3+ '
__author__ = ' Ricardo Jeremias '
__email__ = ' jeremy6321478@gmail.com '
__url__ = ' https://github.com/EyeOdin '

# Name the Python Script for the program
DOCKER_ID = "pykrita_pigment_o"

# Register Krita Extension
Krita.instance().addExtension(PigmentOExtension(Krita.instance()))
# Register Krita Docker
Application.addDockWidgetFactory( DockWidgetFactory(DOCKER_ID, DockWidgetFactoryBase.DockRight, PigmentODocker) )
