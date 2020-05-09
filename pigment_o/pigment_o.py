# Import Krita
from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg, uic
import os.path
import threading
from .pigment_o_constants import Constants
from .pigment_o_style import Style
from .pigment_o_channel import Channel_Linear
from .pigment_o_convert import Convert
from .pigment_o_mixer import Mixer_Color, Mixer_Gradient
from .pigment_o_panel import PanelHsv, PanelHsl
from .pigment_o_clicks import Clicks

# Set Window Title Name
DOCKER_NAME = "Pigment.O"
# Timer
check_timer = 1000  # 1000 = 1 SECOND (Zero will Disable checks)
# Color Space Factors
constant1 = Constants().Krita()
factorAAA = constant1[0]
factorRGB = constant1[1]
factorHUE = constant1[2]
factorSVL = constant1[3]
factorCMYK = constant1[4]
constant2 = Constants().HEX()
factorHEXAAA = constant2[0]
factorHEXRGB = constant2[1]
factorHEXHUE = constant2[2]
factorHEXSVL = constant2[3]
factorHEXCMYK = constant2[4]
# UI variables
cmin1 = 8
cmax1 = 15
cmin2 = 5
cmax2 = 10
cmin3 = 19
cmax3 = 34
tipmm = 30
margin = 5
vspacer = 2
unit = 1
null = 0
# Brush Tip Default
size = 40
opacity = 1
flow = 1

# Create Docker
class PigmentODocker(DockWidget):
    """
    Compact Color Selector with various Color Spaces to choose from
    """

    # Initialize the Dicker Window
    def __init__(self):
        super(PigmentODocker, self).__init__()

        # Window Title
        self.setWindowTitle(DOCKER_NAME)

        # Construct
        self.User_Interface()
        self.Setup()
        self.Connect()
        self.Mixers()
        self.Click_Twice()
        self.Threads()
        self.Style_Sheet()

        # Initial Color
        self.Color_Apply([0,0,0])

    def User_Interface(self):
        # Widget
        self.window = QWidget()
        self.layout = uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + '/pigment_o.ui', self.window)
        self.setWidget(self.window)
        # Values Range for the Double SpinBox
        self.layout.aaa_value.setMinimum(0)
        self.layout.aaa_value.setMaximum(factorAAA)
        self.layout.rgb_1_value.setMinimum(0)
        self.layout.rgb_1_value.setMaximum(factorRGB)
        self.layout.rgb_2_value.setMinimum(0)
        self.layout.rgb_2_value.setMaximum(factorRGB)
        self.layout.rgb_3_value.setMinimum(0)
        self.layout.rgb_3_value.setMaximum(factorRGB)
        self.layout.hsv_1_value.setMinimum(0)
        self.layout.hsv_1_value.setMaximum(factorHUE)
        self.layout.hsv_2_value.setMinimum(0)
        self.layout.hsv_2_value.setMaximum(factorSVL)
        self.layout.hsv_3_value.setMinimum(0)
        self.layout.hsv_3_value.setMaximum(factorSVL)
        self.layout.hsl_1_value.setMinimum(0)
        self.layout.hsl_1_value.setMaximum(factorHUE)
        self.layout.hsl_2_value.setMinimum(0)
        self.layout.hsl_2_value.setMaximum(factorSVL)
        self.layout.hsl_3_value.setMinimum(0)
        self.layout.hsl_3_value.setMaximum(factorSVL)
        self.layout.cmyk_1_value.setMinimum(0)
        self.layout.cmyk_1_value.setMaximum(factorCMYK)
        self.layout.cmyk_2_value.setMinimum(0)
        self.layout.cmyk_2_value.setMaximum(factorCMYK)
        self.layout.cmyk_3_value.setMinimum(0)
        self.layout.cmyk_3_value.setMaximum(factorCMYK)
        self.layout.cmyk_4_value.setMinimum(0)
        self.layout.cmyk_4_value.setMaximum(factorCMYK)
    def Setup(self):
        # Modules
        self.style = Style()
        self.convert = Convert()

        # Set Menus Display
        self.layout.aaa.setChecked(False)
        self.Display_AAA()
        self.layout.rgb.setChecked(True)
        self.Display_RGB()
        self.layout.hsv.setChecked(False)
        self.Display_HSV()
        self.layout.hsl.setChecked(False)
        self.Display_HSL()
        self.layout.cmyk.setChecked(False)
        self.Display_CMYK()
        self.layout.tip.setChecked(False)
        self.Display_Cores()
        self.layout.tts.setChecked(False)
        self.Display_TTS()
        # Mixer Selection
        self.Mixer_Shrink()
        mixer = self.layout.mixer_selector.findText("MIX", QtCore.Qt.MatchFixedString)
        self.layout.mixer_selector.setCurrentIndex(mixer)
        # Panel Selection
        panel = self.layout.panel_selector.findText("PANEL", QtCore.Qt.MatchFixedString)
        self.layout.panel_selector.setCurrentIndex(panel)
        self.Display_Panel()

        # Palette
        self.Color_01("CLEAN")
        self.Color_02("CLEAN")
        self.Color_03("CLEAN")
        self.Color_04("CLEAN")
        self.Color_05("CLEAN")
        self.Color_06("CLEAN")
        self.Color_07("CLEAN")
        self.Color_08("CLEAN")
        self.Color_09("CLEAN")
        self.Color_10("CLEAN")

        # Start Timer and Connect Switch
        if check_timer >= 1000:
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.Krita_Update)
            self.timer.start(check_timer)
            # Method ON/OFF switch boot
            self.layout.check.setChecked(True)
            self.Timer()
    def Connect(self):
        # Module Channel
        self.aaa_slider = Channel_Linear(self.layout.aaa_slider)
        self.aaa_slider.Setup("AAA")
        self.rgb_1_slider = Channel_Linear(self.layout.rgb_1_slider)
        self.rgb_2_slider = Channel_Linear(self.layout.rgb_2_slider)
        self.rgb_3_slider = Channel_Linear(self.layout.rgb_3_slider)
        self.rgb_1_slider.Setup("RGB")
        self.rgb_2_slider.Setup("RGB")
        self.rgb_3_slider.Setup("RGB")
        self.hsv_1_slider = Channel_Linear(self.layout.hsv_1_slider)
        self.hsv_2_slider = Channel_Linear(self.layout.hsv_2_slider)
        self.hsv_3_slider = Channel_Linear(self.layout.hsv_3_slider)
        self.hsv_1_slider.Setup("HUE")
        self.hsv_2_slider.Setup("SVL")
        self.hsv_3_slider.Setup("SVL")
        self.hsl_1_slider = Channel_Linear(self.layout.hsl_1_slider)
        self.hsl_2_slider = Channel_Linear(self.layout.hsl_2_slider)
        self.hsl_3_slider = Channel_Linear(self.layout.hsl_3_slider)
        self.hsl_1_slider.Setup("HUE")
        self.hsl_2_slider.Setup("SVL")
        self.hsl_3_slider.Setup("SVL")
        self.cmyk_1_slider = Channel_Linear(self.layout.cmyk_1_slider)
        self.cmyk_2_slider = Channel_Linear(self.layout.cmyk_2_slider)
        self.cmyk_3_slider = Channel_Linear(self.layout.cmyk_3_slider)
        self.cmyk_4_slider = Channel_Linear(self.layout.cmyk_4_slider)
        self.cmyk_1_slider.Setup("CMYK")
        self.cmyk_2_slider.Setup("CMYK")
        self.cmyk_3_slider.Setup("CMYK")
        self.cmyk_4_slider.Setup("CMYK")

        # Connect Channel Alpha
        self.layout.aaa_label.clicked.connect(lambda: self.Pigment_AAA("50", 0))
        self.layout.aaa_minus.clicked.connect(lambda: self.Pigment_AAA("M1", 1))
        self.layout.aaa_plus.clicked.connect(lambda: self.Pigment_AAA("P1", 1))
        self.aaa_slider.SIGNAL_VALUE.connect(self.layout.aaa_value.setValue)
        self.layout.aaa_value.valueChanged.connect(lambda: self.aaa_slider.Update(self.layout.aaa_value.value(), factorAAA, self.layout.aaa_slider.width()))

        # Connect Channel Red
        self.layout.rgb_1_label.clicked.connect(lambda: self.Pigment_RGB_1("50", 0))
        self.layout.rgb_1_minus.clicked.connect(lambda: self.Pigment_RGB_1("M1", 1))
        self.layout.rgb_1_plus.clicked.connect(lambda: self.Pigment_RGB_1("P1", 1))
        self.rgb_1_slider.SIGNAL_VALUE.connect(self.layout.rgb_1_value.setValue)
        self.layout.rgb_1_value.valueChanged.connect(lambda: self.rgb_1_slider.Update(self.layout.rgb_1_value.value(), factorRGB, self.layout.rgb_1_slider.width()))
        # Connect Channel Green
        self.layout.rgb_2_label.clicked.connect(lambda: self.Pigment_RGB_2("50", 0))
        self.layout.rgb_2_minus.clicked.connect(lambda: self.Pigment_RGB_2("M1", 1))
        self.layout.rgb_2_plus.clicked.connect(lambda: self.Pigment_RGB_2("P1", 1))
        self.rgb_2_slider.SIGNAL_VALUE.connect(self.layout.rgb_2_value.setValue)
        self.layout.rgb_2_value.valueChanged.connect(lambda: self.rgb_2_slider.Update(self.layout.rgb_2_value.value(), factorRGB, self.layout.rgb_2_slider.width()))
        # Connect Channel Blue
        self.layout.rgb_3_label.clicked.connect(lambda: self.Pigment_RGB_3("50", 0))
        self.layout.rgb_3_minus.clicked.connect(lambda: self.Pigment_RGB_3("M1", 1))
        self.layout.rgb_3_plus.clicked.connect(lambda: self.Pigment_RGB_3("P1", 1))
        self.rgb_3_slider.SIGNAL_VALUE.connect(self.layout.rgb_3_value.setValue)
        self.layout.rgb_3_value.valueChanged.connect(lambda: self.rgb_3_slider.Update(self.layout.rgb_3_value.value(), factorRGB, self.layout.rgb_3_slider.width()))

        # Connect Channel Hue
        self.layout.hsv_1_label.clicked.connect(lambda: self.Pigment_HSV_1("50", 0))
        self.layout.hsv_1_minus.clicked.connect(lambda: self.Pigment_HSV_1("M1", 1))
        self.layout.hsv_1_plus.clicked.connect(lambda: self.Pigment_HSV_1("P1", 1))
        self.hsv_1_slider.SIGNAL_VALUE.connect(self.layout.hsv_1_value.setValue)
        self.layout.hsv_1_value.valueChanged.connect(lambda: self.hsv_1_slider.Update(self.layout.hsv_1_value.value(), factorHUE, self.layout.hsv_1_slider.width()))
        # Connect Channel Saturation
        self.layout.hsv_2_label.clicked.connect(lambda: self.Pigment_HSV_2("50", 0))
        self.layout.hsv_2_minus.clicked.connect(lambda: self.Pigment_HSV_2("M1", 1))
        self.layout.hsv_2_plus.clicked.connect(lambda: self.Pigment_HSV_2("P1", 1))
        self.hsv_2_slider.SIGNAL_VALUE.connect(self.layout.hsv_2_value.setValue)
        self.layout.hsv_2_value.valueChanged.connect(lambda: self.hsv_2_slider.Update(self.layout.hsv_2_value.value(), factorSVL, self.layout.hsv_2_slider.width()))
        # Connect Channel Value
        self.layout.hsv_3_label.clicked.connect(lambda: self.Pigment_HSV_3("50", 0))
        self.layout.hsv_3_minus.clicked.connect(lambda: self.Pigment_HSV_3("M1", 1))
        self.layout.hsv_3_plus.clicked.connect(lambda: self.Pigment_HSV_3("P1", 1))
        self.hsv_3_slider.SIGNAL_VALUE.connect(self.layout.hsv_3_value.setValue)
        self.layout.hsv_3_value.valueChanged.connect(lambda: self.hsv_3_slider.Update(self.layout.hsv_3_value.value(), factorSVL, self.layout.hsv_3_slider.width()))

        # Connect Channel Hue
        self.layout.hsl_1_label.clicked.connect(lambda: self.Pigment_HSL_1("50", 0))
        self.layout.hsl_1_minus.clicked.connect(lambda: self.Pigment_HSL_1("M1", 1))
        self.layout.hsl_1_plus.clicked.connect(lambda: self.Pigment_HSL_1("P1", 1))
        self.hsl_1_slider.SIGNAL_VALUE.connect(self.layout.hsl_1_value.setValue)
        self.layout.hsl_1_value.valueChanged.connect(lambda: self.hsl_1_slider.Update(self.layout.hsl_1_value.value(), factorHUE, self.layout.hsl_1_slider.width()))
        # Connect Channel Saturation
        self.layout.hsl_2_label.clicked.connect(lambda: self.Pigment_HSL_2("50", 0))
        self.layout.hsl_2_minus.clicked.connect(lambda: self.Pigment_HSL_2("M1", 1))
        self.layout.hsl_2_plus.clicked.connect(lambda: self.Pigment_HSL_2("P1", 1))
        self.hsl_2_slider.SIGNAL_VALUE.connect(self.layout.hsl_2_value.setValue)
        self.layout.hsl_2_value.valueChanged.connect(lambda: self.hsl_2_slider.Update(self.layout.hsl_2_value.value(), factorSVL, self.layout.hsl_2_slider.width()))
        # Connect Channel Lightness
        self.layout.hsl_3_label.clicked.connect(lambda: self.Pigment_HSL_3("50", 0))
        self.layout.hsl_3_minus.clicked.connect(lambda: self.Pigment_HSL_3("M1", 1))
        self.layout.hsl_3_plus.clicked.connect(lambda: self.Pigment_HSL_3("P1", 1))
        self.hsl_3_slider.SIGNAL_VALUE.connect(self.layout.hsl_3_value.setValue)
        self.layout.hsl_3_value.valueChanged.connect(lambda: self.hsl_3_slider.Update(self.layout.hsl_3_value.value(), factorSVL, self.layout.hsl_3_slider.width()))

        # Connect Channel Cyan
        self.layout.cmyk_1_label.clicked.connect(lambda: self.Pigment_CMYK_1("50", 0))
        self.layout.cmyk_1_minus.clicked.connect(lambda: self.Pigment_CMYK_1("M1", 1))
        self.layout.cmyk_1_plus.clicked.connect(lambda: self.Pigment_CMYK_1("P1", 1))
        self.cmyk_1_slider.SIGNAL_VALUE.connect(self.layout.cmyk_1_value.setValue)
        self.layout.cmyk_1_value.valueChanged.connect(lambda: self.cmyk_1_slider.Update(self.layout.cmyk_1_value.value(), factorCMYK, self.layout.cmyk_1_slider.width()))
        # Connect Channel Magenta
        self.layout.cmyk_2_label.clicked.connect(lambda: self.Pigment_CMYK_2("50", 0))
        self.layout.cmyk_2_minus.clicked.connect(lambda: self.Pigment_CMYK_2("M1", 1))
        self.layout.cmyk_2_plus.clicked.connect(lambda: self.Pigment_CMYK_2("P1", 1))
        self.cmyk_2_slider.SIGNAL_VALUE.connect(self.layout.cmyk_2_value.setValue)
        self.layout.cmyk_2_value.valueChanged.connect(lambda: self.cmyk_2_slider.Update(self.layout.cmyk_2_value.value(), factorCMYK, self.layout.cmyk_2_slider.width()))
        # Connect Channel Yellow
        self.layout.cmyk_3_label.clicked.connect(lambda: self.Pigment_CMYK_3("50", 0))
        self.layout.cmyk_3_minus.clicked.connect(lambda: self.Pigment_CMYK_3("M1", 1))
        self.layout.cmyk_3_plus.clicked.connect(lambda: self.Pigment_CMYK_3("P1", 1))
        self.cmyk_3_slider.SIGNAL_VALUE.connect(self.layout.cmyk_3_value.setValue)
        self.layout.cmyk_3_value.valueChanged.connect(lambda: self.cmyk_3_slider.Update(self.layout.cmyk_3_value.value(), factorCMYK, self.layout.cmyk_3_slider.width()))
        # Connect Channel Key
        self.layout.cmyk_4_label.clicked.connect(lambda: self.Pigment_CMYK_4("50", 0))
        self.layout.cmyk_4_minus.clicked.connect(lambda: self.Pigment_CMYK_4("M1", 1))
        self.layout.cmyk_4_plus.clicked.connect(lambda: self.Pigment_CMYK_4("P1", 1))
        self.cmyk_4_slider.SIGNAL_VALUE.connect(self.layout.cmyk_4_value.setValue)
        self.layout.cmyk_4_value.valueChanged.connect(lambda: self.cmyk_4_slider.Update(self.layout.cmyk_4_value.value(), factorCMYK, self.layout.cmyk_4_slider.width()))

        # Active Color
        self.layout.aaa_value.valueChanged.connect(lambda: self.Pigment_Color("AAA"))
        self.layout.rgb_1_value.valueChanged.connect(lambda: self.Pigment_Color("RGB"))
        self.layout.rgb_2_value.valueChanged.connect(lambda: self.Pigment_Color("RGB"))
        self.layout.rgb_3_value.valueChanged.connect(lambda: self.Pigment_Color("RGB"))
        self.layout.hsv_1_value.valueChanged.connect(lambda: self.Pigment_Color("HSV"))
        self.layout.hsv_2_value.valueChanged.connect(lambda: self.Pigment_Color("HSV"))
        self.layout.hsv_3_value.valueChanged.connect(lambda: self.Pigment_Color("HSV"))
        self.layout.hsl_1_value.valueChanged.connect(lambda: self.Pigment_Color("HSL"))
        self.layout.hsl_2_value.valueChanged.connect(lambda: self.Pigment_Color("HSL"))
        self.layout.hsl_3_value.valueChanged.connect(lambda: self.Pigment_Color("HSL"))
        self.layout.cmyk_1_value.valueChanged.connect(lambda: self.Pigment_Color("CMYK"))
        self.layout.cmyk_2_value.valueChanged.connect(lambda: self.Pigment_Color("CMYK"))
        self.layout.cmyk_3_value.valueChanged.connect(lambda: self.Pigment_Color("CMYK"))
        self.layout.cmyk_4_value.valueChanged.connect(lambda: self.Pigment_Color("CMYK"))

        # Previous Selected Color Values
        self.layout.aaa_value.editingFinished.connect(lambda: self.Pigment_Display_Release(""))
        self.layout.rgb_1_value.editingFinished.connect(lambda: self.Pigment_Display_Release(""))
        self.layout.rgb_2_value.editingFinished.connect(lambda: self.Pigment_Display_Release(""))
        self.layout.rgb_3_value.editingFinished.connect(lambda: self.Pigment_Display_Release(""))
        self.layout.hsv_1_value.editingFinished.connect(lambda: self.Pigment_Display_Release(""))
        self.layout.hsv_2_value.editingFinished.connect(lambda: self.Pigment_Display_Release(""))
        self.layout.hsv_3_value.editingFinished.connect(lambda: self.Pigment_Display_Release(""))
        self.layout.hsl_1_value.editingFinished.connect(lambda: self.Pigment_Display_Release(""))
        self.layout.hsl_2_value.editingFinished.connect(lambda: self.Pigment_Display_Release(""))
        self.layout.hsl_3_value.editingFinished.connect(lambda: self.Pigment_Display_Release(""))
        self.layout.cmyk_1_value.editingFinished.connect(lambda: self.Pigment_Display_Release(""))
        self.layout.cmyk_2_value.editingFinished.connect(lambda: self.Pigment_Display_Release(""))
        self.layout.cmyk_3_value.editingFinished.connect(lambda: self.Pigment_Display_Release(""))
        self.layout.cmyk_4_value.editingFinished.connect(lambda: self.Pigment_Display_Release(""))

        # Hex Input
        self.layout.hex_string.returnPressed.connect(lambda: self.HEX_Code(self.layout.hex_string.text()))

        # UI Display Options
        self.layout.aaa.toggled.connect(self.Display_AAA)
        self.layout.rgb.toggled.connect(self.Display_RGB)
        self.layout.hsv.toggled.connect(self.Display_HSV)
        self.layout.hsl.toggled.connect(self.Display_HSL)
        self.layout.cmyk.toggled.connect(self.Display_CMYK)
        self.layout.check.toggled.connect(self.Timer)
        self.layout.tip.toggled.connect(self.Display_Cores)
        self.layout.tts.toggled.connect(self.Display_TTS)
        self.layout.mixer_selector.currentTextChanged.connect(self.Display_Mixer)
        self.layout.panel_selector.currentTextChanged.connect(self.Display_Panel)

        # Module Panel HSV
        self.panel_hsv = PanelHsv(self.layout.panel_hsv_fg)
        self.panel_hsv.SIGNAL_HSV_NEW.connect(self.Signal_HSV)

        # Module Panel HSV
        self.panel_hsl = PanelHsl(self.layout.panel_hsl_fg)
        self.panel_hsl.SIGNAL_HSL_NEW.connect(self.Signal_HSL)

        # Panel Release Input Update
        self.panel_hsv.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_hsl.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
    def Mixers(self):
        # Module Mixer Colors
        self.mixer_neutral = Mixer_Color(self.layout.neutral)
        self.mixer_rgb_l1 = Mixer_Color(self.layout.rgb_l1)
        self.mixer_rgb_l2 = Mixer_Color(self.layout.rgb_l2)
        self.mixer_rgb_l3 = Mixer_Color(self.layout.rgb_l3)
        self.mixer_rgb_r1 = Mixer_Color(self.layout.rgb_r1)
        self.mixer_rgb_r2 = Mixer_Color(self.layout.rgb_r2)
        self.mixer_rgb_r3 = Mixer_Color(self.layout.rgb_r3)
        self.mixer_hsv_l1 = Mixer_Color(self.layout.hsv_l1)
        self.mixer_hsv_l2 = Mixer_Color(self.layout.hsv_l2)
        self.mixer_hsv_l3 = Mixer_Color(self.layout.hsv_l3)
        self.mixer_hsv_r1 = Mixer_Color(self.layout.hsv_r1)
        self.mixer_hsv_r2 = Mixer_Color(self.layout.hsv_r2)
        self.mixer_hsv_r3 = Mixer_Color(self.layout.hsv_r3)
        self.mixer_hsl_l1 = Mixer_Color(self.layout.hsl_l1)
        self.mixer_hsl_l2 = Mixer_Color(self.layout.hsl_l2)
        self.mixer_hsl_l3 = Mixer_Color(self.layout.hsl_l3)
        self.mixer_hsl_r1 = Mixer_Color(self.layout.hsl_r1)
        self.mixer_hsl_r2 = Mixer_Color(self.layout.hsl_r2)
        self.mixer_hsl_r3 = Mixer_Color(self.layout.hsl_r3)
        self.mixer_cmyk_l1 = Mixer_Color(self.layout.cmyk_l1)
        self.mixer_cmyk_l2 = Mixer_Color(self.layout.cmyk_l2)
        self.mixer_cmyk_l3 = Mixer_Color(self.layout.cmyk_l3)
        self.mixer_cmyk_r1 = Mixer_Color(self.layout.cmyk_r1)
        self.mixer_cmyk_r2 = Mixer_Color(self.layout.cmyk_r2)
        self.mixer_cmyk_r3 = Mixer_Color(self.layout.cmyk_r3)
        # Module Mixer Gradients
        self.mixer_tint = Mixer_Gradient(self.layout.tint)
        self.mixer_tone = Mixer_Gradient(self.layout.tone)
        self.mixer_shade = Mixer_Gradient(self.layout.shade)
        self.mixer_rgb_g1 = Mixer_Gradient(self.layout.rgb_g1)
        self.mixer_rgb_g2 = Mixer_Gradient(self.layout.rgb_g2)
        self.mixer_rgb_g3 = Mixer_Gradient(self.layout.rgb_g3)
        self.mixer_hsv_g1 = Mixer_Gradient(self.layout.hsv_g1)
        self.mixer_hsv_g2 = Mixer_Gradient(self.layout.hsv_g2)
        self.mixer_hsv_g3 = Mixer_Gradient(self.layout.hsv_g3)
        self.mixer_hsl_g1 = Mixer_Gradient(self.layout.hsl_g1)
        self.mixer_hsl_g2 = Mixer_Gradient(self.layout.hsl_g2)
        self.mixer_hsl_g3 = Mixer_Gradient(self.layout.hsl_g3)
        self.mixer_cmyk_g1 = Mixer_Gradient(self.layout.cmyk_g1)
        self.mixer_cmyk_g2 = Mixer_Gradient(self.layout.cmyk_g2)
        self.mixer_cmyk_g3 = Mixer_Gradient(self.layout.cmyk_g3)
        # Mixer Color Connect
        self.mixer_neutral.SIGNAL_MIXER_COLOR.connect(self.Mixer_Neutral)
        self.mixer_rgb_l1.SIGNAL_MIXER_COLOR.connect(self.Mixer_RGB_L1)
        self.mixer_rgb_l2.SIGNAL_MIXER_COLOR.connect(self.Mixer_RGB_L2)
        self.mixer_rgb_l3.SIGNAL_MIXER_COLOR.connect(self.Mixer_RGB_L3)
        self.mixer_rgb_r1.SIGNAL_MIXER_COLOR.connect(self.Mixer_RGB_R1)
        self.mixer_rgb_r2.SIGNAL_MIXER_COLOR.connect(self.Mixer_RGB_R2)
        self.mixer_rgb_r3.SIGNAL_MIXER_COLOR.connect(self.Mixer_RGB_R3)
        self.mixer_hsv_l1.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSV_L1)
        self.mixer_hsv_l2.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSV_L2)
        self.mixer_hsv_l3.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSV_L3)
        self.mixer_hsv_r1.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSV_R1)
        self.mixer_hsv_r2.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSV_R2)
        self.mixer_hsv_r3.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSV_R3)
        self.mixer_hsl_l1.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSL_L1)
        self.mixer_hsl_l2.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSL_L2)
        self.mixer_hsl_l3.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSL_L3)
        self.mixer_hsl_r1.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSL_R1)
        self.mixer_hsl_r2.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSL_R2)
        self.mixer_hsl_r3.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSL_R3)
        self.mixer_cmyk_l1.SIGNAL_MIXER_COLOR.connect(self.Mixer_CMYK_L1)
        self.mixer_cmyk_l2.SIGNAL_MIXER_COLOR.connect(self.Mixer_CMYK_L2)
        self.mixer_cmyk_l3.SIGNAL_MIXER_COLOR.connect(self.Mixer_CMYK_L3)
        self.mixer_cmyk_r1.SIGNAL_MIXER_COLOR.connect(self.Mixer_CMYK_R1)
        self.mixer_cmyk_r2.SIGNAL_MIXER_COLOR.connect(self.Mixer_CMYK_R2)
        self.mixer_cmyk_r3.SIGNAL_MIXER_COLOR.connect(self.Mixer_CMYK_R3)
        # Mixer Gradient Connect
        self.mixer_tint.SIGNAL_MIXER_GRADIENT.connect(self.Mixer_Tint)
        self.mixer_tone.SIGNAL_MIXER_GRADIENT.connect(self.Mixer_Tone)
        self.mixer_shade.SIGNAL_MIXER_GRADIENT.connect(self.Mixer_Shade)
        self.mixer_rgb_g1.SIGNAL_MIXER_GRADIENT.connect(self.Mixer_RGB_G1)
        self.mixer_rgb_g2.SIGNAL_MIXER_GRADIENT.connect(self.Mixer_RGB_G2)
        self.mixer_rgb_g3.SIGNAL_MIXER_GRADIENT.connect(self.Mixer_RGB_G3)
        self.mixer_hsv_g1.SIGNAL_MIXER_GRADIENT.connect(self.Mixer_HSV_G1)
        self.mixer_hsv_g2.SIGNAL_MIXER_GRADIENT.connect(self.Mixer_HSV_G2)
        self.mixer_hsv_g3.SIGNAL_MIXER_GRADIENT.connect(self.Mixer_HSV_G3)
        self.mixer_hsl_g1.SIGNAL_MIXER_GRADIENT.connect(self.Mixer_HSL_G1)
        self.mixer_hsl_g2.SIGNAL_MIXER_GRADIENT.connect(self.Mixer_HSL_G2)
        self.mixer_hsl_g3.SIGNAL_MIXER_GRADIENT.connect(self.Mixer_HSL_G3)
        self.mixer_cmyk_g1.SIGNAL_MIXER_GRADIENT.connect(self.Mixer_CMYK_G1)
        self.mixer_cmyk_g2.SIGNAL_MIXER_GRADIENT.connect(self.Mixer_CMYK_G2)
        self.mixer_cmyk_g3.SIGNAL_MIXER_GRADIENT.connect(self.Mixer_CMYK_G3)

        # Inicial Mixer Color Values
        self.color_neutral = self.Neutral_Colors()
        self.color_white = [1*factorAAA, 1*factorRGB,1*factorRGB,1*factorRGB, 0,0,0,0*factorCMYK]
        self.color_grey = [0.5*factorAAA, 0.5*factorRGB,0.5*factorRGB,0.5*factorRGB, 0,0,0,0.5*factorCMYK]
        self.color_black = [0*factorAAA, 0*factorRGB,0*factorRGB,0*factorRGB, 0,0,0,1*factorCMYK]
        self.color_rgb_l1 = self.Current_Colors()
        self.color_rgb_l2 = self.Current_Colors()
        self.color_rgb_l3 = self.Current_Colors()
        self.color_rgb_r1 = self.Current_Colors()
        self.color_rgb_r2 = self.Current_Colors()
        self.color_rgb_r3 = self.Current_Colors()
        self.color_hsv_l1 = self.Current_Colors()
        self.color_hsv_l2 = self.Current_Colors()
        self.color_hsv_l3 = self.Current_Colors()
        self.color_hsv_r1 = self.Current_Colors()
        self.color_hsv_r2 = self.Current_Colors()
        self.color_hsv_r3 = self.Current_Colors()
        self.color_hsl_l1 = self.Current_Colors()
        self.color_hsl_l2 = self.Current_Colors()
        self.color_hsl_l3 = self.Current_Colors()
        self.color_hsl_r1 = self.Current_Colors()
        self.color_hsl_r2 = self.Current_Colors()
        self.color_hsl_r3 = self.Current_Colors()
        self.color_cmyk_l1 = self.Current_Colors()
        self.color_cmyk_l2 = self.Current_Colors()
        self.color_cmyk_l3 = self.Current_Colors()
        self.color_cmyk_r1 = self.Current_Colors()
        self.color_cmyk_r2 = self.Current_Colors()
        self.color_cmyk_r3 = self.Current_Colors()
        # Percentage Values to Zero
        self.percentage_tint = 0
        self.percentage_tone = 0
        self.percentage_shade = 0
        self.percentage_rgb_g1 = 0
        self.percentage_rgb_g2 = 0
        self.percentage_rgb_g3 = 0
        self.percentage_hsv_g1 = 0
        self.percentage_hsv_g2 = 0
        self.percentage_hsv_g3 = 0
        self.percentage_hsl_g1 = 0
        self.percentage_hsl_g2 = 0
        self.percentage_hsl_g3 = 0
        self.percentage_cmyk_g1 = 0
        self.percentage_cmyk_g2 = 0
        self.percentage_cmyk_g3 = 0

        # Previous Selected Color Sliders
        self.aaa_slider.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.rgb_1_slider.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.rgb_2_slider.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.rgb_3_slider.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.hsv_1_slider.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.hsv_2_slider.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.hsv_3_slider.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.hsl_1_slider.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.hsl_2_slider.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.hsl_3_slider.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.cmyk_1_slider.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.cmyk_2_slider.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.cmyk_3_slider.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.cmyk_4_slider.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        # Previous Selected Mixer Sliders
        self.mixer_tint.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_tone.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_shade.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_rgb_g1.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_rgb_g2.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_rgb_g3.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_hsv_g1.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_hsv_g2.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_hsv_g3.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_hsl_g1.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_hsl_g2.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_hsl_g3.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g1.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g2.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g3.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g3.SIGNAL_RELEASE.connect(self.Pigment_Display_Release)
    def Click_Twice(self):
        # Brush Reset
        self.tip_00 = Clicks(self.layout.tip_00)
        self.tip_00.SIGNAL_CLICKS.connect(self.Brush_Lock)
        self.tip_00.Setup(size, opacity, flow)
        # Palette Colors
        self.palette_cor_01 = Clicks(self.layout.cor_01)
        self.palette_cor_02 = Clicks(self.layout.cor_02)
        self.palette_cor_03 = Clicks(self.layout.cor_03)
        self.palette_cor_04 = Clicks(self.layout.cor_04)
        self.palette_cor_05 = Clicks(self.layout.cor_05)
        self.palette_cor_06 = Clicks(self.layout.cor_06)
        self.palette_cor_07 = Clicks(self.layout.cor_07)
        self.palette_cor_08 = Clicks(self.layout.cor_08)
        self.palette_cor_09 = Clicks(self.layout.cor_09)
        self.palette_cor_10 = Clicks(self.layout.cor_10)
        # Palette Signal
        self.palette_cor_01.SIGNAL_CLICKS.connect(self.Color_01)
        self.palette_cor_02.SIGNAL_CLICKS.connect(self.Color_02)
        self.palette_cor_03.SIGNAL_CLICKS.connect(self.Color_03)
        self.palette_cor_04.SIGNAL_CLICKS.connect(self.Color_04)
        self.palette_cor_05.SIGNAL_CLICKS.connect(self.Color_05)
        self.palette_cor_06.SIGNAL_CLICKS.connect(self.Color_06)
        self.palette_cor_07.SIGNAL_CLICKS.connect(self.Color_07)
        self.palette_cor_08.SIGNAL_CLICKS.connect(self.Color_08)
        self.palette_cor_09.SIGNAL_CLICKS.connect(self.Color_09)
        self.palette_cor_10.SIGNAL_CLICKS.connect(self.Color_10)
    def Threads(self):
        # Pigment Operations
        self.thread_timer = threading.Thread(target=self.Timer, daemon=True)
        self.thread_brush_lock = threading.Thread(target=self.Brush_Lock, daemon=True)
        self.thread_document_profile = threading.Thread(target=self.Document_Profile, daemon=True)
        self.thread_pigment_color = threading.Thread(target=self.Pigment_Color, daemon=True)
        self.thread_pigment_sync = threading.Thread(target=self.Pigment_Sync, daemon=True)
        self.thread_signal_block = threading.Thread(target=self.Signal_Block, daemon=True)
        self.thread_signal_send = threading.Thread(target=self.Signal_Send, daemon=True)
        self.thread_pigment_2_krita = threading.Thread(target=self.Pigment_2_Krita, daemon=True)
        self.thread_pigment_display = threading.Thread(target=self.Pigment_Display, daemon=True)
        self.thread_pigment_display_release = threading.Thread(target=self.Pigment_Display_Release, daemon=True)
        self.thread_pigment_2_hex = threading.Thread(target=self.Pigment_2_HEX, daemon=True)
        self.thread_hex_6_svg = threading.Thread(target=self.HEX_6_SVG, daemon=True)
        self.thread_hex_code = threading.Thread(target=self.HEX_Code, daemon=True)
        self.thread_signal_hsv = threading.Thread(target=self.Signal_HSV, daemon=True)
        self.thread_signal_hsl = threading.Thread(target=self.Signal_HSL, daemon=True)
        # Pigment Relay
        self.thread_pigment_aaa = threading.Thread(target=self.Pigment_AAA, daemon=True)
        self.thread_pigment_rgb_1 = threading.Thread(target=self.Pigment_RGB_1, daemon=True)
        self.thread_pigment_rgb_2 = threading.Thread(target=self.Pigment_RGB_2, daemon=True)
        self.thread_pigment_rgb_3 = threading.Thread(target=self.Pigment_RGB_3, daemon=True)
        self.thread_pigment_hsv_1 = threading.Thread(target=self.Pigment_HSV_1, daemon=True)
        self.thread_pigment_hsv_2 = threading.Thread(target=self.Pigment_HSV_2, daemon=True)
        self.thread_pigment_hsv_3 = threading.Thread(target=self.Pigment_HSV_3, daemon=True)
        self.thread_pigment_hsl_1 = threading.Thread(target=self.Pigment_HSL_1, daemon=True)
        self.thread_pigment_hsl_2 = threading.Thread(target=self.Pigment_HSL_2, daemon=True)
        self.thread_pigment_hsl_3 = threading.Thread(target=self.Pigment_HSL_3, daemon=True)
        self.thread_pigment_cmyk_1 = threading.Thread(target=self.Pigment_CMYK_1, daemon=True)
        self.thread_pigment_cmyk_2 = threading.Thread(target=self.Pigment_CMYK_2, daemon=True)
        self.thread_pigment_cmyk_3 = threading.Thread(target=self.Pigment_CMYK_3, daemon=True)
        self.thread_pigment_cmyk_4 = threading.Thread(target=self.Pigment_CMYK_4, daemon=True)
        # Window Display
        self.thread_display_aaa = threading.Thread(target=self.Display_AAA, daemon=True)
        self.thread_display_rgb = threading.Thread(target=self.Display_RGB, daemon=True)
        self.thread_display_hsv = threading.Thread(target=self.Display_HSV, daemon=True)
        self.thread_display_hsl = threading.Thread(target=self.Display_HSL, daemon=True)
        self.thread_display_cmyk = threading.Thread(target=self.Display_CMYK, daemon=True)
        self.thread_display_cores = threading.Thread(target=self.Display_Cores, daemon=True)
        self.thread_display_tts = threading.Thread(target=self.Display_TTS, daemon=True)
        self.thread_display_mixer = threading.Thread(target=self.Display_Mixer, daemon=True)
        self.thread_mixer_shrink = threading.Thread(target=self.Mixer_Shrink, daemon=True)
        self.thread_display_panel = threading.Thread(target=self.Display_Panel, daemon=True)
        # Palette
        self.thread_color_01 = threading.Thread(target=self.Color_01, daemon=True)
        self.thread_color_02 = threading.Thread(target=self.Color_02, daemon=True)
        self.thread_color_03 = threading.Thread(target=self.Color_03, daemon=True)
        self.thread_color_04 = threading.Thread(target=self.Color_04, daemon=True)
        self.thread_color_05 = threading.Thread(target=self.Color_05, daemon=True)
        self.thread_color_06 = threading.Thread(target=self.Color_06, daemon=True)
        self.thread_color_07 = threading.Thread(target=self.Color_07, daemon=True)
        self.thread_color_08 = threading.Thread(target=self.Color_08, daemon=True)
        self.thread_color_09 = threading.Thread(target=self.Color_09, daemon=True)
        self.thread_color_10 = threading.Thread(target=self.Color_10, daemon=True)
        self.thread_color_apply = threading.Thread(target=self.Color_Apply, daemon=True)
        # Mixer Color
        self.thread_mixer_neutral = threading.Thread(target=self.Mixer_Neutral, daemon=True)
        self.thread_mixer_rgb_l1 = threading.Thread(target=self.Mixer_RGB_L1, daemon=True)
        self.thread_mixer_rgb_l2 = threading.Thread(target=self.Mixer_RGB_L2, daemon=True)
        self.thread_mixer_rgb_l3 = threading.Thread(target=self.Mixer_RGB_L3, daemon=True)
        self.thread_mixer_rgb_r1 = threading.Thread(target=self.Mixer_RGB_R1, daemon=True)
        self.thread_mixer_rgb_r2 = threading.Thread(target=self.Mixer_RGB_R2, daemon=True)
        self.thread_mixer_rgb_r3 = threading.Thread(target=self.Mixer_RGB_R3, daemon=True)
        self.thread_mixer_hsv_l1 = threading.Thread(target=self.Mixer_HSV_L1, daemon=True)
        self.thread_mixer_hsv_l2 = threading.Thread(target=self.Mixer_HSV_L2, daemon=True)
        self.thread_mixer_hsv_l3 = threading.Thread(target=self.Mixer_HSV_L3, daemon=True)
        self.thread_mixer_hsv_r1 = threading.Thread(target=self.Mixer_HSV_R1, daemon=True)
        self.thread_mixer_hsv_r2 = threading.Thread(target=self.Mixer_HSV_R2, daemon=True)
        self.thread_mixer_hsv_r3 = threading.Thread(target=self.Mixer_HSV_R3, daemon=True)
        self.thread_mixer_hsl_l1 = threading.Thread(target=self.Mixer_HSL_L1, daemon=True)
        self.thread_mixer_hsl_l2 = threading.Thread(target=self.Mixer_HSL_L2, daemon=True)
        self.thread_mixer_hsl_l3 = threading.Thread(target=self.Mixer_HSL_L3, daemon=True)
        self.thread_mixer_hsl_r1 = threading.Thread(target=self.Mixer_HSL_R1, daemon=True)
        self.thread_mixer_hsl_r2 = threading.Thread(target=self.Mixer_HSL_R2, daemon=True)
        self.thread_mixer_hsl_r3 = threading.Thread(target=self.Mixer_HSL_R3, daemon=True)
        self.thread_mixer_cmyk_l1 = threading.Thread(target=self.Mixer_CMYK_L1, daemon=True)
        self.thread_mixer_cmyk_l2 = threading.Thread(target=self.Mixer_CMYK_L2, daemon=True)
        self.thread_mixer_cmyk_l3 = threading.Thread(target=self.Mixer_CMYK_L3, daemon=True)
        self.thread_mixer_cmyk_r1 = threading.Thread(target=self.Mixer_CMYK_R1, daemon=True)
        self.thread_mixer_cmyk_r2 = threading.Thread(target=self.Mixer_CMYK_R2, daemon=True)
        self.thread_mixer_cmyk_r3 = threading.Thread(target=self.Mixer_CMYK_R3, daemon=True)
        # Mixer Gradient
        self.thread_mixer_tint = threading.Thread(target=self.Mixer_Tint, daemon=True)
        self.thread_mixer_tone = threading.Thread(target=self.Mixer_Tone, daemon=True)
        self.thread_mixer_shade = threading.Thread(target=self.Mixer_Shade, daemon=True)
        self.thread_mixer_rgb_g1 = threading.Thread(target=self.Mixer_RGB_G1, daemon=True)
        self.thread_mixer_rgb_g2 = threading.Thread(target=self.Mixer_RGB_G2, daemon=True)
        self.thread_mixer_rgb_g3 = threading.Thread(target=self.Mixer_RGB_G3, daemon=True)
        self.thread_mixer_hsv_g1 = threading.Thread(target=self.Mixer_HSV_G1, daemon=True)
        self.thread_mixer_hsv_g2 = threading.Thread(target=self.Mixer_HSV_G2, daemon=True)
        self.thread_mixer_hsv_g3 = threading.Thread(target=self.Mixer_HSV_G3, daemon=True)
        self.thread_mixer_hsl_g1 = threading.Thread(target=self.Mixer_HSL_G1, daemon=True)
        self.thread_mixer_hsl_g2 = threading.Thread(target=self.Mixer_HSL_G2, daemon=True)
        self.thread_mixer_hsl_g3 = threading.Thread(target=self.Mixer_HSL_G3, daemon=True)
        self.thread_mixer_cmyk_g1 = threading.Thread(target=self.Mixer_CMYK_G1, daemon=True)
        self.thread_mixer_cmyk_g2 = threading.Thread(target=self.Mixer_CMYK_G2, daemon=True)
        self.thread_mixer_cmyk_g3 = threading.Thread(target=self.Mixer_CMYK_G3, daemon=True)
        # Mixer Output
        self.thread_mixer_color = threading.Thread(target=self.Mixer_Color, daemon=True)
        self.thread_mixer_display = threading.Thread(target=self.Mixer_Display, daemon=True)
        self.thread_colors = threading.Thread(target=self.Colors, daemon=True)
        self.thread_current_colors = threading.Thread(target=self.Current_Colors, daemon=True)
        self.thread_neutral_colors = threading.Thread(target=self.Neutral_Colors, daemon=True)
        # Window Events
        self.thread_enter_event = threading.Thread(target=self.enterEvent, daemon=True)
        self.thread_leave_event = threading.Thread(target=self.leaveEvent, daemon=True)
        self.thread_show_event = threading.Thread(target=self.showEvent, daemon=True)
        self.thread_resize_event = threading.Thread(target=self.resizeEvent, daemon=True)
        self.thread_close_event = threading.Thread(target=self.closeEvent, daemon=True)
        self.thread_ratio = threading.Thread(target=self.Ratio, daemon=True)

        # Pigment Operations
        self.thread_timer.start()
        self.thread_brush_lock.start()
        self.thread_document_profile.start()
        self.thread_pigment_color.start()
        self.thread_pigment_sync.start()
        self.thread_signal_block.start()
        self.thread_signal_send.start()
        self.thread_pigment_2_krita.start()
        self.thread_pigment_display.start()
        self.thread_pigment_display_release.start()
        self.thread_pigment_2_hex.start()
        self.thread_hex_6_svg.start()
        self.thread_hex_code.start()
        self.thread_signal_hsv.start()
        self.thread_signal_hsl.start()
        # Pigment Relay
        self.thread_pigment_aaa.start()
        self.thread_pigment_rgb_1.start()
        self.thread_pigment_rgb_2.start()
        self.thread_pigment_rgb_3.start()
        self.thread_pigment_hsv_1.start()
        self.thread_pigment_hsv_2.start()
        self.thread_pigment_hsv_3.start()
        self.thread_pigment_hsl_1.start()
        self.thread_pigment_hsl_2.start()
        self.thread_pigment_hsl_3.start()
        self.thread_pigment_cmyk_1.start()
        self.thread_pigment_cmyk_2.start()
        self.thread_pigment_cmyk_3.start()
        self.thread_pigment_cmyk_4.start()
        # Window Display
        self.thread_display_aaa.start()
        self.thread_display_rgb.start()
        self.thread_display_hsv.start()
        self.thread_display_hsl.start()
        self.thread_display_cmyk.start()
        self.thread_display_cores.start()
        self.thread_display_tts.start()
        self.thread_display_mixer.start()
        self.thread_mixer_shrink.start()
        self.thread_display_panel.start()
        # Palette
        self.thread_color_01.start()
        self.thread_color_02.start()
        self.thread_color_03.start()
        self.thread_color_04.start()
        self.thread_color_05.start()
        self.thread_color_06.start()
        self.thread_color_07.start()
        self.thread_color_08.start()
        self.thread_color_09.start()
        self.thread_color_10.start()
        self.thread_color_apply.start()
        # Mixer Color
        self.thread_mixer_neutral.start()
        self.thread_mixer_rgb_l1.start()
        self.thread_mixer_rgb_l2.start()
        self.thread_mixer_rgb_l3.start()
        self.thread_mixer_rgb_r1.start()
        self.thread_mixer_rgb_r2.start()
        self.thread_mixer_rgb_r3.start()
        self.thread_mixer_hsv_l1.start()
        self.thread_mixer_hsv_l2.start()
        self.thread_mixer_hsv_l3.start()
        self.thread_mixer_hsv_r1.start()
        self.thread_mixer_hsv_r2.start()
        self.thread_mixer_hsv_r3.start()
        self.thread_mixer_hsl_l1.start()
        self.thread_mixer_hsl_l2.start()
        self.thread_mixer_hsl_l3.start()
        self.thread_mixer_hsl_r1.start()
        self.thread_mixer_hsl_r2.start()
        self.thread_mixer_hsl_r3.start()
        self.thread_mixer_cmyk_l1.start()
        self.thread_mixer_cmyk_l2.start()
        self.thread_mixer_cmyk_l3.start()
        self.thread_mixer_cmyk_r1.start()
        self.thread_mixer_cmyk_r2.start()
        self.thread_mixer_cmyk_r3.start()
        # Mixer Gradient
        self.thread_mixer_tint.start()
        self.thread_mixer_tone.start()
        self.thread_mixer_shade.start()
        self.thread_mixer_rgb_g1.start()
        self.thread_mixer_rgb_g2.start()
        self.thread_mixer_rgb_g3.start()
        self.thread_mixer_hsv_g1.start()
        self.thread_mixer_hsv_g2.start()
        self.thread_mixer_hsv_g3.start()
        self.thread_mixer_hsl_g1.start()
        self.thread_mixer_hsl_g2.start()
        self.thread_mixer_hsl_g3.start()
        self.thread_mixer_cmyk_g1.start()
        self.thread_mixer_cmyk_g2.start()
        self.thread_mixer_cmyk_g3.start()
        # Mixer Output
        self.thread_mixer_color.start()
        self.thread_mixer_display.start()
        self.thread_colors.start()
        self.thread_neutral_colors.start()
        # Window Events
        self.thread_enter_event.start()
        self.thread_leave_event.start()
        self.thread_show_event.start()
        self.thread_resize_event.start()
        self.thread_close_event.start()
        self.thread_ratio.start()

        # Krita Update Timer
        if check_timer >= 1000:
            self.thread_update = threading.Thread(target=self.Krita_Update, daemon=True)
            self.thread_update.start()
    def Style_Sheet(self):
        # UI Percentage Gradients Display
        p4 = self.style.Percentage("4")
        p6 = self.style.Percentage("6")
        ten = self.style.Percentage("TEN")
        self.layout.percentage_top.setStyleSheet(ten)
        self.layout.percentage_bot.setStyleSheet(ten)
        self.layout.aaa_tick.setStyleSheet(p4)
        self.layout.rgb_1_tick.setStyleSheet(p4)
        self.layout.rgb_2_tick.setStyleSheet(p4)
        self.layout.rgb_3_tick.setStyleSheet(p4)
        self.layout.hsv_1_tick.setStyleSheet(p6)
        self.layout.hsv_2_tick.setStyleSheet(p4)
        self.layout.hsv_3_tick.setStyleSheet(p4)
        self.layout.hsl_1_tick.setStyleSheet(p6)
        self.layout.hsl_2_tick.setStyleSheet(p4)
        self.layout.hsl_3_tick.setStyleSheet(p4)
        self.layout.cmyk_1_tick.setStyleSheet(p4)
        self.layout.cmyk_2_tick.setStyleSheet(p4)
        self.layout.cmyk_3_tick.setStyleSheet(p4)
        self.layout.cmyk_4_tick.setStyleSheet(p4)
        self.layout.percentage_tts_1.setStyleSheet(ten)
        self.layout.percentage_tts_2.setStyleSheet(ten)
        self.layout.percentage_rgb_1.setStyleSheet(ten)
        self.layout.percentage_rgb_2.setStyleSheet(ten)
        self.layout.percentage_hsv_1.setStyleSheet(ten)
        self.layout.percentage_hsv_2.setStyleSheet(ten)
        self.layout.percentage_hsl_1.setStyleSheet(ten)
        self.layout.percentage_hsl_2.setStyleSheet(ten)
        self.layout.percentage_cmyk_1.setStyleSheet(ten)
        self.layout.percentage_cmyk_2.setStyleSheet(ten)
        # Neutral Start Colors
        black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (0, 0, 0))
        self.layout.neutral.setStyleSheet(black)
        self.layout.rgb_l1.setStyleSheet(black)
        self.layout.rgb_l2.setStyleSheet(black)
        self.layout.rgb_l3.setStyleSheet(black)
        self.layout.rgb_r1.setStyleSheet(black)
        self.layout.rgb_r2.setStyleSheet(black)
        self.layout.rgb_r3.setStyleSheet(black)
        self.layout.hsv_l1.setStyleSheet(black)
        self.layout.hsv_l2.setStyleSheet(black)
        self.layout.hsv_l3.setStyleSheet(black)
        self.layout.hsv_r1.setStyleSheet(black)
        self.layout.hsv_r2.setStyleSheet(black)
        self.layout.hsv_r3.setStyleSheet(black)
        self.layout.hsl_l1.setStyleSheet(black)
        self.layout.hsl_l2.setStyleSheet(black)
        self.layout.hsl_l3.setStyleSheet(black)
        self.layout.hsl_r1.setStyleSheet(black)
        self.layout.hsl_r2.setStyleSheet(black)
        self.layout.hsl_r3.setStyleSheet(black)
        self.layout.cmyk_l1.setStyleSheet(black)
        self.layout.cmyk_l2.setStyleSheet(black)
        self.layout.cmyk_l3.setStyleSheet(black)
        self.layout.cmyk_r1.setStyleSheet(black)
        self.layout.cmyk_r2.setStyleSheet(black)
        self.layout.cmyk_r3.setStyleSheet(black)
        # Neutral Start Gradients
        neutral = str("background-color: rgba(%f, %f, %f, %f);" % (0, 0, 0, 0))
        self.layout.rgb_g1.setStyleSheet(neutral)
        self.layout.rgb_g2.setStyleSheet(neutral)
        self.layout.rgb_g3.setStyleSheet(neutral)
        self.layout.hsv_g1.setStyleSheet(neutral)
        self.layout.hsv_g2.setStyleSheet(neutral)
        self.layout.hsv_g3.setStyleSheet(neutral)
        self.layout.hsl_g1.setStyleSheet(neutral)
        self.layout.hsl_g2.setStyleSheet(neutral)
        self.layout.hsl_g3.setStyleSheet(neutral)
        self.layout.cmyk_g1.setStyleSheet(neutral)
        self.layout.cmyk_g2.setStyleSheet(neutral)
        self.layout.cmyk_g3.setStyleSheet(neutral)

    # Function Operations
    def Timer(self):
        font = self.layout.check.font()
        if self.layout.check.isChecked():
            font.setBold(True)
            self.layout.check.setText("ON")
        else:
            font.setBold(False)
            self.layout.check.setText("OFF")
        self.layout.check.setFont(font)
    def Brush_Lock(self, SIGNAL_CLICKS):
        # Check if there is a valid Document Active
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            # Current View
            self.view = Krita.instance().activeWindow().activeView()
            if SIGNAL_CLICKS == "APPLY":
                try:
                    self.view.setBrushSize(self.size)
                    self.view.setPaintingOpacity(self.opacity)
                    self.view.setPaintingFlow(self.flow)
                    self.tip_00.Setup(self.size, self.opacity, self.flow)
                except:
                    self.view.setBrushSize(size)
                    self.view.setPaintingOpacity(opacity)
                    self.view.setPaintingFlow(flow)
                    self.tip_00.Setup(size, opacity, flow)
            elif (SIGNAL_CLICKS == "SAVE" or SIGNAL_CLICKS == "CLEAN"):
                self.size = self.view.brushSize()
                self.opacity = self.view.paintingOpacity()
                self.flow = self.view.paintingFlow()
                self.tip_00.Setup(self.size, self.opacity, self.flow)
    def Document_Profile(self):
        try:
            ki = Krita.instance()
            ad = ki.activeDocument()
            color_model = ad.colorModel()
            color_depth = ad.colorDepth()
            color_profile = ad.colorProfile()
            doc = []
            doc.append(color_model)
            doc.append(color_depth)
            doc.append(color_profile)
        except:
            doc = ["NONE", "NONE", "NONE"]
        return doc
    def Pigment_Color(self, mode):
        # Change Color
        if mode == "AAA":
            # Original
            aaa = self.layout.aaa_value.value() / factorAAA
            # Converts
            hsv = self.convert.rgb_to_hsv(aaa, aaa, aaa)
            hsl = self.convert.rgb_to_hsl(aaa, aaa, aaa)
            cmyk = self.convert.rgb_to_cmyk(aaa, aaa, aaa)
            # to RGB
            rgb1 = aaa
            rgb2 = aaa
            rgb3 = aaa
            # to HSV
            hsv1 = hsv[0]
            hsv2 = hsv[1]
            hsv3 = hsv[2]
            # to HSL
            hsl1 = hsl[0]
            hsl2 = hsl[1]
            hsl3 = hsl[2]
            # to CMYK
            cmyk1 = cmyk[0]
            cmyk2 = cmyk[1]
            cmyk3 = cmyk[2]
            cmyk4 = cmyk[3]
        elif mode == "RGB":
            # Original
            rgb1 = self.layout.rgb_1_value.value() / factorRGB
            rgb2 = self.layout.rgb_2_value.value() / factorRGB
            rgb3 = self.layout.rgb_3_value.value() / factorRGB
            # Conversions
            hsv = self.convert.rgb_to_hsv(rgb1, rgb2, rgb3)
            hsl = self.convert.rgb_to_hsl(rgb1, rgb2, rgb3)
            cmyk = self.convert.rgb_to_cmyk(rgb1, rgb2, rgb3)
            # to Alpha
            aaa = max(rgb1, rgb2, rgb3)
            # to HSV
            hsv1 = hsv[0]
            hsv2 = hsv[1]
            hsv3 = hsv[2]
            # to HSL
            hsl1 = hsl[0]
            hsl2 = hsl[1]
            hsl3 = hsl[2]
            # to CMYK
            cmyk1 = cmyk[0]
            cmyk2 = cmyk[1]
            cmyk3 = cmyk[2]
            cmyk4 = cmyk[3]
        elif mode == "HSV":
            # Original
            hsv1 = self.layout.hsv_1_value.value() / factorHUE
            hsv2 = self.layout.hsv_2_value.value() / factorSVL
            hsv3 = self.layout.hsv_3_value.value() / factorSVL
            # Conversions
            rgb = self.convert.hsv_to_rgb(hsv1, hsv2, hsv3)
            hsl = self.convert.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
            cmyk = self.convert.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
            # to Alpha
            aaa = max(rgb[0], rgb[1], rgb[2])
            # to RGB
            rgb1 = rgb[0]
            rgb2 = rgb[1]
            rgb3 = rgb[2]
            # to HSL
            hsl1 = hsl[0]
            hsl2 = hsl[1]
            hsl3 = hsl[2]
            # to CMYK
            cmyk1 = cmyk[0]
            cmyk2 = cmyk[1]
            cmyk3 = cmyk[2]
            cmyk4 = cmyk[3]
        elif mode == "HSL":
            # Original
            hsl1 = self.layout.hsl_1_value.value() / factorHUE
            hsl2 = self.layout.hsl_2_value.value() / factorSVL
            hsl3 = self.layout.hsl_3_value.value() / factorSVL
            # Conversions
            rgb = self.convert.hsl_to_rgb(hsl1, hsl2, hsl3)
            hsv = self.convert.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
            cmyk = self.convert.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
            # to Alpha
            aaa = max(rgb[0], rgb[1], rgb[2])
            # to RGB
            rgb1 = rgb[0]
            rgb2 = rgb[1]
            rgb3 = rgb[2]
            # to HSV
            hsv1 = hsv[0]
            hsv2 = hsv[1]
            hsv3 = hsv[2]
            # to CMYK
            cmyk1 = cmyk[0]
            cmyk2 = cmyk[1]
            cmyk3 = cmyk[2]
            cmyk4 = cmyk[3]
        elif mode == "CMYK":
            # Original
            cmyk1 = self.layout.cmyk_1_value.value() / factorCMYK
            cmyk2 = self.layout.cmyk_2_value.value() / factorCMYK
            cmyk3 = self.layout.cmyk_3_value.value() / factorCMYK
            cmyk4 = self.layout.cmyk_4_value.value() / factorCMYK
            # Conversions
            rgb = self.convert.cmyk_to_rgb(cmyk1, cmyk2, cmyk3, cmyk4)
            hsv = self.convert.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
            hsl = self.convert.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
            # to Alpha
            aaa = max(rgb[0], rgb[1], rgb[2])
            # to RGB
            rgb1 = rgb[0]
            rgb2 = rgb[1]
            rgb3 = rgb[2]
            # to HSV
            hsv1 = hsv[0]
            hsv2 = hsv[1]
            hsv3 = hsv[2]
            # to HSL
            hsl1 = hsl[0]
            hsl2 = hsl[1]
            hsl3 = hsl[2]
        # Pigment Update Values
        self.Pigment_Sync(mode, aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
        self.Pigment_2_Krita(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
        self.Pigment_Display(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
    def Pigment_Sync(self, mode, aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4):
        if mode == "AAA":
            # Block Signals
            self.Signal_Block("RGB", True)
            self.Signal_Block("HSV", True)
            self.Signal_Block("HSL", True)
            self.Signal_Block("CMYK", True)
            # Set Values
            self.Signal_Send("RGB", rgb1, rgb2, rgb3, 0)
            self.Signal_Send("HSV", hsv1, hsv2, hsv3, 0)
            self.Signal_Send("HSL", hsl1, hsl2, hsl3, 0)
            self.Signal_Send("CMYK", cmyk1, cmyk2, cmyk3, cmyk4)
            # UnBlock Signals
            self.Signal_Block("RGB", False)
            self.Signal_Block("HSV", False)
            self.Signal_Block("HSL", False)
            self.Signal_Block("CMYK", False)
        elif mode == "RGB":
            # Block Signals
            self.Signal_Block("AAA", True)
            self.Signal_Block("HSV", True)
            self.Signal_Block("HSL", True)
            self.Signal_Block("CMYK", True)
            # Set Values
            self.Signal_Send("AAA", aaa, 0, 0, 0)
            self.Signal_Send("HSV", hsv1, hsv2, hsv3, 0)
            self.Signal_Send("HSL", hsl1, hsl2, hsl3, 0)
            self.Signal_Send("CMYK", cmyk1, cmyk2, cmyk3, cmyk4)
            # UnBlock Signals
            self.Signal_Block("AAA", False)
            self.Signal_Block("HSV", False)
            self.Signal_Block("HSL", False)
            self.Signal_Block("CMYK", False)
        elif mode == "HSV":
            # Block Signals
            self.Signal_Block("AAA", True)
            self.Signal_Block("RGB", True)
            self.Signal_Block("HSL", True)
            self.Signal_Block("CMYK", True)
            # Set Values
            self.Signal_Send("AAA", aaa, 0, 0, 0)
            self.Signal_Send("RGB", rgb1, rgb2, rgb3, 0)
            self.Signal_Send("HSL", hsl1, hsl2, hsl3, 0)
            self.Signal_Send("CMYK", cmyk1, cmyk2, cmyk3, cmyk4)
            # UnBlock Signals
            self.Signal_Block("AAA", False)
            self.Signal_Block("RGB", False)
            self.Signal_Block("HSL", False)
            self.Signal_Block("CMYK", False)
        elif mode == "HSL":
            # Block Signals
            self.Signal_Block("AAA", True)
            self.Signal_Block("RGB", True)
            self.Signal_Block("HSV", True)
            self.Signal_Block("CMYK", True)
            # Set Values
            self.Signal_Send("AAA", aaa, 0, 0, 0)
            self.Signal_Send("RGB", rgb1, rgb2, rgb3, 0)
            self.Signal_Send("HSV", hsv1, hsv2, hsv3, 0)
            self.Signal_Send("CMYK", cmyk1, cmyk2, cmyk3, cmyk4)
            # UnBlock Signals
            self.Signal_Block("AAA", False)
            self.Signal_Block("RGB", False)
            self.Signal_Block("HSV", False)
            self.Signal_Block("CMYK", False)
        elif mode == "CMYK":
            # Block Signals
            self.Signal_Block("AAA", True)
            self.Signal_Block("RGB", True)
            self.Signal_Block("HSV", True)
            self.Signal_Block("HSL", True)
            # Set Values
            self.Signal_Send("AAA", aaa, 0, 0, 0)
            self.Signal_Send("RGB", rgb1, rgb2, rgb3, 0)
            self.Signal_Send("HSV", hsv1, hsv2, hsv3, 0)
            self.Signal_Send("HSL", hsl1, hsl2, hsl3, 0)
            # UnBlock Signals
            self.Signal_Block("AAA", False)
            self.Signal_Block("RGB", False)
            self.Signal_Block("HSV", False)
            self.Signal_Block("HSL", False)
        elif mode == "MIX":
            # Block Signals
            self.Signal_Block("AAA", True)
            self.Signal_Block("RGB", True)
            self.Signal_Block("HSV", True)
            self.Signal_Block("HSL", True)
            self.Signal_Block("CMYK", True)
            # Set Values
            self.Signal_Send("AAA", aaa, 0, 0, 0)
            self.Signal_Send("RGB", rgb1, rgb2, rgb3, 0)
            self.Signal_Send("HSV", hsv1, hsv2, hsv3, 0)
            self.Signal_Send("HSL", hsl1, hsl2, hsl3, 0)
            self.Signal_Send("CMYK", cmyk1, cmyk2, cmyk3, cmyk4)
            # UnBlock Signals
            self.Signal_Block("AAA", False)
            self.Signal_Block("RGB", False)
            self.Signal_Block("HSV", False)
            self.Signal_Block("HSL", False)
            self.Signal_Block("CMYK", False)
    def Signal_Block(self, colorspace, boolean):
        if colorspace == "AAA":
            self.layout.aaa_value.blockSignals(boolean)
            self.layout.aaa_slider.blockSignals(boolean)
        elif colorspace == "RGB":
            self.layout.rgb_1_value.blockSignals(boolean)
            self.layout.rgb_2_value.blockSignals(boolean)
            self.layout.rgb_3_value.blockSignals(boolean)
            self.layout.rgb_1_slider.blockSignals(boolean)
            self.layout.rgb_2_slider.blockSignals(boolean)
            self.layout.rgb_3_slider.blockSignals(boolean)
        elif colorspace == "HSV":
            self.layout.hsv_1_value.blockSignals(boolean)
            self.layout.hsv_2_value.blockSignals(boolean)
            self.layout.hsv_3_value.blockSignals(boolean)
            self.layout.hsv_1_slider.blockSignals(boolean)
            self.layout.hsv_2_slider.blockSignals(boolean)
            self.layout.hsv_3_slider.blockSignals(boolean)
        elif colorspace == "HSL":
            self.layout.hsl_1_value.blockSignals(boolean)
            self.layout.hsl_2_value.blockSignals(boolean)
            self.layout.hsl_3_value.blockSignals(boolean)
            self.layout.hsl_1_slider.blockSignals(boolean)
            self.layout.hsl_2_slider.blockSignals(boolean)
            self.layout.hsl_3_slider.blockSignals(boolean)
        elif colorspace == "CMYK":
            self.layout.cmyk_1_value.blockSignals(boolean)
            self.layout.cmyk_2_value.blockSignals(boolean)
            self.layout.cmyk_3_value.blockSignals(boolean)
            self.layout.cmyk_4_value.blockSignals(boolean)
            self.layout.cmyk_1_slider.blockSignals(boolean)
            self.layout.cmyk_2_slider.blockSignals(boolean)
            self.layout.cmyk_3_slider.blockSignals(boolean)
            self.layout.cmyk_4_slider.blockSignals(boolean)
    def Signal_Send(self, colorspace, value1, value2, value3, value4):
        if colorspace == "AAA":
            self.layout.aaa_value.setValue(value1 * factorAAA)
            self.aaa_slider.Update(value1 * factorAAA, factorAAA, self.layout.aaa_slider.width())
        elif colorspace == "RGB":
            self.layout.rgb_1_value.setValue(value1 * factorRGB)
            self.layout.rgb_2_value.setValue(value2 * factorRGB)
            self.layout.rgb_3_value.setValue(value3 * factorRGB)
            self.rgb_1_slider.Update(value1 * factorRGB, factorRGB, self.layout.rgb_1_slider.width())
            self.rgb_2_slider.Update(value2 * factorRGB, factorRGB, self.layout.rgb_2_slider.width())
            self.rgb_3_slider.Update(value3 * factorRGB, factorRGB, self.layout.rgb_3_slider.width())
        elif colorspace == "HSV":
            self.layout.hsv_1_value.setValue(value1 * factorHUE)
            self.layout.hsv_2_value.setValue(value2 * factorSVL)
            self.layout.hsv_3_value.setValue(value3 * factorSVL)
            self.hsv_1_slider.Update(value1 * factorHUE, factorHUE, self.layout.hsv_1_slider.width())
            self.hsv_2_slider.Update(value2 * factorSVL, factorSVL, self.layout.hsv_2_slider.width())
            self.hsv_3_slider.Update(value3 * factorSVL, factorSVL, self.layout.hsv_3_slider.width())
        elif colorspace == "HSL":
            self.layout.hsl_1_value.setValue(value1 * factorHUE)
            self.layout.hsl_2_value.setValue(value2 * factorSVL)
            self.layout.hsl_3_value.setValue(value3 * factorSVL)
            self.hsl_1_slider.Update(value1 * factorHUE, factorHUE, self.layout.hsl_1_slider.width())
            self.hsl_2_slider.Update(value2 * factorSVL, factorSVL, self.layout.hsl_2_slider.width())
            self.hsl_3_slider.Update(value3 * factorSVL, factorSVL, self.layout.hsl_3_slider.width())
        elif colorspace == "CMYK":
            self.layout.cmyk_1_value.setValue(value1 * factorCMYK)
            self.layout.cmyk_2_value.setValue(value2 * factorCMYK)
            self.layout.cmyk_3_value.setValue(value3 * factorCMYK)
            self.layout.cmyk_4_value.setValue(value4 * factorCMYK)
            self.cmyk_1_slider.Update(value1 * factorCMYK, factorCMYK, self.layout.cmyk_1_slider.width())
            self.cmyk_2_slider.Update(value2 * factorCMYK, factorCMYK, self.layout.cmyk_2_slider.width())
            self.cmyk_3_slider.Update(value3 * factorCMYK, factorCMYK, self.layout.cmyk_3_slider.width())
            self.cmyk_4_slider.Update(value4 * factorCMYK, factorCMYK, self.layout.cmyk_4_slider.width())
        # Panels
        self.panel_hsv.Update_Panel(self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value(), self.layout.panel_hsv_fg.width(), self.layout.panel_hsv_fg.height(), self.HEX_6_SVG())
        self.panel_hsl.Update_Panel(self.layout.hsl_2_value.value(), self.layout.hsl_3_value.value(), self.layout.panel_hsl_fg.width(), self.layout.panel_hsl_fg.height(), self.HEX_6_SVG())
    def Pigment_2_Krita(self, aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4):
        # Check if there is a valid Document Active
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            pigment = self.layout.check.text()
            if (pigment == "ON" or pigment == "&ON"):
                # Check Eraser Mode ON or OFF
                kritaEraserAction = Application.action("erase_action")
                # Check Document Profile
                doc = self.Document_Profile()
                # Alpha mask
                if doc[0] == "A":
                    # Apply Color to Krita in RGB (This nullifies the Eraser if it is ON)
                    pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                    pigment_color.setComponents([aaa])
                    Application.activeWindow().activeView().setForeGroundColor(pigment_color)
                    # If Eraser, set it ON again
                    if kritaEraserAction.isChecked():
                        kritaEraserAction.trigger()
                elif doc[0] == "GRAYA":  # Gray with alpha channel
                    # Apply Color to Krita in RGB (This nullifies the Eraser if it is ON)
                    pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                    pigment_color.setComponents([aaa, 1.0])
                    Application.activeWindow().activeView().setForeGroundColor(pigment_color)
                    # If Eraser, set it ON again
                    if kritaEraserAction.isChecked():
                        kritaEraserAction.trigger()
                elif doc[0] == "RGBA":  # RGB with alpha channel (The actual order of channels is most often BGR!)
                    # Apply Color to Krita in RGB (This nullifies the Eraser if it is ON)
                    pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                    pigment_color.setComponents([rgb3, rgb2, rgb1, 1.0])
                    Application.activeWindow().activeView().setForeGroundColor(pigment_color)
                    # If Eraser, set it ON again
                    if kritaEraserAction.isChecked():
                        kritaEraserAction.trigger()
                elif doc[0] == "CMYKA":  # CMYK with alpha channel
                    # Apply Color to Krita in RGB (This nullifies the Eraser if it is ON)
                    pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                    pigment_color.setComponents([cmyk1, cmyk2, cmyk3, cmyk4, 1.0])
                    Application.activeWindow().activeView().setForeGroundColor(pigment_color)
                    # If Eraser, set it ON again
                    if kritaEraserAction.isChecked():
                        kritaEraserAction.trigger()
                elif doc[0] == "XYZA":  # XYZ with alpha channel
                    pass
                elif doc[0] == "LABA":  # LAB with alpha channel
                    pass
                elif doc[0] == "YCbCrA":  # YCbCr with alpha channel
                    pass
        else:
            pass
    def Pigment_Display(self, aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4):
        # Foreground Color Display (Top Left)
        active_color_1 = str("QWidget { background-color: rgb(%f, %f, %f);}" % (rgb1*factorRGB, rgb2*factorRGB, rgb3*factorRGB))
        self.layout.color_1.setStyleSheet(active_color_1)
        # Alpha
        sss_aaa = str(self.style.Slider("AAA", 0, aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3))
        # RGB
        sss_rgb1 = str(self.style.Slider("RGB", 0, aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3))
        sss_rgb2 = str(self.style.Slider("RGB", 1, aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3))
        sss_rgb3 = str(self.style.Slider("RGB", 2, aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3))
        # HSV
        sss_hsv1 = str(self.style.Slider("HSV", 0, aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3))
        hsv2_left = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, 0, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
        hsv2_right = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, 1, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
        hsv3_left = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, 0, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
        hsv3_right = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, 1, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
        sss_hsv2 = str(self.style.HSV_Gradient(self.layout.hsv_2_slider.width(), hsv2_left, hsv2_right))
        sss_hsv3 = str(self.style.HSV_Gradient(self.layout.hsv_3_slider.width(), hsv3_left, hsv3_right))
        # HSL
        sss_hsl1 = str(self.style.Slider("HSL", 0, aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3))
        hsl2_left = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, 0, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
        hsl2_right = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, 1, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
        hsl3_left = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, 0, cmyk1, cmyk2, cmyk3, cmyk4)
        hsl3_right = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, 1, cmyk1, cmyk2, cmyk3, cmyk4)
        sss_hsl2 = str(self.style.HSL_Gradient(self.layout.hsl_2_slider.width(), hsl2_left, hsl2_right))
        sss_hsl3 = str(self.style.HSL_Gradient(self.layout.hsl_3_slider.width(), hsl3_left, hsl3_right))
        # CMYK
        cmyk1_left = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, 0, cmyk2, cmyk3, cmyk4)
        cmyk1_right = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, 1, cmyk2, cmyk3, cmyk4)
        cmyk2_left = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, 0, cmyk3, cmyk4)
        cmyk2_right = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, 1, cmyk3, cmyk4)
        cmyk3_left = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, 0, cmyk4)
        cmyk3_right = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, 1, cmyk4)
        cmyk4_left = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, 0)
        cmyk4_right = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, 1)
        sss_cmyk1 = str(self.style.CMYK_Gradient(self.layout.cmyk_1_slider.width(), cmyk1_left, cmyk1_right))
        sss_cmyk2 = str(self.style.CMYK_Gradient(self.layout.cmyk_2_slider.width(), cmyk2_left, cmyk2_right))
        sss_cmyk3 = str(self.style.CMYK_Gradient(self.layout.cmyk_3_slider.width(), cmyk3_left, cmyk3_right))
        sss_cmyk4 = str(self.style.CMYK_Gradient(self.layout.cmyk_4_slider.width(), cmyk4_left, cmyk4_right))
        # Apply Style Sheets
        self.layout.aaa_slider.setStyleSheet(sss_aaa)
        self.layout.rgb_1_slider.setStyleSheet(sss_rgb1)
        self.layout.rgb_2_slider.setStyleSheet(sss_rgb2)
        self.layout.rgb_3_slider.setStyleSheet(sss_rgb3)
        self.layout.hsv_1_slider.setStyleSheet(sss_hsv1)
        self.layout.hsv_2_slider.setStyleSheet(sss_hsv2)
        self.layout.hsv_3_slider.setStyleSheet(sss_hsv3)
        self.layout.hsl_1_slider.setStyleSheet(sss_hsl1)
        self.layout.hsl_2_slider.setStyleSheet(sss_hsl2)
        self.layout.hsl_3_slider.setStyleSheet(sss_hsl3)
        self.layout.cmyk_1_slider.setStyleSheet(sss_cmyk1)
        self.layout.cmyk_2_slider.setStyleSheet(sss_cmyk2)
        self.layout.cmyk_3_slider.setStyleSheet(sss_cmyk3)
        self.layout.cmyk_4_slider.setStyleSheet(sss_cmyk4)
        # Check Amount of Channels
        channels = "THREE"
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            doc = self.Document_Profile()
            if (doc[0] == "A" or doc[0] == "GRAYA"):
                channels = "ONE"
            elif doc[0] == "CMYKA":
                channels = "FOUR"
        # Hex Color
        hex = self.Pigment_2_HEX(channels, aaa, rgb1, rgb2, rgb3, cmyk1, cmyk2, cmyk3, cmyk4)
        self.layout.hex_string.setText(str(hex))
        # Panel Display
        panel = self.layout.panel_selector.currentText()
        # Colors for Panels
        if panel == "HSV":
            # Black and White when in Greyscale
            if channels == "ONE":
                hue_left = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, 0, 1, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
                hue_right = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, 0, 1, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
            else:
                hue_left = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, 0, 1, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
                hue_right = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, 1, 1, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
            base_color = self.style.HSV_Panel(self.layout.hsv_1_slider.width(), hue_left, hue_right)
            self.layout.panel_hsv_bg.setStyleSheet(base_color)
            base_value = str("QWidget { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255)); }")
            self.layout.panel_hsv_fg.setStyleSheet(base_value)
        elif panel == "HSV0":
            # Colors for HSV Square Background Gradients
            base_color = str("QWidget { background-color: rgba(0, 0, 0, 0); }")
            self.layout.panel_hsv_bg.setStyleSheet(base_color)
            base_value = str("QWidget { background-color: rgba(0, 0, 0, 0); }")
            self.layout.panel_hsv_fg.setStyleSheet(base_value)
        elif panel == "HSL":
            # Black and White when in Greyscale
            if channels == "ONE":
                hue_left = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, 0, 1, cmyk1, cmyk2, cmyk3, cmyk4)
                hue_right = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, 0, 1, cmyk1, cmyk2, cmyk3, cmyk4)
            else:
                hue_left = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, 0, 0.5, cmyk1, cmyk2, cmyk3, cmyk4)
                hue_right = self.Colors(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, 1, 0.5, cmyk1, cmyk2, cmyk3, cmyk4)
            base_color = self.style.HSL_Panel(self.layout.hsl_1_slider.width(), hue_left, hue_right)
            self.layout.panel_hsl_bg.setStyleSheet(base_color)
            base_value = str("QWidget { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.5 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255)); }")
            self.layout.panel_hsl_fg.setStyleSheet(base_value)
        elif panel == "HSL0":
            # Colors for HSL Square Background Gradients
            base_color = str("QWidget { background-color: rgba(0, 0, 0, 0); }")
            self.layout.panel_hsl_bg.setStyleSheet(base_color)
            base_value = str("QWidget { background-color: rgba(0, 0, 0, 0); }")
            self.layout.panel_hsl_fg.setStyleSheet(base_value)
    def Pigment_Display_Release(self, SIGNAL_RELEASE):
        rgb1 = self.layout.rgb_1_value.value()
        rgb2 = self.layout.rgb_2_value.value()
        rgb3 = self.layout.rgb_3_value.value()
        active_color_2 = str("QWidget { background-color: rgb(%f, %f, %f);}" % (rgb1, rgb2, rgb3))
        self.layout.color_2.setStyleSheet(active_color_2)
    def Pigment_2_HEX(self, channels, aaa, rgb1, rgb2, rgb3, cmyk1, cmyk2, cmyk3, cmyk4):
        # Convert Fraction Values to Real HEX Values
        aaa = aaa * factorHEXAAA
        rgb1 = rgb1 * factorHEXRGB
        rgb2 = rgb2 * factorHEXRGB
        rgb3 = rgb3 * factorHEXRGB
        cmyk1 = cmyk1 * factorHEXCMYK
        cmyk2 = cmyk2 * factorHEXCMYK
        cmyk3 = cmyk3 * factorHEXCMYK
        # Considering how many channels for HEX code
        if channels == "ONE":
            # self.layout.hex_string.setMaxLength(3)
            aaa = aaa
            hex1 = str(hex(int(aaa)))[2:4].zfill(2)
            pigment_hex = str("#"+hex1)
        elif channels == "THREE":
            # self.layout.hex_string.setMaxLength(7)
            hex1 = str(hex(int(rgb1)))[2:4].zfill(2)
            hex2 = str(hex(int(rgb2)))[2:4].zfill(2)
            hex3 = str(hex(int(rgb3)))[2:4].zfill(2)
            pigment_hex = str("#"+hex1+hex2+hex3)
        elif channels == "FOUR":
            # self.layout.hex_string.setMaxLength(9)
            hex1 = str(hex(int(cmyk1)))[2:4].zfill(2)
            hex2 = str(hex(int(cmyk2)))[2:4].zfill(2)
            hex3 = str(hex(int(cmyk3)))[2:4].zfill(2)
            hex4 = str(hex(int(cmyk4)))[2:4].zfill(2)
            pigment_hex = str("#"+hex1+hex2+hex3+hex4)
        return pigment_hex
    def HEX_6_SVG(self):
        doc = self.Document_Profile()
        if (doc[0] == "A" or doc[0] == "GRAYA"):
            # Query RGB Values
            rgb1 = (self.layout.aaa_value.value() / factorAAA) * factorHEXAAA
            rgb2 = (self.layout.aaa_value.value() / factorAAA) * factorHEXAAA
            rgb3 = (self.layout.aaa_value.value() / factorAAA) * factorHEXAAA
        else:
            # Query RGB Values
            rgb1 = (self.layout.rgb_1_value.value() / factorRGB) * factorHEXRGB
            rgb2 = (self.layout.rgb_2_value.value() / factorRGB) * factorHEXRGB
            rgb3 = (self.layout.rgb_3_value.value() / factorRGB) * factorHEXRGB
        # Transform into HEX
        hex1 = str(hex(int(rgb1)))[2:4].zfill(2)
        hex2 = str(hex(int(rgb2)))[2:4].zfill(2)
        hex3 = str(hex(int(rgb3)))[2:4].zfill(2)
        pigment_hex = str("#"+hex1+hex2+hex3)
        return pigment_hex
    def HEX_Code(self, hex):
        length = len(hex)
        if hex[0] == "#":
            if length == 3:
                # Parse Hex Code
                hex1 = int(format(int(hex[1:3],16),'02d'))
                # Apply to Pigment
                self.Pigment_AAA("HEX", (hex1 / factorHEXAAA) * factorAAA)
            elif length == 7:
                # Parse Hex Code
                hex1 = int(format(int(hex[1:3],16),'02d'))
                hex2 = int(format(int(hex[3:5],16),'02d'))
                hex3 = int(format(int(hex[5:7],16),'02d'))
                # Apply to Pigment
                self.Pigment_RGB_1("HEX", (hex1 / factorHEXRGB) * factorRGB)
                self.Pigment_RGB_2("HEX", (hex2 / factorHEXRGB) * factorRGB)
                self.Pigment_RGB_3("HEX", (hex3 / factorHEXRGB) * factorRGB)
            elif length == 9:
                # Parse Hex Code
                hex1 = int(format(int(hex[1:3],16),'02d'))
                hex2 = int(format(int(hex[3:5],16),'02d'))
                hex3 = int(format(int(hex[5:7],16),'02d'))
                hex4 = int(format(int(hex[7:9],16),'02d'))
                # Apply to Pigment
                self.Pigment_CMYK_1("HEX", (hex1 / factorHEXCMYK) * factorCMYK)
                self.Pigment_CMYK_2("HEX", (hex2 / factorHEXCMYK) * factorCMYK)
                self.Pigment_CMYK_3("HEX", (hex3 / factorHEXCMYK) * factorCMYK)
                self.Pigment_CMYK_4("HEX", (hex4 / factorHEXCMYK) * factorCMYK)
            else:
                self.layout.hex_string.setText("Error")
        else:
            self.layout.hex_string.setText("Error")
    def Signal_HSV(self, SIGNAL_HSV):
        self.layout.hsv_2_value.setValue(round(SIGNAL_HSV[0], 2))
        self.layout.hsv_3_value.setValue(round(SIGNAL_HSV[1], 2))
    def Signal_HSL(self, SIGNAL_HSL):
        self.layout.hsl_2_value.setValue(round(SIGNAL_HSL[0], 2))
        self.layout.hsl_3_value.setValue(round(SIGNAL_HSL[1], 2))
    def Krita_Update(self):
        # Consider if nothing is on the Canvas
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            pigment = self.layout.check.text()
            if (pigment == "ON" or pigment == "&ON"):
                # Check Eraser Mode ON or OFF
                kritaEraserAction = Application.action("erase_action")
                # Pigment Values
                aaa = self.layout.aaa_value.value() / factorAAA
                rgb1 = self.layout.rgb_1_value.value() / factorRGB
                rgb2 = self.layout.rgb_2_value.value() / factorRGB
                rgb3 = self.layout.rgb_3_value.value() / factorRGB
                hsv1 = self.layout.hsv_1_value.value() / factorHUE
                hsv2 = self.layout.hsv_2_value.value() / factorSVL
                hsv3 = self.layout.hsv_3_value.value() / factorSVL
                hsl1 = self.layout.hsl_1_value.value() / factorHUE
                hsl2 = self.layout.hsl_2_value.value() / factorSVL
                hsl3 = self.layout.hsl_3_value.value() / factorSVL
                cmyk1 = self.layout.cmyk_1_value.value() / factorCMYK
                cmyk2 = self.layout.cmyk_2_value.value() / factorCMYK
                cmyk3 = self.layout.cmyk_3_value.value() / factorCMYK
                cmyk4 = self.layout.cmyk_4_value.value() / factorCMYK
                # Document Profile
                doc = self.Document_Profile()
                try:
                    # Current Krita Color
                    color_foreground = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                    color_foreground = Application.activeWindow().activeView().foregroundColor()
                    color_background = Application.activeWindow().activeView().backgroundColor()
                    components_fg = color_foreground.components()
                    components_bg = color_background.components()
                    # Update Pigmento if Values Differ
                    if (doc[0] == "A" or doc[0] == "GRAYA"):
                        # Foreground and Background Colors
                        kac1 = components_fg[0]
                        kbc1 = components_fg[0]
                        # Verify conditions to change Pigment
                        if aaa != kac1:
                            if not kritaEraserAction.isChecked():
                                # Change Pigment
                                self.Pigment_AAA("KU", kac1 * factorAAA)
                                self.Pigment_Color("AAA")
                    elif doc[0] == "RGBA":
                        length = len(components_fg)
                        if length == 2:
                            kac1 = components_fg[0]
                            if aaa != kac1:
                                if not kritaEraserAction.isChecked():
                                    self.Pigment_AAA("KU", kac1 * factorAAA)
                                    self.Pigment_Color("AAA")
                        else:
                            # Foreground and Background Colors (Krita is in BGR)
                            kac1 = components_fg[2] # Blue
                            kac2 = components_fg[1] # Green
                            kac3 = components_fg[0] # Red
                            kbc1 = components_bg[2]
                            kbc2 = components_bg[1]
                            kbc3 = components_bg[0]
                            # Verify conditions to change Pigment
                            if (rgb1 != kac1 or rgb2 != kac2 or rgb3 != kac3):
                                if not kritaEraserAction.isChecked():
                                    # Change Pigment
                                    self.Pigment_RGB_1("KU", kac1 * factorRGB)
                                    self.Pigment_RGB_2("KU", kac2 * factorRGB)
                                    self.Pigment_RGB_3("KU", kac3 * factorRGB)
                                    self.Pigment_Color("RGB")
                    elif doc[0] == "CMYKA":
                        length = len(components_fg)
                        if length == 2:
                            kac1 = components_fg[0]
                            if aaa != kac1:
                                if not kritaEraserAction.isChecked():
                                    self.Pigment_AAA("KU", kac1 * factorAAA)
                                    self.Pigment_Color("AAA")
                        else:
                            # Foreground and Background Colors
                            kac1 = components_fg[0]
                            kac2 = components_fg[1]
                            kac3 = components_fg[2]
                            kac4 = components_fg[3]
                            kbc1 = components_fg[0]
                            kbc2 = components_fg[1]
                            kbc3 = components_fg[2]
                            kbc4 = components_fg[3]
                            # Verify conditions to change Pigment
                            if (cmyk1 != kac1 or cmyk2 != kac2 or cmyk3 != kac3 or cmyk4 != kac4):
                                if not kritaEraserAction.isChecked():
                                    # Change Pigment
                                    self.Pigment_CMYK_1("KU", kac1 * factorCMYK)
                                    self.Pigment_CMYK_2("KU", kac2 * factorCMYK)
                                    self.Pigment_CMYK_3("KU", kac3 * factorCMYK)
                                    self.Pigment_CMYK_4("KU", kac4 * factorCMYK)
                                    self.Pigment_Color("CMYK")
                    elif doc[0] == "XYZA":
                        pass
                    elif doc[0] == "LABA":
                        pass
                    elif doc[0] == "YCbCrA":
                        pass
                except:
                    pass

    # Pigment Color
    def Pigment_AAA(self, case, value):
        width = self.layout.aaa_slider.width()
        if case == "50":
            min = self.layout.aaa_value.minimum()
            max = self.layout.aaa_value.maximum()
            half = (max-min)/2
            self.aaa_slider.Update(half, factorAAA, width)
            self.layout.aaa_value.setValue(half)
        elif case == "M1":
            channel = self.layout.aaa_value.value()
            self.aaa_slider.Update((channel-value), factorAAA, width)
            self.layout.aaa_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.aaa_value.value()
            self.aaa_slider.Update((channel+value), factorAAA, width)
            self.layout.aaa_value.setValue(channel+value)
        elif case == "KU":
            self.aaa_slider.Update(value, factorAAA, width)
            self.layout.aaa_value.setValue(value)
        elif case == "HEX":
            self.aaa_slider.Update(value, factorAAA, width)
            self.layout.aaa_value.setValue(value)
        self.Pigment_Display_Release("")

    def Pigment_RGB_1(self, case, value):
        width = self.layout.rgb_1_slider.width()
        if case == "50":
            min = self.layout.rgb_1_value.minimum()
            max = self.layout.rgb_1_value.maximum()
            half = (max-min)/2
            self.rgb_1_slider.Update(half, factorRGB, width)
            self.layout.rgb_1_value.setValue(half)
        elif case == "M1":
            channel = self.layout.rgb_1_value.value()
            self.rgb_1_slider.Update((channel-value), factorRGB, width)
            self.layout.rgb_1_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.rgb_1_value.value()
            self.rgb_1_slider.Update((channel+value), factorRGB, width)
            self.layout.rgb_1_value.setValue(channel+value)
        elif case == "KU":
            self.rgb_1_slider.Update(value, factorRGB, width)
            self.layout.rgb_1_value.setValue(value)
        elif case == "HEX":
            self.rgb_1_slider.Update(value, factorRGB, width)
            self.layout.rgb_1_value.setValue(value)
        self.Pigment_Display_Release("")
    def Pigment_RGB_2(self, case, value):
        width = self.layout.rgb_2_slider.width()
        if case == "50":
            min = self.layout.rgb_2_value.minimum()
            max = self.layout.rgb_2_value.maximum()
            half = (max-min)/2
            self.rgb_2_slider.Update(half, factorRGB, width)
            self.layout.rgb_2_value.setValue(half)
        elif case == "M1":
            channel = self.layout.rgb_2_value.value()
            self.rgb_2_slider.Update((channel-value), factorRGB, width)
            self.layout.rgb_2_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.rgb_2_value.value()
            self.rgb_2_slider.Update((channel+value), factorRGB, width)
            self.layout.rgb_2_value.setValue(channel+value)
        elif case == "KU":
            self.rgb_2_slider.Update(value, factorRGB, width)
            self.layout.rgb_2_value.setValue(value)
        elif case == "HEX":
            self.rgb_2_slider.Update(value, factorRGB, width)
            self.layout.rgb_2_value.setValue(value)
        self.Pigment_Display_Release("")
    def Pigment_RGB_3(self, case, value):
        width = self.layout.rgb_3_slider.width()
        if case == "50":
            min = self.layout.rgb_3_value.minimum()
            max = self.layout.rgb_3_value.maximum()
            half = (max-min)/2
            self.rgb_3_slider.Update(half, factorRGB, width)
            self.layout.rgb_3_value.setValue(half)
        elif case == "M1":
            channel = self.layout.rgb_3_value.value()
            self.rgb_3_slider.Update((channel-value), factorRGB, width)
            self.layout.rgb_3_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.rgb_3_value.value()
            self.rgb_3_slider.Update((channel+value), factorRGB, width)
            self.layout.rgb_3_value.setValue(channel+value)
        elif case == "KU":
            self.rgb_3_slider.Update(value, factorRGB, width)
            self.layout.rgb_3_value.setValue(value)
        elif case == "HEX":
            self.rgb_3_slider.Update(value, factorRGB, width)
            self.layout.rgb_3_value.setValue(value)
        self.Pigment_Display_Release("")

    def Pigment_HSV_1(self, case, value):
        width = self.layout.hsv_1_slider.width()
        if case == "50":
            hue = self.layout.hsv_1_value.value()
            if (hue >= 0 and hue <= 30):
                hue = 0
            elif (hue > 30 and hue <= 90):
                hue = 60
            elif (hue > 90 and hue <= 150):
                hue = 120
            elif (hue > 150 and hue <= 210):
                hue = 180
            elif (hue > 210 and hue <= 270):
                hue = 240
            elif (hue > 270 and hue <= 330):
                hue = 300
            elif (hue > 330 and hue <= 360):
                hue = 360
            self.hsv_1_slider.Update(hue, factorHUE, width)
            self.layout.hsv_1_value.setValue(hue)
        elif case == "M1":
            channel = self.layout.hsv_1_value.value()
            self.hsv_1_slider.Update((channel-value), factorHUE,  width)
            self.layout.hsv_1_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.hsv_1_value.value()
            self.hsv_1_slider.Update((channel+value), factorHUE, width)
            self.layout.hsv_1_value.setValue(channel+value)
        elif case == "KU":
            self.hsv_1_slider.Update(value, factorHUE, width)
            self.layout.hsv_1_value.setValue(value)
        elif case == "HEX":
            self.hsv_1_slider.Update(value, factorHUE, width)
            self.layout.hsv_1_value.setValue(value)
        self.Pigment_Display_Release("")
    def Pigment_HSV_2(self, case, value):
        width = self.layout.hsv_2_slider.width()
        if case == "50":
            min = self.layout.hsv_2_value.minimum()
            max = self.layout.hsv_2_value.maximum()
            half = (max-min)/2
            self.hsv_2_slider.Update(half, factorSVL, width)
            self.layout.hsv_2_value.setValue(half)
        elif case == "M1":
            channel = self.layout.hsv_2_value.value()
            self.hsv_2_slider.Update((channel-value), factorSVL, width)
            self.layout.hsv_2_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.hsv_2_value.value()
            self.hsv_2_slider.Update((channel+value), factorSVL, width)
            self.layout.hsv_2_value.setValue(channel+value)
        elif case == "KU":
            self.hsv_2_slider.Update(value, factorSVL, width)
            self.layout.hsv_2_value.setValue(value)
        elif case == "HEX":
            self.hsv_2_slider.Update(value, factorSVL, width)
            self.layout.hsv_2_value.setValue(value)
        self.Pigment_Display_Release("")
    def Pigment_HSV_3(self, case, value):
        width = self.layout.hsv_3_slider.width()
        if case == "50":
            min = self.layout.hsv_3_value.minimum()
            max = self.layout.hsv_3_value.maximum()
            half = (max-min)/2
            self.hsv_3_slider.Update(half, factorSVL, width)
            self.layout.hsv_3_value.setValue(half)
        elif case == "M1":
            channel = self.layout.hsv_3_value.value()
            self.hsv_3_slider.Update((channel-value), factorSVL, width)
            self.layout.hsv_3_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.hsv_3_value.value()
            self.hsv_3_slider.Update((channel+value), factorSVL, width)
            self.layout.hsv_3_value.setValue(channel+value)
        elif case == "KU":
            self.hsv_3_slider.Update(value, factorSVL, width)
            self.layout.hsv_3_value.setValue(value)
        elif case == "HEX":
            self.hsv_3_slider.Update(value, factorSVL, width)
            self.layout.hsv_3_value.setValue(value)
        self.Pigment_Display_Release("")

    def Pigment_HSL_1(self, case, value):
        width = self.layout.hsl_1_slider.width()
        if case == "50":
            hue = self.layout.hsl_1_value.value()
            if (hue >= 0 and hue <= 30):
                hue = 0
            elif (hue > 30 and hue <= 90):
                hue = 60
            elif (hue > 90 and hue <= 150):
                hue = 120
            elif (hue > 150 and hue <= 210):
                hue = 180
            elif (hue > 210 and hue <= 270):
                hue = 240
            elif (hue > 270 and hue <= 330):
                hue = 300
            elif (hue > 330 and hue <= 360):
                hue = 360
            self.hsl_1_slider.Update(hue, factorHUE, width)
            self.layout.hsl_1_value.setValue(hue)
        elif case == "M1":
            channel = self.layout.hsl_1_value.value()
            self.hsl_1_slider.Update((channel-value), factorHUE,  width)
            self.layout.hsl_1_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.hsl_1_value.value()
            self.hsl_1_slider.Update((channel+value), factorHUE, width)
            self.layout.hsl_1_value.setValue(channel+value)
        elif case == "KU":
            self.hsl_1_slider.Update(value, factorHUE, width)
            self.layout.hsl_1_value.setValue(value)
        elif case == "HEX":
            self.hsl_1_slider.Update(value, factorHUE, width)
            self.layout.hsl_1_value.setValue(value)
        self.Pigment_Display_Release("")
    def Pigment_HSL_2(self, case, value):
        width = self.layout.hsl_2_slider.width()
        if case == "50":
            min = self.layout.hsl_2_value.minimum()
            max = self.layout.hsl_2_value.maximum()
            half = (max-min)/2
            self.hsl_2_slider.Update(half, factorSVL, width)
            self.layout.hsl_2_value.setValue(half)
        elif case == "M1":
            channel = self.layout.hsl_2_value.value()
            self.hsl_2_slider.Update((channel-value), factorSVL, width)
            self.layout.hsl_2_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.hsl_2_value.value()
            self.hsl_2_slider.Update((channel+value), factorSVL, width)
            self.layout.hsl_2_value.setValue(channel+value)
        elif case == "KU":
            self.hsl_2_slider.Update(value, factorSVL, width)
            self.layout.hsl_2_value.setValue(value)
        elif case == "HEX":
            self.hsl_2_slider.Update(value, factorSVL, width)
            self.layout.hsl_2_value.setValue(value)
        self.Pigment_Display_Release("")
    def Pigment_HSL_3(self, case, value):
        width = self.layout.hsl_3_slider.width()
        if case == "50":
            min = self.layout.hsl_3_value.minimum()
            max = self.layout.hsl_3_value.maximum()
            half = (max-min)/2
            self.hsl_3_slider.Update(half, factorSVL, width)
            self.layout.hsl_3_value.setValue(half)
        elif case == "M1":
            channel = self.layout.hsl_3_value.value()
            self.hsl_3_slider.Update((channel-value), factorSVL, width)
            self.layout.hsl_3_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.hsl_3_value.value()
            self.hsl_3_slider.Update((channel+value), factorSVL, width)
            self.layout.hsl_3_value.setValue(channel+value)
        elif case == "KU":
            self.hsl_3_slider.Update(value, factorSVL, width)
            self.layout.hsl_3_value.setValue(value)
        elif case == "HEX":
            self.hsl_3_slider.Update(value, factorSVL, width)
            self.layout.hsl_3_value.setValue(value)
        self.Pigment_Display_Release("")

    def Pigment_CMYK_1(self, case, value):
        width = self.layout.cmyk_1_slider.width()
        if case == "50":
            min = self.layout.cmyk_1_value.minimum()
            max = self.layout.cmyk_1_value.maximum()
            half = (max-min)/2
            self.cmyk_1_slider.Update(half, factorCMYK, width)
            self.layout.cmyk_1_value.setValue(half)
        elif case == "M1":
            channel = self.layout.cmyk_1_value.value()
            self.cmyk_1_slider.Update((channel-value), factorCMYK,  width)
            self.layout.cmyk_1_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.cmyk_1_value.value()
            self.cmyk_1_slider.Update((channel+value), factorCMYK, width)
            self.layout.cmyk_1_value.setValue(channel+value)
        elif case == "KU":
            self.cmyk_1_slider.Update(value, factorCMYK, width)
            self.layout.cmyk_1_value.setValue(value)
        elif case == "HEX":
            self.cmyk_1_slider.Update(value, factorCMYK, width)
            self.layout.cmyk_1_value.setValue(value)
        self.Pigment_Display_Release("")
    def Pigment_CMYK_2(self, case, value):
        width = self.layout.cmyk_2_slider.width()
        if case == "50":
            min = self.layout.cmyk_2_value.minimum()
            max = self.layout.cmyk_2_value.maximum()
            half = (max-min)/2
            self.cmyk_2_slider.Update(half, factorCMYK, width)
            self.layout.cmyk_2_value.setValue(half)
        elif case == "M1":
            channel = self.layout.cmyk_2_value.value()
            self.cmyk_2_slider.Update((channel-value), factorCMYK, width)
            self.layout.cmyk_2_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.cmyk_2_value.value()
            self.cmyk_2_slider.Update((channel+value), factorCMYK, width)
            self.layout.cmyk_2_value.setValue(channel+value)
        elif case == "KU":
            self.cmyk_2_slider.Update(value, factorCMYK, width)
            self.layout.cmyk_2_value.setValue(value)
        elif case == "HEX":
            self.cmyk_2_slider.Update(value, factorCMYK, width)
            self.layout.cmyk_2_value.setValue(value)
        self.Pigment_Display_Release("")
    def Pigment_CMYK_3(self, case, value):
        width = self.layout.cmyk_3_slider.width()
        if case == "50":
            min = self.layout.cmyk_3_value.minimum()
            max = self.layout.cmyk_3_value.maximum()
            half = (max-min)/2
            self.cmyk_3_slider.Update(half, factorCMYK, width)
            self.layout.cmyk_3_value.setValue(half)
        elif case == "M1":
            channel = self.layout.cmyk_3_value.value()
            self.cmyk_3_slider.Update((channel-value), factorCMYK, width)
            self.layout.cmyk_3_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.cmyk_3_value.value()
            self.cmyk_3_slider.Update((channel+value), factorCMYK, width)
            self.layout.cmyk_3_value.setValue(channel+value)
        elif case == "KU":
            self.cmyk_3_slider.Update(value, factorCMYK, width)
            self.layout.cmyk_3_value.setValue(value)
        elif case == "HEX":
            self.cmyk_3_slider.Update(value, factorCMYK, width)
            self.layout.cmyk_3_value.setValue(value)
        self.Pigment_Display_Release("")
    def Pigment_CMYK_4(self, case, value):
        width = self.layout.cmyk_4_slider.width()
        if case == "50":
            min = self.layout.cmyk_4_value.minimum()
            max = self.layout.cmyk_4_value.maximum()
            half = (max-min)/2
            self.cmyk_4_slider.Update(half, factorCMYK, width)
            self.layout.cmyk_4_value.setValue(half)
        elif case == "M1":
            channel = self.layout.cmyk_4_value.value()
            self.cmyk_4_slider.Update((channel-value), factorCMYK, width)
            self.layout.cmyk_4_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.cmyk_4_value.value()
            self.cmyk_4_slider.Update((channel+value), factorCMYK, width)
            self.layout.cmyk_4_value.setValue(channel+value)
        elif case == "KU":
            self.cmyk_4_slider.Update(value, factorCMYK, width)
            self.layout.cmyk_4_value.setValue(value)
        elif case == "HEX":
            self.cmyk_4_slider.Update(value, factorCMYK, width)
            self.layout.cmyk_4_value.setValue(value)
        self.Pigment_Display_Release("")

    # Menu Displays
    def Display_AAA(self):
        font = self.layout.aaa.font()
        if self.layout.aaa.isChecked():
            font.setBold(True)
            self.layout.aaa_label.setMinimumHeight(cmin1)
            self.layout.aaa_label.setMaximumHeight(cmax1)
            self.layout.aaa_minus.setMinimumHeight(cmin1)
            self.layout.aaa_minus.setMaximumHeight(cmax1)
            self.layout.aaa_slider.setMinimumHeight(cmin1)
            self.layout.aaa_slider.setMaximumHeight(cmax1)
            self.layout.aaa_plus.setMinimumHeight(cmin1)
            self.layout.aaa_plus.setMaximumHeight(cmax1)
            self.layout.aaa_value.setMinimumHeight(cmin1)
            self.layout.aaa_value.setMaximumHeight(cmax1)
            self.layout.aaa_tick.setMinimumHeight(unit)
            # Place Percentage Style
            if (self.layout.aaa.isChecked() == True or
            self.layout.rgb.isChecked() == True or
            self.layout.hsv.isChecked() == True or
            self.layout.hsl.isChecked() == True or
            self.layout.cmyk.isChecked() == True):
                ten = self.style.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            font.setBold(False)
            self.layout.aaa_label.setMinimumHeight(null)
            self.layout.aaa_label.setMaximumHeight(null)
            self.layout.aaa_minus.setMinimumHeight(null)
            self.layout.aaa_minus.setMaximumHeight(null)
            self.layout.aaa_slider.setMinimumHeight(null)
            self.layout.aaa_slider.setMaximumHeight(null)
            self.layout.aaa_plus.setMinimumHeight(null)
            self.layout.aaa_plus.setMaximumHeight(null)
            self.layout.aaa_value.setMinimumHeight(null)
            self.layout.aaa_value.setMaximumHeight(null)
            self.layout.aaa_tick.setMinimumHeight(null)
            # Remove Percentage Style
            if (self.layout.aaa.isChecked() == False and
            self.layout.rgb.isChecked() == False and
            self.layout.hsv.isChecked() == False and
            self.layout.hsl.isChecked() == False and
            self.layout.cmyk.isChecked() == False):
                alpha = self.style.Alpha()
                self.layout.percentage_top.setStyleSheet(alpha)
                self.layout.percentage_bot.setStyleSheet(alpha)
        self.layout.aaa.setFont(font)
    def Display_RGB(self):
        font = self.layout.rgb.font()
        if self.layout.rgb.isChecked():
            font.setBold(True)
            self.layout.rgb_1_label.setMinimumHeight(cmin1)
            self.layout.rgb_1_label.setMaximumHeight(cmax1)
            self.layout.rgb_1_minus.setMinimumHeight(cmin1)
            self.layout.rgb_1_minus.setMaximumHeight(cmax1)
            self.layout.rgb_1_slider.setMinimumHeight(cmin1)
            self.layout.rgb_1_slider.setMaximumHeight(cmax1)
            self.layout.rgb_1_plus.setMinimumHeight(cmin1)
            self.layout.rgb_1_plus.setMaximumHeight(cmax1)
            self.layout.rgb_1_value.setMinimumHeight(cmin1)
            self.layout.rgb_1_value.setMaximumHeight(cmax1)
            self.layout.rgb_1_tick.setMinimumHeight(unit)
            self.layout.rgb_2_label.setMinimumHeight(cmin1)
            self.layout.rgb_2_label.setMaximumHeight(cmax1)
            self.layout.rgb_2_minus.setMinimumHeight(cmin1)
            self.layout.rgb_2_minus.setMaximumHeight(cmax1)
            self.layout.rgb_2_slider.setMinimumHeight(cmin1)
            self.layout.rgb_2_slider.setMaximumHeight(cmax1)
            self.layout.rgb_2_plus.setMinimumHeight(cmin1)
            self.layout.rgb_2_plus.setMaximumHeight(cmax1)
            self.layout.rgb_2_value.setMinimumHeight(cmin1)
            self.layout.rgb_2_value.setMaximumHeight(cmax1)
            self.layout.rgb_2_tick.setMinimumHeight(unit)
            self.layout.rgb_3_label.setMinimumHeight(cmin1)
            self.layout.rgb_3_label.setMaximumHeight(cmax1)
            self.layout.rgb_3_minus.setMinimumHeight(cmin1)
            self.layout.rgb_3_minus.setMaximumHeight(cmax1)
            self.layout.rgb_3_slider.setMinimumHeight(cmin1)
            self.layout.rgb_3_slider.setMaximumHeight(cmax1)
            self.layout.rgb_3_plus.setMinimumHeight(cmin1)
            self.layout.rgb_3_plus.setMaximumHeight(cmax1)
            self.layout.rgb_3_value.setMinimumHeight(cmin1)
            self.layout.rgb_3_value.setMaximumHeight(cmax1)
            self.layout.rgb_3_tick.setMinimumHeight(unit)
            # Place Percentage Style
            if (self.layout.aaa.isChecked() == True or
            self.layout.rgb.isChecked() == True or
            self.layout.hsv.isChecked() == True or
            self.layout.hsl.isChecked() == True or
            self.layout.cmyk.isChecked() == True):
                ten = self.style.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            font.setBold(False)
            self.layout.rgb_1_label.setMinimumHeight(null)
            self.layout.rgb_1_label.setMaximumHeight(null)
            self.layout.rgb_1_minus.setMinimumHeight(null)
            self.layout.rgb_1_minus.setMaximumHeight(null)
            self.layout.rgb_1_slider.setMinimumHeight(null)
            self.layout.rgb_1_slider.setMaximumHeight(null)
            self.layout.rgb_1_plus.setMinimumHeight(null)
            self.layout.rgb_1_plus.setMaximumHeight(null)
            self.layout.rgb_1_value.setMinimumHeight(null)
            self.layout.rgb_1_value.setMaximumHeight(null)
            self.layout.rgb_1_tick.setMinimumHeight(null)
            self.layout.rgb_2_label.setMinimumHeight(null)
            self.layout.rgb_2_label.setMaximumHeight(null)
            self.layout.rgb_2_minus.setMinimumHeight(null)
            self.layout.rgb_2_minus.setMaximumHeight(null)
            self.layout.rgb_2_slider.setMinimumHeight(null)
            self.layout.rgb_2_slider.setMaximumHeight(null)
            self.layout.rgb_2_plus.setMinimumHeight(null)
            self.layout.rgb_2_plus.setMaximumHeight(null)
            self.layout.rgb_2_value.setMinimumHeight(null)
            self.layout.rgb_2_value.setMaximumHeight(null)
            self.layout.rgb_2_tick.setMinimumHeight(null)
            self.layout.rgb_3_label.setMinimumHeight(null)
            self.layout.rgb_3_label.setMaximumHeight(null)
            self.layout.rgb_3_minus.setMinimumHeight(null)
            self.layout.rgb_3_minus.setMaximumHeight(null)
            self.layout.rgb_3_slider.setMinimumHeight(null)
            self.layout.rgb_3_slider.setMaximumHeight(null)
            self.layout.rgb_3_plus.setMinimumHeight(null)
            self.layout.rgb_3_plus.setMaximumHeight(null)
            self.layout.rgb_3_value.setMinimumHeight(null)
            self.layout.rgb_3_value.setMaximumHeight(null)
            self.layout.rgb_3_tick.setMinimumHeight(null)
            # Remove Percentage Style
            if (self.layout.aaa.isChecked() == False and
            self.layout.rgb.isChecked() == False and
            self.layout.hsv.isChecked() == False and
            self.layout.hsl.isChecked() == False and
            self.layout.cmyk.isChecked() == False):
                alpha = self.style.Alpha()
                self.layout.percentage_top.setStyleSheet(alpha)
                self.layout.percentage_bot.setStyleSheet(alpha)
        self.layout.rgb.setFont(font)
    def Display_HSV(self):
        font = self.layout.hsv.font()
        if self.layout.hsv.isChecked():
            font.setBold(True)
            self.layout.hsv_1_label.setMinimumHeight(cmin1)
            self.layout.hsv_1_label.setMaximumHeight(cmax1)
            self.layout.hsv_1_minus.setMinimumHeight(cmin1)
            self.layout.hsv_1_minus.setMaximumHeight(cmax1)
            self.layout.hsv_1_slider.setMinimumHeight(cmin1)
            self.layout.hsv_1_slider.setMaximumHeight(cmax1)
            self.layout.hsv_1_plus.setMinimumHeight(cmin1)
            self.layout.hsv_1_plus.setMaximumHeight(cmax1)
            self.layout.hsv_1_value.setMinimumHeight(cmin1)
            self.layout.hsv_1_value.setMaximumHeight(cmax1)
            self.layout.hsv_1_tick.setMinimumHeight(unit)
            self.layout.hsv_2_label.setMinimumHeight(cmin1)
            self.layout.hsv_2_label.setMaximumHeight(cmax1)
            self.layout.hsv_2_minus.setMinimumHeight(cmin1)
            self.layout.hsv_2_minus.setMaximumHeight(cmax1)
            self.layout.hsv_2_slider.setMinimumHeight(cmin1)
            self.layout.hsv_2_slider.setMaximumHeight(cmax1)
            self.layout.hsv_2_plus.setMinimumHeight(cmin1)
            self.layout.hsv_2_plus.setMaximumHeight(cmax1)
            self.layout.hsv_2_value.setMinimumHeight(cmin1)
            self.layout.hsv_2_value.setMaximumHeight(cmax1)
            self.layout.hsv_2_tick.setMinimumHeight(unit)
            self.layout.hsv_3_label.setMinimumHeight(cmin1)
            self.layout.hsv_3_label.setMaximumHeight(cmax1)
            self.layout.hsv_3_minus.setMinimumHeight(cmin1)
            self.layout.hsv_3_minus.setMaximumHeight(cmax1)
            self.layout.hsv_3_slider.setMinimumHeight(cmin1)
            self.layout.hsv_3_slider.setMaximumHeight(cmax1)
            self.layout.hsv_3_plus.setMinimumHeight(cmin1)
            self.layout.hsv_3_plus.setMaximumHeight(cmax1)
            self.layout.hsv_3_value.setMinimumHeight(cmin1)
            self.layout.hsv_3_value.setMaximumHeight(cmax1)
            self.layout.hsv_3_tick.setMinimumHeight(unit)
            # Place Percetage Style
            if (self.layout.aaa.isChecked() == True or
            self.layout.rgb.isChecked() == True or
            self.layout.hsv.isChecked() == True or
            self.layout.hsl.isChecked() == True or
            self.layout.cmyk.isChecked() == True):
                ten = self.style.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            font.setBold(False)
            self.layout.hsv_1_label.setMinimumHeight(null)
            self.layout.hsv_1_label.setMaximumHeight(null)
            self.layout.hsv_1_minus.setMinimumHeight(null)
            self.layout.hsv_1_minus.setMaximumHeight(null)
            self.layout.hsv_1_slider.setMinimumHeight(null)
            self.layout.hsv_1_slider.setMaximumHeight(null)
            self.layout.hsv_1_plus.setMinimumHeight(null)
            self.layout.hsv_1_plus.setMaximumHeight(null)
            self.layout.hsv_1_value.setMinimumHeight(null)
            self.layout.hsv_1_value.setMaximumHeight(null)
            self.layout.hsv_1_tick.setMinimumHeight(null)
            self.layout.hsv_2_label.setMinimumHeight(null)
            self.layout.hsv_2_label.setMaximumHeight(null)
            self.layout.hsv_2_minus.setMinimumHeight(null)
            self.layout.hsv_2_minus.setMaximumHeight(null)
            self.layout.hsv_2_slider.setMinimumHeight(null)
            self.layout.hsv_2_slider.setMaximumHeight(null)
            self.layout.hsv_2_plus.setMinimumHeight(null)
            self.layout.hsv_2_plus.setMaximumHeight(null)
            self.layout.hsv_2_value.setMinimumHeight(null)
            self.layout.hsv_2_value.setMaximumHeight(null)
            self.layout.hsv_2_tick.setMinimumHeight(null)
            self.layout.hsv_3_label.setMinimumHeight(null)
            self.layout.hsv_3_label.setMaximumHeight(null)
            self.layout.hsv_3_minus.setMinimumHeight(null)
            self.layout.hsv_3_minus.setMaximumHeight(null)
            self.layout.hsv_3_slider.setMinimumHeight(null)
            self.layout.hsv_3_slider.setMaximumHeight(null)
            self.layout.hsv_3_plus.setMinimumHeight(null)
            self.layout.hsv_3_plus.setMaximumHeight(null)
            self.layout.hsv_3_value.setMinimumHeight(null)
            self.layout.hsv_3_value.setMaximumHeight(null)
            self.layout.hsv_3_tick.setMinimumHeight(null)
            # Remove Percentage Style
            if (self.layout.aaa.isChecked() == False and
            self.layout.rgb.isChecked() == False and
            self.layout.hsv.isChecked() == False and
            self.layout.hsl.isChecked() == False and
            self.layout.cmyk.isChecked() == False):
                alpha = self.style.Alpha()
                self.layout.percentage_top.setStyleSheet(alpha)
                self.layout.percentage_bot.setStyleSheet(alpha)
        self.layout.hsv.setFont(font)
    def Display_HSL(self):
        font = self.layout.hsl.font()
        if self.layout.hsl.isChecked():
            font.setBold(True)
            self.layout.hsl_1_label.setMinimumHeight(cmin1)
            self.layout.hsl_1_label.setMaximumHeight(cmax1)
            self.layout.hsl_1_minus.setMinimumHeight(cmin1)
            self.layout.hsl_1_minus.setMaximumHeight(cmax1)
            self.layout.hsl_1_slider.setMinimumHeight(cmin1)
            self.layout.hsl_1_slider.setMaximumHeight(cmax1)
            self.layout.hsl_1_plus.setMinimumHeight(cmin1)
            self.layout.hsl_1_plus.setMaximumHeight(cmax1)
            self.layout.hsl_1_value.setMinimumHeight(cmin1)
            self.layout.hsl_1_value.setMaximumHeight(cmax1)
            self.layout.hsl_1_tick.setMinimumHeight(unit)
            self.layout.hsl_2_label.setMinimumHeight(cmin1)
            self.layout.hsl_2_label.setMaximumHeight(cmax1)
            self.layout.hsl_2_minus.setMinimumHeight(cmin1)
            self.layout.hsl_2_minus.setMaximumHeight(cmax1)
            self.layout.hsl_2_slider.setMinimumHeight(cmin1)
            self.layout.hsl_2_slider.setMaximumHeight(cmax1)
            self.layout.hsl_2_plus.setMinimumHeight(cmin1)
            self.layout.hsl_2_plus.setMaximumHeight(cmax1)
            self.layout.hsl_2_value.setMinimumHeight(cmin1)
            self.layout.hsl_2_value.setMaximumHeight(cmax1)
            self.layout.hsl_2_tick.setMinimumHeight(unit)
            self.layout.hsl_3_label.setMinimumHeight(cmin1)
            self.layout.hsl_3_label.setMaximumHeight(cmax1)
            self.layout.hsl_3_minus.setMinimumHeight(cmin1)
            self.layout.hsl_3_minus.setMaximumHeight(cmax1)
            self.layout.hsl_3_slider.setMinimumHeight(cmin1)
            self.layout.hsl_3_slider.setMaximumHeight(cmax1)
            self.layout.hsl_3_plus.setMinimumHeight(cmin1)
            self.layout.hsl_3_plus.setMaximumHeight(cmax1)
            self.layout.hsl_3_value.setMinimumHeight(cmin1)
            self.layout.hsl_3_value.setMaximumHeight(cmax1)
            self.layout.hsl_3_tick.setMinimumHeight(unit)
            # Place Percetage Style
            if (self.layout.aaa.isChecked() == True or
            self.layout.rgb.isChecked() == True or
            self.layout.hsv.isChecked() == True or
            self.layout.hsl.isChecked() == True or
            self.layout.cmyk.isChecked() == True):
                ten = self.style.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            font.setBold(False)
            self.layout.hsl_1_label.setMinimumHeight(null)
            self.layout.hsl_1_label.setMaximumHeight(null)
            self.layout.hsl_1_minus.setMinimumHeight(null)
            self.layout.hsl_1_minus.setMaximumHeight(null)
            self.layout.hsl_1_slider.setMinimumHeight(null)
            self.layout.hsl_1_slider.setMaximumHeight(null)
            self.layout.hsl_1_plus.setMinimumHeight(null)
            self.layout.hsl_1_plus.setMaximumHeight(null)
            self.layout.hsl_1_value.setMinimumHeight(null)
            self.layout.hsl_1_value.setMaximumHeight(null)
            self.layout.hsl_1_tick.setMinimumHeight(null)
            self.layout.hsl_2_label.setMinimumHeight(null)
            self.layout.hsl_2_label.setMaximumHeight(null)
            self.layout.hsl_2_minus.setMinimumHeight(null)
            self.layout.hsl_2_minus.setMaximumHeight(null)
            self.layout.hsl_2_slider.setMinimumHeight(null)
            self.layout.hsl_2_slider.setMaximumHeight(null)
            self.layout.hsl_2_plus.setMinimumHeight(null)
            self.layout.hsl_2_plus.setMaximumHeight(null)
            self.layout.hsl_2_value.setMinimumHeight(null)
            self.layout.hsl_2_value.setMaximumHeight(null)
            self.layout.hsl_2_tick.setMinimumHeight(null)
            self.layout.hsl_3_label.setMinimumHeight(null)
            self.layout.hsl_3_label.setMaximumHeight(null)
            self.layout.hsl_3_minus.setMinimumHeight(null)
            self.layout.hsl_3_minus.setMaximumHeight(null)
            self.layout.hsl_3_slider.setMinimumHeight(null)
            self.layout.hsl_3_slider.setMaximumHeight(null)
            self.layout.hsl_3_plus.setMinimumHeight(null)
            self.layout.hsl_3_plus.setMaximumHeight(null)
            self.layout.hsl_3_value.setMinimumHeight(null)
            self.layout.hsl_3_value.setMaximumHeight(null)
            self.layout.hsl_3_tick.setMinimumHeight(null)
            # Remove Percentage Style
            if (self.layout.aaa.isChecked() == False and
            self.layout.rgb.isChecked() == False and
            self.layout.hsv.isChecked() == False and
            self.layout.hsl.isChecked() == False and
            self.layout.cmyk.isChecked() == False):
                alpha = self.style.Alpha()
                self.layout.percentage_top.setStyleSheet(alpha)
                self.layout.percentage_bot.setStyleSheet(alpha)
        self.layout.hsl.setFont(font)
    def Display_CMYK(self):
        font = self.layout.cmyk.font()
        if self.layout.cmyk.isChecked():
            font.setBold(True)
            self.layout.cmyk_1_label.setMinimumHeight(cmin1)
            self.layout.cmyk_1_label.setMaximumHeight(cmax1)
            self.layout.cmyk_1_minus.setMinimumHeight(cmin1)
            self.layout.cmyk_1_minus.setMaximumHeight(cmax1)
            self.layout.cmyk_1_slider.setMinimumHeight(cmin1)
            self.layout.cmyk_1_slider.setMaximumHeight(cmax1)
            self.layout.cmyk_1_plus.setMinimumHeight(cmin1)
            self.layout.cmyk_1_plus.setMaximumHeight(cmax1)
            self.layout.cmyk_1_value.setMinimumHeight(cmin1)
            self.layout.cmyk_1_value.setMaximumHeight(cmax1)
            self.layout.cmyk_1_tick.setMinimumHeight(unit)
            self.layout.cmyk_2_label.setMinimumHeight(cmin1)
            self.layout.cmyk_2_label.setMaximumHeight(cmax1)
            self.layout.cmyk_2_minus.setMinimumHeight(cmin1)
            self.layout.cmyk_2_minus.setMaximumHeight(cmax1)
            self.layout.cmyk_2_slider.setMinimumHeight(cmin1)
            self.layout.cmyk_2_slider.setMaximumHeight(cmax1)
            self.layout.cmyk_2_plus.setMinimumHeight(cmin1)
            self.layout.cmyk_2_plus.setMaximumHeight(cmax1)
            self.layout.cmyk_2_value.setMinimumHeight(cmin1)
            self.layout.cmyk_2_value.setMaximumHeight(cmax1)
            self.layout.cmyk_2_tick.setMinimumHeight(unit)
            self.layout.cmyk_3_label.setMinimumHeight(cmin1)
            self.layout.cmyk_3_label.setMaximumHeight(cmax1)
            self.layout.cmyk_3_minus.setMinimumHeight(cmin1)
            self.layout.cmyk_3_minus.setMaximumHeight(cmax1)
            self.layout.cmyk_3_slider.setMinimumHeight(cmin1)
            self.layout.cmyk_3_slider.setMaximumHeight(cmax1)
            self.layout.cmyk_3_plus.setMinimumHeight(cmin1)
            self.layout.cmyk_3_plus.setMaximumHeight(cmax1)
            self.layout.cmyk_3_value.setMinimumHeight(cmin1)
            self.layout.cmyk_3_value.setMaximumHeight(cmax1)
            self.layout.cmyk_3_tick.setMinimumHeight(unit)
            self.layout.cmyk_4_label.setMinimumHeight(cmin1)
            self.layout.cmyk_4_label.setMaximumHeight(cmax1)
            self.layout.cmyk_4_minus.setMinimumHeight(cmin1)
            self.layout.cmyk_4_minus.setMaximumHeight(cmax1)
            self.layout.cmyk_4_slider.setMinimumHeight(cmin1)
            self.layout.cmyk_4_slider.setMaximumHeight(cmax1)
            self.layout.cmyk_4_plus.setMinimumHeight(cmin1)
            self.layout.cmyk_4_plus.setMaximumHeight(cmax1)
            self.layout.cmyk_4_value.setMinimumHeight(cmin1)
            self.layout.cmyk_4_value.setMaximumHeight(cmax1)
            self.layout.cmyk_4_tick.setMinimumHeight(unit)
            # Place Percetage Style
            if (self.layout.aaa.isChecked() == True or
            self.layout.rgb.isChecked() == True or
            self.layout.hsv.isChecked() == True or
            self.layout.hsl.isChecked() == True or
            self.layout.cmyk.isChecked() == True):
                ten = self.style.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            font.setBold(False)
            self.layout.cmyk_1_label.setMinimumHeight(null)
            self.layout.cmyk_1_label.setMaximumHeight(null)
            self.layout.cmyk_1_minus.setMinimumHeight(null)
            self.layout.cmyk_1_minus.setMaximumHeight(null)
            self.layout.cmyk_1_slider.setMinimumHeight(null)
            self.layout.cmyk_1_slider.setMaximumHeight(null)
            self.layout.cmyk_1_plus.setMinimumHeight(null)
            self.layout.cmyk_1_plus.setMaximumHeight(null)
            self.layout.cmyk_1_value.setMinimumHeight(null)
            self.layout.cmyk_1_value.setMaximumHeight(null)
            self.layout.cmyk_1_tick.setMinimumHeight(null)
            self.layout.cmyk_2_label.setMinimumHeight(null)
            self.layout.cmyk_2_label.setMaximumHeight(null)
            self.layout.cmyk_2_minus.setMinimumHeight(null)
            self.layout.cmyk_2_minus.setMaximumHeight(null)
            self.layout.cmyk_2_slider.setMinimumHeight(null)
            self.layout.cmyk_2_slider.setMaximumHeight(null)
            self.layout.cmyk_2_plus.setMinimumHeight(null)
            self.layout.cmyk_2_plus.setMaximumHeight(null)
            self.layout.cmyk_2_value.setMinimumHeight(null)
            self.layout.cmyk_2_value.setMaximumHeight(null)
            self.layout.cmyk_2_tick.setMinimumHeight(null)
            self.layout.cmyk_3_label.setMinimumHeight(null)
            self.layout.cmyk_3_label.setMaximumHeight(null)
            self.layout.cmyk_3_minus.setMinimumHeight(null)
            self.layout.cmyk_3_minus.setMaximumHeight(null)
            self.layout.cmyk_3_slider.setMinimumHeight(null)
            self.layout.cmyk_3_slider.setMaximumHeight(null)
            self.layout.cmyk_3_plus.setMinimumHeight(null)
            self.layout.cmyk_3_plus.setMaximumHeight(null)
            self.layout.cmyk_3_value.setMinimumHeight(null)
            self.layout.cmyk_3_value.setMaximumHeight(null)
            self.layout.cmyk_3_tick.setMinimumHeight(null)
            self.layout.cmyk_4_label.setMinimumHeight(null)
            self.layout.cmyk_4_label.setMaximumHeight(null)
            self.layout.cmyk_4_minus.setMinimumHeight(null)
            self.layout.cmyk_4_minus.setMaximumHeight(null)
            self.layout.cmyk_4_slider.setMinimumHeight(null)
            self.layout.cmyk_4_slider.setMaximumHeight(null)
            self.layout.cmyk_4_plus.setMinimumHeight(null)
            self.layout.cmyk_4_plus.setMaximumHeight(null)
            self.layout.cmyk_4_value.setMinimumHeight(null)
            self.layout.cmyk_4_value.setMaximumHeight(null)
            self.layout.cmyk_4_tick.setMinimumHeight(null)
            # Remove Percentage Style
            if (self.layout.aaa.isChecked() == False and
            self.layout.rgb.isChecked() == False and
            self.layout.hsv.isChecked() == False and
            self.layout.hsl.isChecked() == False and
            self.layout.cmyk.isChecked() == False):
                alpha = self.style.Alpha()
                self.layout.percentage_top.setStyleSheet(alpha)
                self.layout.percentage_bot.setStyleSheet(alpha)
        self.layout.cmyk.setFont(font)

    def Display_Cores(self):
        font = self.layout.tip.font()
        if self.layout.tip.isChecked():
            font.setBold(True)
            self.layout.tip_00.setMinimumHeight(tipmm)
            self.layout.tip_00.setMaximumHeight(tipmm)
            self.layout.line.setMinimumHeight(tipmm)
            self.layout.line.setMaximumHeight(tipmm)
            self.layout.cor_01.setMinimumHeight(tipmm)
            self.layout.cor_01.setMaximumHeight(tipmm)
            self.layout.cor_02.setMinimumHeight(tipmm)
            self.layout.cor_02.setMaximumHeight(tipmm)
            self.layout.cor_03.setMinimumHeight(tipmm)
            self.layout.cor_03.setMaximumHeight(tipmm)
            self.layout.cor_04.setMinimumHeight(tipmm)
            self.layout.cor_04.setMaximumHeight(tipmm)
            self.layout.cor_05.setMinimumHeight(tipmm)
            self.layout.cor_05.setMaximumHeight(tipmm)
            self.layout.cor_06.setMinimumHeight(tipmm)
            self.layout.cor_06.setMaximumHeight(tipmm)
            self.layout.cor_07.setMinimumHeight(tipmm)
            self.layout.cor_07.setMaximumHeight(tipmm)
            self.layout.cor_08.setMinimumHeight(tipmm)
            self.layout.cor_08.setMaximumHeight(tipmm)
            self.layout.cor_09.setMinimumHeight(tipmm)
            self.layout.cor_09.setMaximumHeight(tipmm)
            self.layout.cor_10.setMinimumHeight(tipmm)
            self.layout.cor_10.setMaximumHeight(tipmm)
            self.layout.cores.setContentsMargins(0, vspacer, 0, margin)
        else:
            font.setBold(False)
            self.layout.tip_00.setMinimumHeight(null)
            self.layout.tip_00.setMaximumHeight(null)
            self.layout.line.setMinimumHeight(null)
            self.layout.line.setMaximumHeight(null)
            self.layout.cor_01.setMinimumHeight(null)
            self.layout.cor_01.setMaximumHeight(null)
            self.layout.cor_02.setMinimumHeight(null)
            self.layout.cor_02.setMaximumHeight(null)
            self.layout.cor_03.setMinimumHeight(null)
            self.layout.cor_03.setMaximumHeight(null)
            self.layout.cor_04.setMinimumHeight(null)
            self.layout.cor_04.setMaximumHeight(null)
            self.layout.cor_05.setMinimumHeight(null)
            self.layout.cor_05.setMaximumHeight(null)
            self.layout.cor_06.setMinimumHeight(null)
            self.layout.cor_06.setMaximumHeight(null)
            self.layout.cor_07.setMinimumHeight(null)
            self.layout.cor_07.setMaximumHeight(null)
            self.layout.cor_08.setMinimumHeight(null)
            self.layout.cor_08.setMaximumHeight(null)
            self.layout.cor_09.setMinimumHeight(null)
            self.layout.cor_09.setMaximumHeight(null)
            self.layout.cor_10.setMinimumHeight(null)
            self.layout.cor_10.setMaximumHeight(null)
            self.layout.cores.setContentsMargins(0, null, 0, null)
        self.layout.tip.setFont(font)
    def Display_TTS(self):
        font = self.layout.tts.font()
        if self.layout.tts.isChecked():
            font.setBold(True)
            self.layout.neutral.setMinimumHeight(cmin3)
            self.layout.neutral.setMaximumHeight(cmax3)
            self.layout.tint.setMinimumHeight(cmin2)
            self.layout.tint.setMaximumHeight(cmax2)
            self.layout.tone.setMinimumHeight(cmin2)
            self.layout.tone.setMaximumHeight(cmax2)
            self.layout.shade.setMinimumHeight(cmin2)
            self.layout.shade.setMaximumHeight(cmax2)
            self.layout.white.setMinimumHeight(cmin2)
            self.layout.white.setMaximumHeight(cmax2)
            self.layout.grey.setMinimumHeight(cmin2)
            self.layout.grey.setMaximumHeight(cmax2)
            self.layout.black.setMinimumHeight(cmin2)
            self.layout.black.setMaximumHeight(cmax2)
            self.layout.spacer_tts_1.setMinimumHeight(cmin2)
            self.layout.spacer_tts_1.setMaximumHeight(cmax2)
            self.layout.spacer_tts_2.setMinimumHeight(cmin2)
            self.layout.spacer_tts_2.setMaximumHeight(cmax2)
            self.layout.spacer_tts_3.setMinimumHeight(cmin2)
            self.layout.spacer_tts_3.setMaximumHeight(cmax2)
            self.layout.spacer_tts_4.setMinimumHeight(cmin2)
            self.layout.spacer_tts_4.setMaximumHeight(cmax2)
            self.layout.percentage_tts_1.setMinimumHeight(vspacer)
            self.layout.percentage_tts_1.setMaximumHeight(vspacer)
            self.layout.percentage_tts_2.setMinimumHeight(vspacer)
            self.layout.percentage_tts_2.setMaximumHeight(vspacer)
            self.layout.tint_tone_shade.setContentsMargins(0, 0, 0, margin)
        else:
            font.setBold(False)
            self.layout.neutral.setMinimumHeight(null)
            self.layout.neutral.setMaximumHeight(null)
            self.layout.tint.setMinimumHeight(null)
            self.layout.tint.setMaximumHeight(null)
            self.layout.tone.setMinimumHeight(null)
            self.layout.tone.setMaximumHeight(null)
            self.layout.shade.setMinimumHeight(null)
            self.layout.shade.setMaximumHeight(null)
            self.layout.white.setMinimumHeight(null)
            self.layout.white.setMaximumHeight(null)
            self.layout.grey.setMinimumHeight(null)
            self.layout.grey.setMaximumHeight(null)
            self.layout.black.setMinimumHeight(null)
            self.layout.black.setMaximumHeight(null)
            self.layout.spacer_tts_1.setMinimumHeight(null)
            self.layout.spacer_tts_1.setMaximumHeight(null)
            self.layout.spacer_tts_2.setMinimumHeight(null)
            self.layout.spacer_tts_2.setMaximumHeight(null)
            self.layout.spacer_tts_3.setMinimumHeight(null)
            self.layout.spacer_tts_3.setMaximumHeight(null)
            self.layout.spacer_tts_4.setMinimumHeight(null)
            self.layout.spacer_tts_4.setMaximumHeight(null)
            self.layout.percentage_tts_1.setMinimumHeight(null)
            self.layout.percentage_tts_1.setMaximumHeight(null)
            self.layout.percentage_tts_2.setMinimumHeight(null)
            self.layout.percentage_tts_2.setMaximumHeight(null)
            self.layout.tint_tone_shade.setContentsMargins(0, 0, 0, null)
        self.layout.tts.setFont(font)
    def Display_Mixer(self):
        mixer = self.layout.mixer_selector.currentText()
        self.Mixer_Shrink()
        if mixer == "MIX":
            pass
        elif mixer == "RGB":
            self.layout.rgb_l1.setMinimumHeight(cmin2)
            self.layout.rgb_l1.setMaximumHeight(cmax2)
            self.layout.rgb_l2.setMinimumHeight(cmin2)
            self.layout.rgb_l2.setMaximumHeight(cmax2)
            self.layout.rgb_l3.setMinimumHeight(cmin2)
            self.layout.rgb_l3.setMaximumHeight(cmax2)
            self.layout.rgb_r1.setMinimumHeight(cmin2)
            self.layout.rgb_r1.setMaximumHeight(cmax2)
            self.layout.rgb_r2.setMinimumHeight(cmin2)
            self.layout.rgb_r2.setMaximumHeight(cmax2)
            self.layout.rgb_r3.setMinimumHeight(cmin2)
            self.layout.rgb_r3.setMaximumHeight(cmax2)
            self.layout.rgb_g1.setMinimumHeight(cmin2)
            self.layout.rgb_g1.setMaximumHeight(cmax2)
            self.layout.rgb_g2.setMinimumHeight(cmin2)
            self.layout.rgb_g2.setMaximumHeight(cmax2)
            self.layout.rgb_g3.setMinimumHeight(cmin2)
            self.layout.rgb_g3.setMaximumHeight(cmax2)
            self.layout.spacer_rgb_1.setMinimumHeight(cmin2)
            self.layout.spacer_rgb_1.setMaximumHeight(cmax2)
            self.layout.spacer_rgb_2.setMinimumHeight(cmin2)
            self.layout.spacer_rgb_2.setMaximumHeight(cmax2)
            self.layout.spacer_rgb_3.setMinimumHeight(cmin2)
            self.layout.spacer_rgb_3.setMaximumHeight(cmax2)
            self.layout.spacer_rgb_4.setMinimumHeight(cmin2)
            self.layout.spacer_rgb_4.setMaximumHeight(cmax2)
            self.layout.percentage_rgb_1.setMinimumHeight(vspacer)
            self.layout.percentage_rgb_1.setMaximumHeight(vspacer)
            self.layout.percentage_rgb_2.setMinimumHeight(vspacer)
            self.layout.percentage_rgb_2.setMaximumHeight(vspacer)
            self.layout.mixer_rgb.setContentsMargins(0, 0, 0, margin)
        elif mixer == "HSV":
            self.layout.hsv_l1.setMinimumHeight(cmin2)
            self.layout.hsv_l1.setMaximumHeight(cmax2)
            self.layout.hsv_l2.setMinimumHeight(cmin2)
            self.layout.hsv_l2.setMaximumHeight(cmax2)
            self.layout.hsv_l3.setMinimumHeight(cmin2)
            self.layout.hsv_l3.setMaximumHeight(cmax2)
            self.layout.hsv_r1.setMinimumHeight(cmin2)
            self.layout.hsv_r1.setMaximumHeight(cmax2)
            self.layout.hsv_r2.setMinimumHeight(cmin2)
            self.layout.hsv_r2.setMaximumHeight(cmax2)
            self.layout.hsv_r3.setMinimumHeight(cmin2)
            self.layout.hsv_r3.setMaximumHeight(cmax2)
            self.layout.hsv_g1.setMinimumHeight(cmin2)
            self.layout.hsv_g1.setMaximumHeight(cmax2)
            self.layout.hsv_g2.setMinimumHeight(cmin2)
            self.layout.hsv_g2.setMaximumHeight(cmax2)
            self.layout.hsv_g3.setMinimumHeight(cmin2)
            self.layout.hsv_g3.setMaximumHeight(cmax2)
            self.layout.spacer_hsv_1.setMinimumHeight(cmin2)
            self.layout.spacer_hsv_1.setMaximumHeight(cmax2)
            self.layout.spacer_hsv_2.setMinimumHeight(cmin2)
            self.layout.spacer_hsv_2.setMaximumHeight(cmax2)
            self.layout.spacer_hsv_3.setMinimumHeight(cmin2)
            self.layout.spacer_hsv_3.setMaximumHeight(cmax2)
            self.layout.spacer_hsv_4.setMinimumHeight(cmin2)
            self.layout.spacer_hsv_4.setMaximumHeight(cmax2)
            self.layout.percentage_hsv_1.setMinimumHeight(vspacer)
            self.layout.percentage_hsv_1.setMaximumHeight(vspacer)
            self.layout.percentage_hsv_2.setMinimumHeight(vspacer)
            self.layout.percentage_hsv_2.setMaximumHeight(vspacer)
            self.layout.mixer_hsv.setContentsMargins(0, 0, 0, margin)
        elif mixer == "HSL":
            self.layout.hsl_l1.setMinimumHeight(cmin2)
            self.layout.hsl_l1.setMaximumHeight(cmax2)
            self.layout.hsl_l2.setMinimumHeight(cmin2)
            self.layout.hsl_l2.setMaximumHeight(cmax2)
            self.layout.hsl_l3.setMinimumHeight(cmin2)
            self.layout.hsl_l3.setMaximumHeight(cmax2)
            self.layout.hsl_r1.setMinimumHeight(cmin2)
            self.layout.hsl_r1.setMaximumHeight(cmax2)
            self.layout.hsl_r2.setMinimumHeight(cmin2)
            self.layout.hsl_r2.setMaximumHeight(cmax2)
            self.layout.hsl_r3.setMinimumHeight(cmin2)
            self.layout.hsl_r3.setMaximumHeight(cmax2)
            self.layout.hsl_g1.setMinimumHeight(cmin2)
            self.layout.hsl_g1.setMaximumHeight(cmax2)
            self.layout.hsl_g2.setMinimumHeight(cmin2)
            self.layout.hsl_g2.setMaximumHeight(cmax2)
            self.layout.hsl_g3.setMinimumHeight(cmin2)
            self.layout.hsl_g3.setMaximumHeight(cmax2)
            self.layout.spacer_hsl_1.setMinimumHeight(cmin2)
            self.layout.spacer_hsl_1.setMaximumHeight(cmax2)
            self.layout.spacer_hsl_2.setMinimumHeight(cmin2)
            self.layout.spacer_hsl_2.setMaximumHeight(cmax2)
            self.layout.spacer_hsl_3.setMinimumHeight(cmin2)
            self.layout.spacer_hsl_3.setMaximumHeight(cmax2)
            self.layout.spacer_hsl_4.setMinimumHeight(cmin2)
            self.layout.spacer_hsl_4.setMaximumHeight(cmax2)
            self.layout.percentage_hsl_1.setMinimumHeight(vspacer)
            self.layout.percentage_hsl_1.setMaximumHeight(vspacer)
            self.layout.percentage_hsl_2.setMinimumHeight(vspacer)
            self.layout.percentage_hsl_2.setMaximumHeight(vspacer)
            self.layout.mixer_hsl.setContentsMargins(0, 0, 0, margin)
        elif mixer == "CMYK":
            self.layout.cmyk_l1.setMinimumHeight(cmin2)
            self.layout.cmyk_l1.setMaximumHeight(cmax2)
            self.layout.cmyk_l2.setMinimumHeight(cmin2)
            self.layout.cmyk_l2.setMaximumHeight(cmax2)
            self.layout.cmyk_l3.setMinimumHeight(cmin2)
            self.layout.cmyk_l3.setMaximumHeight(cmax2)
            self.layout.cmyk_r1.setMinimumHeight(cmin2)
            self.layout.cmyk_r1.setMaximumHeight(cmax2)
            self.layout.cmyk_r2.setMinimumHeight(cmin2)
            self.layout.cmyk_r2.setMaximumHeight(cmax2)
            self.layout.cmyk_r3.setMinimumHeight(cmin2)
            self.layout.cmyk_r3.setMaximumHeight(cmax2)
            self.layout.cmyk_g1.setMinimumHeight(cmin2)
            self.layout.cmyk_g1.setMaximumHeight(cmax2)
            self.layout.cmyk_g2.setMinimumHeight(cmin2)
            self.layout.cmyk_g2.setMaximumHeight(cmax2)
            self.layout.cmyk_g3.setMinimumHeight(cmin2)
            self.layout.cmyk_g3.setMaximumHeight(cmax2)
            self.layout.spacer_cmyk_1.setMinimumHeight(cmin2)
            self.layout.spacer_cmyk_1.setMaximumHeight(cmax2)
            self.layout.spacer_cmyk_2.setMinimumHeight(cmin2)
            self.layout.spacer_cmyk_2.setMaximumHeight(cmax2)
            self.layout.spacer_cmyk_3.setMinimumHeight(cmin2)
            self.layout.spacer_cmyk_3.setMaximumHeight(cmax2)
            self.layout.spacer_cmyk_4.setMinimumHeight(cmin2)
            self.layout.spacer_cmyk_4.setMaximumHeight(cmax2)
            self.layout.percentage_cmyk_1.setMinimumHeight(vspacer)
            self.layout.percentage_cmyk_1.setMaximumHeight(vspacer)
            self.layout.percentage_cmyk_2.setMinimumHeight(vspacer)
            self.layout.percentage_cmyk_2.setMaximumHeight(vspacer)
            self.layout.mixer_cmyk.setContentsMargins(0, 0, 0, margin)
    def Mixer_Shrink(self):
        # Mix RGB
        self.layout.rgb_l1.setMinimumHeight(null)
        self.layout.rgb_l1.setMaximumHeight(null)
        self.layout.rgb_l2.setMinimumHeight(null)
        self.layout.rgb_l2.setMaximumHeight(null)
        self.layout.rgb_l3.setMinimumHeight(null)
        self.layout.rgb_l3.setMaximumHeight(null)
        self.layout.rgb_r1.setMinimumHeight(null)
        self.layout.rgb_r1.setMaximumHeight(null)
        self.layout.rgb_r2.setMinimumHeight(null)
        self.layout.rgb_r2.setMaximumHeight(null)
        self.layout.rgb_r3.setMinimumHeight(null)
        self.layout.rgb_r3.setMaximumHeight(null)
        self.layout.rgb_g1.setMinimumHeight(null)
        self.layout.rgb_g1.setMaximumHeight(null)
        self.layout.rgb_g2.setMinimumHeight(null)
        self.layout.rgb_g2.setMaximumHeight(null)
        self.layout.rgb_g3.setMinimumHeight(null)
        self.layout.rgb_g3.setMaximumHeight(null)
        self.layout.spacer_rgb_1.setMinimumHeight(null)
        self.layout.spacer_rgb_1.setMaximumHeight(null)
        self.layout.spacer_rgb_2.setMinimumHeight(null)
        self.layout.spacer_rgb_2.setMaximumHeight(null)
        self.layout.spacer_rgb_3.setMinimumHeight(null)
        self.layout.spacer_rgb_3.setMaximumHeight(null)
        self.layout.spacer_rgb_4.setMinimumHeight(null)
        self.layout.spacer_rgb_4.setMaximumHeight(null)
        self.layout.percentage_rgb_1.setMinimumHeight(null)
        self.layout.percentage_rgb_1.setMaximumHeight(null)
        self.layout.percentage_rgb_2.setMinimumHeight(null)
        self.layout.percentage_rgb_2.setMaximumHeight(null)
        self.layout.mixer_rgb.setContentsMargins(0, 0, 0, null)
        # Mix HSV
        self.layout.hsv_l1.setMinimumHeight(null)
        self.layout.hsv_l1.setMaximumHeight(null)
        self.layout.hsv_l2.setMinimumHeight(null)
        self.layout.hsv_l2.setMaximumHeight(null)
        self.layout.hsv_l3.setMinimumHeight(null)
        self.layout.hsv_l3.setMaximumHeight(null)
        self.layout.hsv_r1.setMinimumHeight(null)
        self.layout.hsv_r1.setMaximumHeight(null)
        self.layout.hsv_r2.setMinimumHeight(null)
        self.layout.hsv_r2.setMaximumHeight(null)
        self.layout.hsv_r3.setMinimumHeight(null)
        self.layout.hsv_r3.setMaximumHeight(null)
        self.layout.hsv_g1.setMinimumHeight(null)
        self.layout.hsv_g1.setMaximumHeight(null)
        self.layout.hsv_g2.setMinimumHeight(null)
        self.layout.hsv_g2.setMaximumHeight(null)
        self.layout.hsv_g3.setMinimumHeight(null)
        self.layout.hsv_g3.setMaximumHeight(null)
        self.layout.spacer_hsv_1.setMinimumHeight(null)
        self.layout.spacer_hsv_1.setMaximumHeight(null)
        self.layout.spacer_hsv_2.setMinimumHeight(null)
        self.layout.spacer_hsv_2.setMaximumHeight(null)
        self.layout.spacer_hsv_3.setMinimumHeight(null)
        self.layout.spacer_hsv_3.setMaximumHeight(null)
        self.layout.spacer_hsv_4.setMinimumHeight(null)
        self.layout.spacer_hsv_4.setMaximumHeight(null)
        self.layout.percentage_hsv_1.setMinimumHeight(null)
        self.layout.percentage_hsv_1.setMaximumHeight(null)
        self.layout.percentage_hsv_2.setMinimumHeight(null)
        self.layout.percentage_hsv_2.setMaximumHeight(null)
        self.layout.mixer_hsv.setContentsMargins(0, 0, 0, null)
        # Mix HSL
        self.layout.hsl_l1.setMinimumHeight(null)
        self.layout.hsl_l1.setMaximumHeight(null)
        self.layout.hsl_l2.setMinimumHeight(null)
        self.layout.hsl_l2.setMaximumHeight(null)
        self.layout.hsl_l3.setMinimumHeight(null)
        self.layout.hsl_l3.setMaximumHeight(null)
        self.layout.hsl_r1.setMinimumHeight(null)
        self.layout.hsl_r1.setMaximumHeight(null)
        self.layout.hsl_r2.setMinimumHeight(null)
        self.layout.hsl_r2.setMaximumHeight(null)
        self.layout.hsl_r3.setMinimumHeight(null)
        self.layout.hsl_r3.setMaximumHeight(null)
        self.layout.hsl_g1.setMinimumHeight(null)
        self.layout.hsl_g1.setMaximumHeight(null)
        self.layout.hsl_g2.setMinimumHeight(null)
        self.layout.hsl_g2.setMaximumHeight(null)
        self.layout.hsl_g3.setMinimumHeight(null)
        self.layout.hsl_g3.setMaximumHeight(null)
        self.layout.spacer_hsl_1.setMinimumHeight(null)
        self.layout.spacer_hsl_1.setMaximumHeight(null)
        self.layout.spacer_hsl_2.setMinimumHeight(null)
        self.layout.spacer_hsl_2.setMaximumHeight(null)
        self.layout.spacer_hsl_3.setMinimumHeight(null)
        self.layout.spacer_hsl_3.setMaximumHeight(null)
        self.layout.spacer_hsl_4.setMinimumHeight(null)
        self.layout.spacer_hsl_4.setMaximumHeight(null)
        self.layout.percentage_hsl_1.setMinimumHeight(null)
        self.layout.percentage_hsl_1.setMaximumHeight(null)
        self.layout.percentage_hsl_2.setMinimumHeight(null)
        self.layout.percentage_hsl_2.setMaximumHeight(null)
        self.layout.mixer_hsl.setContentsMargins(0, 0, 0, null)
        # Mix CMYK
        self.layout.cmyk_l1.setMinimumHeight(null)
        self.layout.cmyk_l1.setMaximumHeight(null)
        self.layout.cmyk_l2.setMinimumHeight(null)
        self.layout.cmyk_l2.setMaximumHeight(null)
        self.layout.cmyk_l3.setMinimumHeight(null)
        self.layout.cmyk_l3.setMaximumHeight(null)
        self.layout.cmyk_r1.setMinimumHeight(null)
        self.layout.cmyk_r1.setMaximumHeight(null)
        self.layout.cmyk_r2.setMinimumHeight(null)
        self.layout.cmyk_r2.setMaximumHeight(null)
        self.layout.cmyk_r3.setMinimumHeight(null)
        self.layout.cmyk_r3.setMaximumHeight(null)
        self.layout.cmyk_g1.setMinimumHeight(null)
        self.layout.cmyk_g1.setMaximumHeight(null)
        self.layout.cmyk_g2.setMinimumHeight(null)
        self.layout.cmyk_g2.setMaximumHeight(null)
        self.layout.cmyk_g3.setMinimumHeight(null)
        self.layout.cmyk_g3.setMaximumHeight(null)
        self.layout.spacer_cmyk_1.setMinimumHeight(null)
        self.layout.spacer_cmyk_1.setMaximumHeight(null)
        self.layout.spacer_cmyk_2.setMinimumHeight(null)
        self.layout.spacer_cmyk_2.setMaximumHeight(null)
        self.layout.spacer_cmyk_3.setMinimumHeight(null)
        self.layout.spacer_cmyk_3.setMaximumHeight(null)
        self.layout.spacer_cmyk_4.setMinimumHeight(null)
        self.layout.spacer_cmyk_4.setMaximumHeight(null)
        self.layout.percentage_cmyk_1.setMinimumHeight(null)
        self.layout.percentage_cmyk_1.setMaximumHeight(null)
        self.layout.percentage_cmyk_2.setMinimumHeight(null)
        self.layout.percentage_cmyk_2.setMaximumHeight(null)
        self.layout.mixer_cmyk.setContentsMargins(0, 0, 0, null)
    def Display_Panel(self):
        panel = self.layout.panel_selector.currentText()
        if panel == "PANEL":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            # Expanding
        elif panel == "HSV":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.Pigment_Color("HSV")
        elif panel == "HSV0":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.Pigment_Color("HSV")
        elif panel == "HSL":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Color("HSL")
        elif panel == "HSL0":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Color("HSL")

    # Palette
    def Color_01(self, SIGNAL_CLICKS):
        if SIGNAL_CLICKS == "APPLY":
            self.Color_Apply(self.color_01)
        elif SIGNAL_CLICKS == "SAVE":
            self.color_01 = [self.layout.rgb_1_value.value()/factorRGB, self.layout.rgb_2_value.value()/factorRGB, self.layout.rgb_3_value.value()/factorRGB]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_01[0]*factorRGB, self.color_01[1]*factorRGB, self.color_01[2]*factorRGB))
            self.layout.cor_01.setStyleSheet(color)
        elif SIGNAL_CLICKS == "CLEAN":
            self.color_01 = self.Neutral_Colors()
            black = str("background-color: rgba(0, 0, 0, 50); ")
            self.layout.cor_01.setStyleSheet(black)
    def Color_02(self, SIGNAL_CLICKS):
        if SIGNAL_CLICKS == "APPLY":
            self.Color_Apply(self.color_02)
        elif SIGNAL_CLICKS == "SAVE":
            self.color_02 = [self.layout.rgb_1_value.value()/factorRGB, self.layout.rgb_2_value.value()/factorRGB, self.layout.rgb_3_value.value()/factorRGB]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_02[0]*factorRGB, self.color_02[1]*factorRGB, self.color_02[2]*factorRGB))
            self.layout.cor_02.setStyleSheet(color)
        elif SIGNAL_CLICKS == "CLEAN":
            self.color_02 = self.Neutral_Colors()
            black = str("background-color: rgba(0, 0, 0, 50); ")
            self.layout.cor_02.setStyleSheet(black)
    def Color_03(self, SIGNAL_CLICKS):
        if SIGNAL_CLICKS == "APPLY":
            self.Color_Apply(self.color_03)
        elif SIGNAL_CLICKS == "SAVE":
            self.color_03 = [self.layout.rgb_1_value.value()/factorRGB, self.layout.rgb_2_value.value()/factorRGB, self.layout.rgb_3_value.value()/factorRGB]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_03[0]*factorRGB, self.color_03[1]*factorRGB, self.color_03[2]*factorRGB))
            self.layout.cor_03.setStyleSheet(color)
        elif SIGNAL_CLICKS == "CLEAN":
            self.color_03 = self.Neutral_Colors()
            black = str("background-color: rgba(0, 0, 0, 50); ")
            self.layout.cor_03.setStyleSheet(black)
    def Color_04(self, SIGNAL_CLICKS):
        if SIGNAL_CLICKS == "APPLY":
            self.Color_Apply(self.color_04)
        elif SIGNAL_CLICKS == "SAVE":
            self.color_04 = [self.layout.rgb_1_value.value()/factorRGB, self.layout.rgb_2_value.value()/factorRGB, self.layout.rgb_3_value.value()/factorRGB]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_04[0]*factorRGB, self.color_04[1]*factorRGB, self.color_04[2]*factorRGB))
            self.layout.cor_04.setStyleSheet(color)
        elif SIGNAL_CLICKS == "CLEAN":
            self.color_04 = self.Neutral_Colors()
            black = str("background-color: rgba(0, 0, 0, 50); ")
            self.layout.cor_04.setStyleSheet(black)
    def Color_05(self, SIGNAL_CLICKS):
        if SIGNAL_CLICKS == "APPLY":
            self.Color_Apply(self.color_05)
        elif SIGNAL_CLICKS == "SAVE":
            self.color_05 = [self.layout.rgb_1_value.value()/factorRGB, self.layout.rgb_2_value.value()/factorRGB, self.layout.rgb_3_value.value()/factorRGB]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_05[0]*factorRGB, self.color_05[1]*factorRGB, self.color_05[2]*factorRGB))
            self.layout.cor_05.setStyleSheet(color)
        elif SIGNAL_CLICKS == "CLEAN":
            self.color_05 = self.Neutral_Colors()
            black = str("background-color: rgba(0, 0, 0, 50); ")
            self.layout.cor_05.setStyleSheet(black)
    def Color_06(self, SIGNAL_CLICKS):
        if SIGNAL_CLICKS == "APPLY":
            self.Color_Apply(self.color_06)
        elif SIGNAL_CLICKS == "SAVE":
            self.color_06 = [self.layout.rgb_1_value.value()/factorRGB, self.layout.rgb_2_value.value()/factorRGB, self.layout.rgb_3_value.value()/factorRGB]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_06[0]*factorRGB, self.color_06[1]*factorRGB, self.color_06[2]*factorRGB))
            self.layout.cor_06.setStyleSheet(color)
        elif SIGNAL_CLICKS == "CLEAN":
            self.color_06 = self.Neutral_Colors()
            black = str("background-color: rgba(0, 0, 0, 50); ")
            self.layout.cor_06.setStyleSheet(black)
    def Color_07(self, SIGNAL_CLICKS):
        if SIGNAL_CLICKS == "APPLY":
            self.Color_Apply(self.color_07)
        elif SIGNAL_CLICKS == "SAVE":
            self.color_07 = [self.layout.rgb_1_value.value()/factorRGB, self.layout.rgb_2_value.value()/factorRGB, self.layout.rgb_3_value.value()/factorRGB]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_07[0]*factorRGB, self.color_07[1]*factorRGB, self.color_07[2]*factorRGB))
            self.layout.cor_07.setStyleSheet(color)
        elif SIGNAL_CLICKS == "CLEAN":
            self.color_07 = self.Neutral_Colors()
            black = str("background-color: rgba(0, 0, 0, 50); ")
            self.layout.cor_07.setStyleSheet(black)
    def Color_08(self, SIGNAL_CLICKS):
        if SIGNAL_CLICKS == "APPLY":
            self.Color_Apply(self.color_08)
        elif SIGNAL_CLICKS == "SAVE":
            self.color_08 = [self.layout.rgb_1_value.value()/factorRGB, self.layout.rgb_2_value.value()/factorRGB, self.layout.rgb_3_value.value()/factorRGB]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_08[0]*factorRGB, self.color_08[1]*factorRGB, self.color_08[2]*factorRGB))
            self.layout.cor_08.setStyleSheet(color)
        elif SIGNAL_CLICKS == "CLEAN":
            self.color_08 = self.Neutral_Colors()
            black = str("background-color: rgba(0, 0, 0, 50); ")
            self.layout.cor_08.setStyleSheet(black)
    def Color_09(self, SIGNAL_CLICKS):
        if SIGNAL_CLICKS == "APPLY":
            self.Color_Apply(self.color_09)
        elif SIGNAL_CLICKS == "SAVE":
            self.color_09 = [self.layout.rgb_1_value.value()/factorRGB, self.layout.rgb_2_value.value()/factorRGB, self.layout.rgb_3_value.value()/factorRGB]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_09[0]*factorRGB, self.color_09[1]*factorRGB, self.color_09[2]*factorRGB))
            self.layout.cor_09.setStyleSheet(color)
        elif SIGNAL_CLICKS == "CLEAN":
            self.color_09 = self.Neutral_Colors()
            black = str("background-color: rgba(0, 0, 0, 50); ")
            self.layout.cor_09.setStyleSheet(black)
    def Color_10(self, SIGNAL_CLICKS):
        if SIGNAL_CLICKS == "APPLY":
            self.Color_Apply(self.color_10)
        elif SIGNAL_CLICKS == "SAVE":
            self.color_10 = [self.layout.rgb_1_value.value()/factorRGB, self.layout.rgb_2_value.value()/factorRGB, self.layout.rgb_3_value.value()/factorRGB]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_10[0]*factorRGB, self.color_10[1]*factorRGB, self.color_10[2]*factorRGB))
            self.layout.cor_10.setStyleSheet(color)
        elif SIGNAL_CLICKS == "CLEAN":
            self.color_10 = self.Neutral_Colors()
            black = str("background-color: rgba(0, 0, 0, 50); ")
            self.layout.cor_10.setStyleSheet(black)

    def Color_Apply(self, rgb):
        hsv = self.convert.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsl = self.convert.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        cmyk = self.convert.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # to AAA
        aaa = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        rgb1 = rgb[0]
        rgb2 = rgb[1]
        rgb3 = rgb[2]
        # to HSV
        hsv1 = hsv[0]
        hsv2 = hsv[1]
        hsv3 = hsv[2]
        # to HSL
        hsl1 = hsl[0]
        hsl2 = hsl[1]
        hsl3 = hsl[2]
        # to CMYK
        cmyk1 = cmyk[0]
        cmyk2 = cmyk[1]
        cmyk3 = cmyk[2]
        cmyk4 = cmyk[3]
        # Pigment Update Values
        self.Pigment_Sync("MIX", aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
        self.Pigment_2_Krita(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
        self.Pigment_Display(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
        self.Pigment_Display_Release("")

    # Mixer
    def Mixer_Neutral(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_neutral = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;"  % (self.color_neutral[1], self.color_neutral[2], self.color_neutral[3]))
            white = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_white[1], self.color_white[2], self.color_white[3]))
            grey = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_grey[1], self.color_grey[2], self.color_grey[3]))
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            self.layout.neutral.setStyleSheet(color)
            self.layout.white.setStyleSheet(white)
            self.layout.grey.setStyleSheet(grey)
            self.layout.black.setStyleSheet(black)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_neutral = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 0); border: 1px solid rgba(56, 56, 56, 255) ;")
            self.layout.neutral.setStyleSheet(black)
            self.layout.white.setStyleSheet(alpha)
            self.layout.grey.setStyleSheet(alpha)
            self.layout.black.setStyleSheet(alpha)
            self.layout.tint.setStyleSheet(alpha)
            self.layout.tone.setStyleSheet(alpha)
            self.layout.shade.setStyleSheet(alpha)
            # Correct Values
            self.percentage_tint = 0
            self.percentage_tone = 0
            self.percentage_shade = 0
            self.mixer_tint.Update(self.percentage_tint, self.layout.tint.width())
            self.mixer_tone.Update(self.percentage_tone, self.layout.tone.width())
            self.mixer_shade.Update(self.percentage_shade, self.layout.shade.width())

    def Mixer_RGB_L1(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_rgb_l1 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l1[1], self.color_rgb_l1[2], self.color_rgb_l1[3]))
            self.layout.rgb_l1.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_rgb_l1 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgba(%f, %f, %f,255); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.rgb_l1.setStyleSheet(black)
            self.layout.rgb_g1.setStyleSheet(alpha)
            # Correct Values
            self.percentage_rgb_g1 = 0
            self.mixer_rgb_g1.Update(self.percentage_rgb_g1, self.layout.rgb_g1.width())
    def Mixer_RGB_L2(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_rgb_l2 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l2[1], self.color_rgb_l2[2], self.color_rgb_l2[3]))
            self.layout.rgb_l2.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_rgb_l2 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.rgb_l2.setStyleSheet(black)
            self.layout.rgb_g2.setStyleSheet(alpha)
            # Correct Values
            self.percentage_rgb_g2 = 0
            self.mixer_rgb_g2.Update(self.percentage_rgb_g2, self.layout.rgb_g2.width())
    def Mixer_RGB_L3(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_rgb_l3 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l3[1], self.color_rgb_l3[2], self.color_rgb_l3[3]))
            self.layout.rgb_l3.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_rgb_l3 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.rgb_l3.setStyleSheet(black)
            self.layout.rgb_g3.setStyleSheet(alpha)
            # Correct Values
            self.percentage_rgb_g3 = 0
            self.mixer_rgb_g3.Update(self.percentage_rgb_g3, self.layout.rgb_g3.width())
    def Mixer_RGB_R1(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_rgb_r1 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r1[1], self.color_rgb_r1[2], self.color_rgb_r1[3]))
            self.layout.rgb_r1.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_rgb_r1 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.rgb_r1.setStyleSheet(black)
            self.layout.rgb_g1.setStyleSheet(alpha)
            # Correct Values
            self.percentage_rgb_g1 = 0
            self.mixer_rgb_g1.Update(self.percentage_rgb_g1, self.layout.rgb_g1.width())
    def Mixer_RGB_R2(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_rgb_r2 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r2[1], self.color_rgb_r2[2], self.color_rgb_r2[3]))
            self.layout.rgb_r2.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_rgb_r2 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.rgb_r2.setStyleSheet(black)
            self.layout.rgb_g2.setStyleSheet(alpha)
            # Correct Values
            self.percentage_rgb_g2 = 0
            self.mixer_rgb_g2.Update(self.percentage_rgb_g2, self.layout.rgb_g2.width())
    def Mixer_RGB_R3(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_rgb_r3 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r3[1], self.color_rgb_r3[2], self.color_rgb_r3[3]))
            self.layout.rgb_r3.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_rgb_r3 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.rgb_r3.setStyleSheet(black)
            self.layout.rgb_g3.setStyleSheet(alpha)
            # Correct Values
            self.percentage_rgb_g3 = 0
            self.mixer_rgb_g3.Update(self.percentage_rgb_g3, self.layout.rgb_g3.width())

    def Mixer_HSV_L1(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsv_l1 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_l1[1], self.color_hsv_l1[2], self.color_hsv_l1[3]))
            self.layout.hsv_l1.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_hsv_l1 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.hsv_l1.setStyleSheet(black)
            self.layout.hsv_g1.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsv_g1 = 0
            self.mixer_hsv_g1.Update(self.percentage_hsv_g1, self.layout.hsv_g1.width())
    def Mixer_HSV_L2(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsv_l2 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_l2[1], self.color_hsv_l2[2], self.color_hsv_l2[3]))
            self.layout.hsv_l2.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_hsv_l2 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.hsv_l2.setStyleSheet(black)
            self.layout.hsv_g2.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsv_g2 = 0
            self.mixer_hsv_g2.Update(self.percentage_hsv_g2, self.layout.hsv_g2.width())
    def Mixer_HSV_L3(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsv_l3 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_l3[1], self.color_hsv_l3[2], self.color_hsv_l3[3]))
            self.layout.hsv_l3.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_hsv_l3 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.hsv_l3.setStyleSheet(black)
            self.layout.hsv_g3.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsv_g3 = 0
            self.mixer_hsv_g3.Update(self.percentage_hsv_g3, self.layout.hsv_g3.width())
    def Mixer_HSV_R1(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsv_r1 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_r1[1], self.color_hsv_r1[2], self.color_hsv_r1[3]))
            self.layout.hsv_r1.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_hsv_r1 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.hsv_r1.setStyleSheet(black)
            self.layout.hsv_g1.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsv_g1 = 0
            self.mixer_hsv_g1.Update(self.percentage_hsv_g1, self.layout.hsv_g1.width())
    def Mixer_HSV_R2(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsv_r2 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_r2[1], self.color_hsv_r2[2], self.color_hsv_r2[3]))
            self.layout.hsv_r2.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_hsv_r2 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.hsv_r2.setStyleSheet(black)
            self.layout.hsv_g2.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsv_g2 = 0
            self.mixer_hsv_g2.Update(self.percentage_hsv_g2, self.layout.hsv_g2.width())
    def Mixer_HSV_R3(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsv_r3 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_r3[1], self.color_hsv_r3[2], self.color_hsv_r3[3]))
            self.layout.hsv_r3.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_hsv_r3 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.hsv_r3.setStyleSheet(black)
            self.layout.hsv_g3.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsv_g3 = 0
            self.mixer_hsv_g3.Update(self.percentage_hsv_g3, self.layout.hsv_g3.width())

    def Mixer_HSL_L1(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsl_l1 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_l1[1], self.color_hsl_l1[2], self.color_hsl_l1[3]))
            self.layout.hsl_l1.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_hsl_l1 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.hsl_l1.setStyleSheet(black)
            self.layout.hsl_g1.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsl_g1 = 0
            self.mixer_hsl_g1.Update(self.percentage_hsl_g1, self.layout.hsl_g1.width())
    def Mixer_HSL_L2(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsl_l2 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_l2[1], self.color_hsl_l2[2], self.color_hsl_l2[3]))
            self.layout.hsl_l2.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_hsl_l2 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.hsl_l2.setStyleSheet(black)
            self.layout.hsl_g2.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsl_g2 = 0
            self.mixer_hsl_g2.Update(self.percentage_hsl_g2, self.layout.hsl_g2.width())
    def Mixer_HSL_L3(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsl_l3 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_l3[1], self.color_hsl_l3[2], self.color_hsl_l3[3]))
            self.layout.hsl_l3.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_hsl_l3 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.hsl_l3.setStyleSheet(black)
            self.layout.hsl_g3.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsl_g3 = 0
            self.mixer_hsl_g3.Update(self.percentage_hsl_g3, self.layout.hsl_g3.width())
    def Mixer_HSL_R1(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsl_r1 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_r1[1], self.color_hsl_r1[2], self.color_hsl_r1[3]))
            self.layout.hsl_r1.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_hsl_r1 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.hsl_r1.setStyleSheet(black)
            self.layout.hsl_g1.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsl_g1 = 0
            self.mixer_hsl_g1.Update(self.percentage_hsl_g1, self.layout.hsl_g1.width())
    def Mixer_HSL_R2(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsl_r2 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_r2[1], self.color_hsl_r2[2], self.color_hsl_r2[3]))
            self.layout.hsl_r2.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_hsl_r2 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.hsl_r2.setStyleSheet(black)
            self.layout.hsl_g2.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsl_g2 = 0
            self.mixer_hsl_g2.Update(self.percentage_hsl_g2, self.layout.hsl_g2.width())
    def Mixer_HSL_R3(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsl_r3 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_r3[1], self.color_hsl_r3[2], self.color_hsl_r3[3]))
            self.layout.hsl_r3.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_hsl_r3 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.hsl_r3.setStyleSheet(black)
            self.layout.hsl_g3.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsl_g3 = 0
            self.mixer_hsl_g3.Update(self.percentage_hsl_g3, self.layout.hsl_g3.width())

    def Mixer_CMYK_L1(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_cmyk_l1 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_l1[1], self.color_cmyk_l1[2], self.color_cmyk_l1[3]))
            self.layout.cmyk_l1.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_cmyk_l1 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.cmyk_l1.setStyleSheet(black)
            self.layout.cmyk_g1.setStyleSheet(alpha)
            # Correct Values
            self.percentage_cmyk_g1 = 0
            self.mixer_cmyk_g1.Update(self.percentage_cmyk_g1, self.layout.cmyk_g1.width())
    def Mixer_CMYK_L2(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_cmyk_l2 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_l2[1], self.color_cmyk_l2[2], self.color_cmyk_l2[3]))
            self.layout.cmyk_l2.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_cmyk_l2 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.cmyk_l2.setStyleSheet(black)
            self.layout.cmyk_g2.setStyleSheet(alpha)
            # Correct Values
            self.percentage_cmyk_g2 = 0
            self.mixer_cmyk_g2.Update(self.percentage_cmyk_g2, self.layout.cmyk_g2.width())
    def Mixer_CMYK_L3(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_cmyk_l3 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_l3[1], self.color_cmyk_l3[2], self.color_cmyk_l3[3]))
            self.layout.cmyk_l3.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_cmyk_l3 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.cmyk_l3.setStyleSheet(black)
            self.layout.cmyk_g3.setStyleSheet(alpha)
            # Correct Values
            self.percentage_cmyk_g3 = 0
            self.mixer_cmyk_g3.Update(self.percentage_cmyk_g3, self.layout.cmyk_g3.width())
    def Mixer_CMYK_R1(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_cmyk_r1 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_r1[1], self.color_cmyk_r1[2], self.color_cmyk_r1[3]))
            self.layout.cmyk_r1.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_cmyk_r1 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.cmyk_r1.setStyleSheet(black)
            self.layout.cmyk_g1.setStyleSheet(alpha)
            # Correct Values
            self.percentage_cmyk_g1 = 0
            self.mixer_cmyk_g1.Update(self.percentage_cmyk_g1, self.layout.cmyk_g1.width())
    def Mixer_CMYK_R2(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_cmyk_r2 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_r2[1], self.color_cmyk_r2[2], self.color_cmyk_r2[3]))
            self.layout.cmyk_r2.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_cmyk_r2 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.cmyk_r2.setStyleSheet(black)
            self.layout.cmyk_g2.setStyleSheet(alpha)
            # Correct Values
            self.percentage_cmyk_g2 = 0
            self.mixer_cmyk_g2.Update(self.percentage_cmyk_g2, self.layout.cmyk_g2.width())
    def Mixer_CMYK_R3(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_cmyk_r3 = self.Current_Colors()
            # Display
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_r3[1], self.color_cmyk_r3[2], self.color_cmyk_r3[3]))
            self.layout.cmyk_r3.setStyleSheet(color)
            self.Mixer_Display()
        else:
            # Color Math
            self.color_cmyk_r3 = self.Neutral_Colors()
            # Display
            black = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_black[1], self.color_black[2], self.color_black[3]))
            alpha = str("background-color: rgba(0, 0, 0, 50);")
            self.layout.cmyk_r3.setStyleSheet(black)
            self.layout.cmyk_g3.setStyleSheet(alpha)
            # Correct Values
            self.percentage_cmyk_g3 = 0
            self.mixer_cmyk_g3.Update(self.percentage_cmyk_g3, self.layout.cmyk_g3.width())

    def Mixer_Tint(self, SIGNAL_MIXER_GRADIENT):
        # Percentage Value
        self.percentage_tint = SIGNAL_MIXER_GRADIENT / (self.layout.tint.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = ((self.color_neutral[1]) + (self.percentage_tint * (self.color_white[1] - self.color_neutral[1]))) / factorRGB
        rgb2 = ((self.color_neutral[2]) + (self.percentage_tint * (self.color_white[2] - self.color_neutral[2]))) / factorRGB
        rgb3 = ((self.color_neutral[3]) + (self.percentage_tint * (self.color_white[3] - self.color_neutral[3]))) / factorRGB
        # Converts
        rgb = [rgb1, rgb2, rgb3]
        hsv = self.convert.rgb_to_hsv(rgb1, rgb2, rgb3)
        hsl = self.convert.rgb_to_hsl(rgb1, rgb2, rgb3)
        cmyk = self.convert.rgb_to_cmyk(rgb1, rgb2, rgb3)
        # Send Values
        self.Mixer_Color(rgb, hsv, hsl, cmyk)
    def Mixer_Tone(self, SIGNAL_MIXER_GRADIENT):
        # Percentage Value
        self.percentage_tone = SIGNAL_MIXER_GRADIENT / (self.layout.tone.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = ((self.color_neutral[1]) + (self.percentage_tone * (self.color_grey[1] - self.color_neutral[1]))) / factorRGB
        rgb2 = ((self.color_neutral[2]) + (self.percentage_tone * (self.color_grey[2] - self.color_neutral[2]))) / factorRGB
        rgb3 = ((self.color_neutral[3]) + (self.percentage_tone * (self.color_grey[3] - self.color_neutral[3]))) / factorRGB
        # Converts
        rgb = [rgb1, rgb2, rgb3]
        hsv = self.convert.rgb_to_hsv(rgb1, rgb2, rgb3)
        hsl = self.convert.rgb_to_hsl(rgb1, rgb2, rgb3)
        cmyk = self.convert.rgb_to_cmyk(rgb1, rgb2, rgb3)
        # Send Values
        self.Mixer_Color(rgb, hsv, hsl, cmyk)
    def Mixer_Shade(self, SIGNAL_MIXER_GRADIENT):
        # Percentage Value
        self.percentage_shade = SIGNAL_MIXER_GRADIENT / (self.layout.shade.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = ((self.color_neutral[1]) + (self.percentage_shade * (self.color_black[1] - self.color_neutral[1]))) / factorRGB
        rgb2 = ((self.color_neutral[2]) + (self.percentage_shade * (self.color_black[2] - self.color_neutral[2]))) / factorRGB
        rgb3 = ((self.color_neutral[3]) + (self.percentage_shade * (self.color_black[3] - self.color_neutral[3]))) / factorRGB
        # Converts
        rgb = [rgb1, rgb2, rgb3]
        hsv = self.convert.rgb_to_hsv(rgb1, rgb2, rgb3)
        hsl = self.convert.rgb_to_hsl(rgb1, rgb2, rgb3)
        cmyk = self.convert.rgb_to_cmyk(rgb1, rgb2, rgb3)
        # Send Values
        self.Mixer_Color(rgb, hsv, hsl, cmyk)

    def Mixer_RGB_G1(self, SIGNAL_MIXER_GRADIENT):
        # Percentage Value
        self.percentage_rgb_g1 = SIGNAL_MIXER_GRADIENT / (self.layout.rgb_g1.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = (self.color_rgb_l1[1] + (self.percentage_rgb_g1 * (self.color_rgb_r1[1] - self.color_rgb_l1[1]))) / factorRGB
        rgb2 = (self.color_rgb_l1[2] + (self.percentage_rgb_g1 * (self.color_rgb_r1[2] - self.color_rgb_l1[2]))) / factorRGB
        rgb3 = (self.color_rgb_l1[3] + (self.percentage_rgb_g1 * (self.color_rgb_r1[3] - self.color_rgb_l1[3]))) / factorRGB
        # Converts
        rgb = [rgb1, rgb2, rgb3]
        hsv = self.convert.rgb_to_hsv(rgb1, rgb2, rgb3)
        hsl = self.convert.rgb_to_hsl(rgb1, rgb2, rgb3)
        cmyk = self.convert.rgb_to_cmyk(rgb1, rgb2, rgb3)
        # Send Values
        self.Mixer_Color(rgb, hsv, hsl, cmyk)
    def Mixer_RGB_G2(self, SIGNAL_MIXER_GRADIENT):
        # Percentage Value
        self.percentage_rgb_g2 = SIGNAL_MIXER_GRADIENT / (self.layout.rgb_g2.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = (self.color_rgb_l2[1] + (self.percentage_rgb_g2 * (self.color_rgb_r2[1] - self.color_rgb_l2[1]))) / factorRGB
        rgb2 = (self.color_rgb_l2[2] + (self.percentage_rgb_g2 * (self.color_rgb_r2[2] - self.color_rgb_l2[2]))) / factorRGB
        rgb3 = (self.color_rgb_l2[3] + (self.percentage_rgb_g2 * (self.color_rgb_r2[3] - self.color_rgb_l2[3]))) / factorRGB
        # Converts
        rgb = [rgb1, rgb2, rgb3]
        hsv = self.convert.rgb_to_hsv(rgb1, rgb2, rgb3)
        hsl = self.convert.rgb_to_hsl(rgb1, rgb2, rgb3)
        cmyk = self.convert.rgb_to_cmyk(rgb1, rgb2, rgb3)
        # Send Values
        self.Mixer_Color(rgb, hsv, hsl, cmyk)
    def Mixer_RGB_G3(self, SIGNAL_MIXER_GRADIENT):
        # Percentage Value
        self.percentage_rgb_g3 = SIGNAL_MIXER_GRADIENT / (self.layout.rgb_g3.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = (self.color_rgb_l3[1] + (self.percentage_rgb_g3 * (self.color_rgb_r3[1] - self.color_rgb_l3[1]))) / factorRGB
        rgb2 = (self.color_rgb_l3[2] + (self.percentage_rgb_g3 * (self.color_rgb_r3[2] - self.color_rgb_l3[2]))) / factorRGB
        rgb3 = (self.color_rgb_l3[3] + (self.percentage_rgb_g3 * (self.color_rgb_r3[3] - self.color_rgb_l3[3]))) / factorRGB
        # Converts
        rgb = [rgb1, rgb2, rgb3]
        hsv = self.convert.rgb_to_hsv(rgb1, rgb2, rgb3)
        hsl = self.convert.rgb_to_hsl(rgb1, rgb2, rgb3)
        cmyk = self.convert.rgb_to_cmyk(rgb1, rgb2, rgb3)
        # Send Values
        self.Mixer_Color(rgb, hsv, hsl, cmyk)

    def Mixer_HSV_G1(self, SIGNAL_MIXER_GRADIENT):
        # Percentage Value
        self.percentage_hsv_g1 = SIGNAL_MIXER_GRADIENT / (self.layout.hsv_g1.width())
        # Conditions
        cond1 = self.color_hsv_r1[4] - self.color_hsv_l1[4]
        cond2 = (self.color_hsv_l1[4] + factorHUE) - self.color_hsv_r1[4]
        # Descriminate Condition
        if cond1 <= cond2:
            hue = (self.color_hsv_l1[4] + (self.percentage_hsv_g1 * cond1))
        else:
            hue = (self.color_hsv_l1[4] - (self.percentage_hsv_g1 * cond2))
            if hue <= 0:
                hue = hue + factorHUE
            else:
                pass
        hsv1 = hue / factorHUE
        hsv2 = (self.color_hsv_l1[5] + (self.percentage_hsv_g1 * (self.color_hsv_r1[5] - self.color_hsv_l1[5]))) / factorSVL
        hsv3 = (self.color_hsv_l1[6] + (self.percentage_hsv_g1 * (self.color_hsv_r1[6] - self.color_hsv_l1[6]))) / factorSVL
        # Converts
        rgb = self.convert.hsv_to_rgb(hsv1, hsv2, hsv3)
        hsv = [hsv1, hsv2, hsv3]
        hsl = self.convert.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        cmyk = self.convert.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # Send Values
        self.Mixer_Color(rgb, hsv, hsl, cmyk)
    def Mixer_HSV_G2(self, SIGNAL_MIXER_GRADIENT):
        # Percentage Value
        self.percentage_hsv_g2 = SIGNAL_MIXER_GRADIENT / (self.layout.hsv_g2.width())
        # Conditions
        cond1 = self.color_hsv_r2[4] - self.color_hsv_l2[4]
        cond2 = (self.color_hsv_l2[4] + factorHUE) - self.color_hsv_r2[4]
        # Descriminate Condition
        if cond1 <= cond2:
            hue = (self.color_hsv_l2[4] + (self.percentage_hsv_g2 * cond1))
        else:
            hue = (self.color_hsv_l2[4] - (self.percentage_hsv_g2 * cond2))
            if hue <= 0:
                hue = hue + factorHUE
            else:
                pass
        hsv1 = hue / factorHUE
        hsv2 = (self.color_hsv_l2[5] + (self.percentage_hsv_g2 * (self.color_hsv_r2[5] - self.color_hsv_l2[5]))) / factorSVL
        hsv3 = (self.color_hsv_l2[6] + (self.percentage_hsv_g2 * (self.color_hsv_r2[6] - self.color_hsv_l2[6]))) / factorSVL
        # Converts
        rgb = self.convert.hsv_to_rgb(hsv1, hsv2, hsv3)
        hsv = [hsv1, hsv2, hsv3]
        hsl = self.convert.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        cmyk = self.convert.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # Send Values
        self.Mixer_Color(rgb, hsv, hsl, cmyk)
    def Mixer_HSV_G3(self, SIGNAL_MIXER_GRADIENT):
        # Percentage Value
        self.percentage_hsv_g3 = SIGNAL_MIXER_GRADIENT / (self.layout.hsv_g3.width())
        # Conditions
        cond1 = self.color_hsv_r3[4] - self.color_hsv_l3[4]
        cond2 = (self.color_hsv_l3[4] + factorHUE) - self.color_hsv_r3[4]
        # Descriminate Condition
        if cond1 <= cond2:
            hue = (self.color_hsv_l3[4] + (self.percentage_hsv_g3 * cond1))
        else:
            hue = (self.color_hsv_l3[4] - (self.percentage_hsv_g3 * cond2))
            if hue <= 0:
                hue = hue + factorHUE
            else:
                pass
        hsv1 = hue / factorHUE
        hsv2 = (self.color_hsv_l3[5] + (self.percentage_hsv_g3 * (self.color_hsv_r3[5] - self.color_hsv_l3[5]))) / factorSVL
        hsv3 = (self.color_hsv_l3[6] + (self.percentage_hsv_g3 * (self.color_hsv_r3[6] - self.color_hsv_l3[6]))) / factorSVL
        # Converts
        rgb = self.convert.hsv_to_rgb(hsv1, hsv2, hsv3)
        hsv = [hsv1, hsv2, hsv3]
        hsl = self.convert.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        cmyk = self.convert.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # Send Values
        self.Mixer_Color(rgb, hsv, hsl, cmyk)

    def Mixer_HSL_G1(self, SIGNAL_MIXER_GRADIENT):
        # Percentage Value
        self.percentage_hsl_g1 = SIGNAL_MIXER_GRADIENT / (self.layout.hsl_g1.width())
        # Conditions
        cond1 = self.color_hsl_r1[7] - self.color_hsl_l1[7]
        cond2 = (self.color_hsl_l1[7] + factorHUE) - self.color_hsl_r1[7]
        # Descriminate Condition
        if cond1 <= cond2:
            hue = (self.color_hsl_l1[7] + (self.percentage_hsl_g1 * cond1))
        else:
            hue = (self.color_hsl_l1[7] - (self.percentage_hsl_g1 * cond2))
            if hue <= 0:
                hue = hue + factorHUE
            else:
                pass
        hsl1 = hue / factorHUE
        hsl2 = (self.color_hsl_l1[8] + (self.percentage_hsl_g1 * (self.color_hsl_r1[8] - self.color_hsl_l1[8]))) / factorSVL
        hsl3 = (self.color_hsl_l1[9] + (self.percentage_hsl_g1 * (self.color_hsl_r1[9] - self.color_hsl_l1[9]))) / factorSVL
        # Converts
        rgb = self.convert.hsl_to_rgb(hsl1, hsl2, hsl3)
        hsv = self.convert.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsl = [hsl1, hsl2, hsl3]
        cmyk = self.convert.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # Send Values
        self.Mixer_Color(rgb, hsv, hsl, cmyk)
    def Mixer_HSL_G2(self, SIGNAL_MIXER_GRADIENT):
        # Percentage Value
        self.percentage_hsl_g2 = SIGNAL_MIXER_GRADIENT / (self.layout.hsl_g2.width())
        # Conditions
        cond1 = self.color_hsl_r2[7] - self.color_hsl_l2[7]
        cond2 = (self.color_hsl_l2[7] + factorHUE) - self.color_hsl_r2[7]
        # Descriminate Condition
        if cond1 <= cond2:
            hue = (self.color_hsl_l2[7] + (self.percentage_hsl_g2 * cond1))
        else:
            hue = (self.color_hsl_l2[7] - (self.percentage_hsl_g2 * cond2))
            if hue <= 0:
                hue = hue + factorHUE
            else:
                pass
        hsl1 = hue / factorHUE
        hsl2 = (self.color_hsl_l2[8] + (self.percentage_hsl_g2 * (self.color_hsl_r2[8] - self.color_hsl_l2[8]))) / factorSVL
        hsl3 = (self.color_hsl_l2[9] + (self.percentage_hsl_g2 * (self.color_hsl_r2[9] - self.color_hsl_l2[9]))) / factorSVL
        # Converts
        rgb = self.convert.hsl_to_rgb(hsl1, hsl2, hsl3)
        hsv = self.convert.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsl = [hsl1, hsl2, hsl3]
        cmyk = self.convert.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # Send Values
        self.Mixer_Color(rgb, hsv, hsl, cmyk)
    def Mixer_HSL_G3(self, SIGNAL_MIXER_GRADIENT):
        # Percentage Value
        self.percentage_hsl_g3 = SIGNAL_MIXER_GRADIENT / (self.layout.hsl_g3.width())
        # Conditions
        cond1 = self.color_hsl_r3[7] - self.color_hsl_l3[7]
        cond2 = (self.color_hsl_l3[7] + factorHUE) - self.color_hsl_r3[7]
        # Descriminate Condition
        if cond1 <= cond2:
            hue = (self.color_hsl_l3[7] + (self.percentage_hsl_g3 * cond1))
        else:
            hue = (self.color_hsl_l3[7] - (self.percentage_hsl_g3 * cond2))
            if hue <= 0:
                hue = hue + factorHUE
            else:
                pass
        hsl1 = hue / factorHUE
        hsl2 = (self.color_hsl_l3[8] + (self.percentage_hsl_g3 * (self.color_hsl_r3[8] - self.color_hsl_l3[8]))) / factorSVL
        hsl3 = (self.color_hsl_l3[9] + (self.percentage_hsl_g3 * (self.color_hsl_r3[9] - self.color_hsl_l3[9]))) / factorSVL
        # Converts
        rgb = self.convert.hsl_to_rgb(hsl1, hsl2, hsl3)
        hsv = self.convert.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsl = [hsl1, hsl2, hsl3]
        cmyk = self.convert.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # Send Values
        self.Mixer_Color(rgb, hsv, hsl, cmyk)

    def Mixer_CMYK_G1(self, SIGNAL_MIXER_GRADIENT):
        # Percentage Value
        self.percentage_cmyk_g1 = SIGNAL_MIXER_GRADIENT / (self.layout.cmyk_g1.width())
        # Percentual Value added to Left Color Percentil
        cmyk1 = (self.color_cmyk_l1[10] + (self.percentage_cmyk_g1 * (self.color_cmyk_r1[10] - self.color_cmyk_l1[10]))) / factorCMYK
        cmyk2 = (self.color_cmyk_l1[11] + (self.percentage_cmyk_g1 * (self.color_cmyk_r1[11] - self.color_cmyk_l1[11]))) / factorCMYK
        cmyk3 = (self.color_cmyk_l1[12] + (self.percentage_cmyk_g1 * (self.color_cmyk_r1[12] - self.color_cmyk_l1[12]))) / factorCMYK
        cmyk4 = (self.color_cmyk_l1[13] + (self.percentage_cmyk_g1 * (self.color_cmyk_r1[13] - self.color_cmyk_l1[13]))) / factorCMYK
        # Converts
        rgb = self.convert.cmyk_to_rgb(cmyk1, cmyk2, cmyk3, cmyk4)
        hsv = self.convert.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsl = self.convert.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        cmyk = [cmyk1, cmyk2, cmyk3, cmyk4]
        # Send Values
        self.Mixer_Color(rgb, hsv, hsl, cmyk)
    def Mixer_CMYK_G2(self, SIGNAL_MIXER_GRADIENT):
        # Percentage Value
        self.percentage_cmyk_g2 = SIGNAL_MIXER_GRADIENT / (self.layout.cmyk_g2.width())
        # Percentual Value added to Left Color Percentil
        cmyk1 = (self.color_cmyk_l2[10] + (self.percentage_cmyk_g2 * (self.color_cmyk_r2[10] - self.color_cmyk_l2[10]))) / factorCMYK
        cmyk2 = (self.color_cmyk_l2[11] + (self.percentage_cmyk_g2 * (self.color_cmyk_r2[11] - self.color_cmyk_l2[11]))) / factorCMYK
        cmyk3 = (self.color_cmyk_l2[12] + (self.percentage_cmyk_g2 * (self.color_cmyk_r2[12] - self.color_cmyk_l2[12]))) / factorCMYK
        cmyk4 = (self.color_cmyk_l2[13] + (self.percentage_cmyk_g2 * (self.color_cmyk_r2[13] - self.color_cmyk_l2[13]))) / factorCMYK
        # Converts
        rgb = self.convert.cmyk_to_rgb(cmyk1, cmyk2, cmyk3, cmyk4)
        hsv = self.convert.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsl = self.convert.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        cmyk = [cmyk1, cmyk2, cmyk3, cmyk4]
        # Send Values
        self.Mixer_Color(rgb, hsv, hsl, cmyk)
    def Mixer_CMYK_G3(self, SIGNAL_MIXER_GRADIENT):
        # Percentage Value
        self.percentage_cmyk_g3 = SIGNAL_MIXER_GRADIENT / (self.layout.cmyk_g3.width())
        # Percentual Value added to Left Color Percentil
        cmyk1 = (self.color_cmyk_l3[10] + (self.percentage_cmyk_g3 * (self.color_cmyk_r3[10] - self.color_cmyk_l3[10]))) / factorCMYK
        cmyk2 = (self.color_cmyk_l3[11] + (self.percentage_cmyk_g3 * (self.color_cmyk_r3[11] - self.color_cmyk_l3[11]))) / factorCMYK
        cmyk3 = (self.color_cmyk_l3[12] + (self.percentage_cmyk_g3 * (self.color_cmyk_r3[12] - self.color_cmyk_l3[12]))) / factorCMYK
        cmyk4 = (self.color_cmyk_l3[13] + (self.percentage_cmyk_g3 * (self.color_cmyk_r3[13] - self.color_cmyk_l3[13]))) / factorCMYK
        # Converts
        rgb = self.convert.cmyk_to_rgb(cmyk1, cmyk2, cmyk3, cmyk4)
        hsv = self.convert.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsl = self.convert.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        cmyk = [cmyk1, cmyk2, cmyk3, cmyk4]
        # Send Values
        self.Mixer_Color(rgb, hsv, hsl, cmyk)

    def Mixer_Color(self, rgb, hsv, hsl, cmyk):
        # to Alpha
        aaa = hsv[2]
        # to HSV
        rgb1 = rgb[0]
        rgb2 = rgb[1]
        rgb3 = rgb[2]
        # to HSV
        hsv1 = hsv[0]
        hsv2 = hsv[1]
        hsv3 = hsv[2]
        # to HSL
        hsl1 = hsl[0]
        hsl2 = hsl[1]
        hsl3 = hsl[2]
        # to CMYK
        cmyk1 = cmyk[0]
        cmyk2 = cmyk[1]
        cmyk3 = cmyk[2]
        cmyk4 = cmyk[3]
        # Apply Values
        self.Pigment_Sync("MIX", aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
        self.Pigment_2_Krita(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
        self.Pigment_Display(aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4)
    def Mixer_Display(self):
        # Display Color with Tint, Tone, Shade
        mix_tint = self.style.RGB_Gradient(self.layout.tint.width(), self.color_neutral, self.color_white)
        self.layout.tint.setStyleSheet(mix_tint)
        mix_tone = self.style.RGB_Gradient(self.layout.tone.width(), self.color_neutral, self.color_grey)
        self.layout.tone.setStyleSheet(mix_tone)
        mix_shade = self.style.RGB_Gradient(self.layout.shade.width(), self.color_neutral, self.color_black)
        self.layout.shade.setStyleSheet(mix_shade)
        # RGB Gradients
        mix_rgb_g1 = self.style.RGB_Gradient(self.layout.rgb_g1.width(), self.color_rgb_l1, self.color_rgb_r1)
        self.layout.rgb_g1.setStyleSheet(mix_rgb_g1)
        mix_rgb_g2 = self.style.RGB_Gradient(self.layout.rgb_g2.width(), self.color_rgb_l2, self.color_rgb_r2)
        self.layout.rgb_g2.setStyleSheet(mix_rgb_g2)
        mix_rgb_g3 = self.style.RGB_Gradient(self.layout.rgb_g3.width(), self.color_rgb_l3, self.color_rgb_r3)
        self.layout.rgb_g3.setStyleSheet(mix_rgb_g3)
        # HSV Gradients
        mix_hsv_g1 = self.style.HSV_Gradient(self.layout.hsv_g1.width(), self.color_hsv_l1, self.color_hsv_r1)
        self.layout.hsv_g1.setStyleSheet(str(mix_hsv_g1))
        mix_hsv_g2 = self.style.HSV_Gradient(self.layout.hsv_g2.width(), self.color_hsv_l2, self.color_hsv_r2)
        self.layout.hsv_g2.setStyleSheet(str(mix_hsv_g2))
        mix_hsv_g3 = self.style.HSV_Gradient(self.layout.hsv_g3.width(), self.color_hsv_l3, self.color_hsv_r3)
        self.layout.hsv_g3.setStyleSheet(str(mix_hsv_g3))
        # HSL Gradients
        mix_hsl_g1 = self.style.HSL_Gradient(self.layout.hsl_g1.width(), self.color_hsl_l1, self.color_hsl_r1)
        self.layout.hsl_g1.setStyleSheet(str(mix_hsl_g1))
        mix_hsl_g2 = self.style.HSL_Gradient(self.layout.hsl_g2.width(), self.color_hsl_l2, self.color_hsl_r2)
        self.layout.hsl_g2.setStyleSheet(str(mix_hsl_g2))
        mix_hsl_g3 = self.style.HSL_Gradient(self.layout.hsl_g3.width(), self.color_hsl_l3, self.color_hsl_r3)
        self.layout.hsl_g3.setStyleSheet(str(mix_hsl_g3))
        # HSL Gradients
        mix_cmyk_g1 = self.style.CMYK_Gradient(self.layout.cmyk_g1.width(), self.color_cmyk_l1, self.color_cmyk_r1)
        self.layout.cmyk_g1.setStyleSheet(str(mix_cmyk_g1))
        mix_cmyk_g2 = self.style.CMYK_Gradient(self.layout.cmyk_g2.width(), self.color_cmyk_l2, self.color_cmyk_r2)
        self.layout.cmyk_g2.setStyleSheet(str(mix_cmyk_g2))
        mix_cmyk_g3 = self.style.CMYK_Gradient(self.layout.cmyk_g3.width(), self.color_cmyk_l3, self.color_cmyk_r3)
        self.layout.cmyk_g3.setStyleSheet(str(mix_cmyk_g3))

    def Colors(self, aaa, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3, hsl1, hsl2, hsl3, cmyk1, cmyk2, cmyk3, cmyk4):
        values = [
        aaa*factorAAA,
        rgb1*factorRGB, rgb2*factorRGB, rgb3*factorRGB,
        hsv1*factorHUE, hsv2*factorSVL, hsv3*factorSVL,
        hsl1*factorHUE, hsl2*factorSVL, hsl3*factorSVL,
        cmyk1*factorCMYK, cmyk2*factorCMYK, cmyk3*factorCMYK, cmyk4*factorCMYK]
        return values
    def Current_Colors(self):
        values = [
        self.layout.aaa_value.value(),
        self.layout.rgb_1_value.value(), self.layout.rgb_2_value.value(), self.layout.rgb_3_value.value(),
        self.layout.hsv_1_value.value(), self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value(),
        self.layout.hsl_1_value.value(), self.layout.hsl_2_value.value(), self.layout.hsl_3_value.value(),
        self.layout.cmyk_1_value.value(), self.layout.cmyk_2_value.value(), self.layout.cmyk_3_value.value(), self.layout.cmyk_4_value.value()]
        return values
    def Neutral_Colors(self):
        values = [0, 0,0,0, 0,0,0, 0,0,0, 0,0,0,1*factorCMYK]
        return values

    # Widget Events
    def enterEvent(self, event):
        # Check Krita Once before edit
        self.Krita_Update()
        # Confirm Panel
        self.Ratio()
        # Stop Asking Krita the Current Color
        if check_timer >= 1000:
            self.timer.stop()
        else:
            pass
    def leaveEvent(self, event):
        # Start Asking Krita the Current Color
        if check_timer >= 1000:
            self.timer.start()
        else:
            pass
    def showEvent(self, event):
        # Update on init for correct window Size
        self.panel_hsv.Update_Panel(self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value(), self.layout.panel_hsv_fg.width(), self.layout.panel_hsv_fg.height(), self.HEX_6_SVG())
        self.panel_hsl.Update_Panel(self.layout.hsl_2_value.value(), self.layout.hsl_3_value.value(), self.layout.panel_hsl_fg.width(), self.layout.panel_hsl_fg.height(), self.HEX_6_SVG())
    def resizeEvent(self, event):
        self.Ratio()
    def closeEvent(self, event):
        # Stop QTimer
        if check_timer >= 1000:
            self.timer.stop()
        else:
            pass

    def Ratio(self):
        # Relocate Channel Handle due to Size Variation
        self.aaa_slider.Update(self.layout.aaa_value.value(), factorAAA, self.layout.aaa_slider.width())
        self.rgb_1_slider.Update(self.layout.rgb_1_value.value(), factorRGB, self.layout.rgb_1_slider.width())
        self.rgb_2_slider.Update(self.layout.rgb_2_value.value(), factorRGB, self.layout.rgb_2_slider.width())
        self.rgb_3_slider.Update(self.layout.rgb_3_value.value(), factorRGB, self.layout.rgb_3_slider.width())
        self.hsv_1_slider.Update(self.layout.hsv_1_value.value(), factorHUE, self.layout.hsv_1_slider.width())
        self.hsv_2_slider.Update(self.layout.hsv_2_value.value(), factorSVL, self.layout.hsv_2_slider.width())
        self.hsv_3_slider.Update(self.layout.hsv_3_value.value(), factorSVL, self.layout.hsv_3_slider.width())
        self.hsl_1_slider.Update(self.layout.hsl_1_value.value(), factorHUE, self.layout.hsl_1_slider.width())
        self.hsl_2_slider.Update(self.layout.hsl_2_value.value(), factorSVL, self.layout.hsl_2_slider.width())
        self.hsl_3_slider.Update(self.layout.hsl_3_value.value(), factorSVL, self.layout.hsl_3_slider.width())
        self.cmyk_1_slider.Update(self.layout.cmyk_1_value.value(), factorCMYK, self.layout.cmyk_1_slider.width())
        self.cmyk_2_slider.Update(self.layout.cmyk_2_value.value(), factorCMYK, self.layout.cmyk_2_slider.width())
        self.cmyk_3_slider.Update(self.layout.cmyk_3_value.value(), factorCMYK, self.layout.cmyk_3_slider.width())
        self.cmyk_4_slider.Update(self.layout.cmyk_4_value.value(), factorCMYK, self.layout.cmyk_4_slider.width())

        # Relocate Mixer Handle due to Size Variation
        self.mixer_tint.Update(self.percentage_tint, self.layout.tint.width())
        self.mixer_tone.Update(self.percentage_tone, self.layout.tone.width())
        self.mixer_shade.Update(self.percentage_shade, self.layout.shade.width())
        self.mixer_rgb_g1.Update(self.percentage_rgb_g1, self.layout.rgb_g1.width())
        self.mixer_rgb_g2.Update(self.percentage_rgb_g2, self.layout.rgb_g2.width())
        self.mixer_rgb_g3.Update(self.percentage_rgb_g3, self.layout.rgb_g3.width())
        self.mixer_hsv_g1.Update(self.percentage_hsv_g1, self.layout.hsv_g1.width())
        self.mixer_hsv_g2.Update(self.percentage_hsv_g2, self.layout.hsv_g2.width())
        self.mixer_hsv_g3.Update(self.percentage_hsv_g3, self.layout.hsv_g3.width())
        self.mixer_hsl_g1.Update(self.percentage_hsl_g1, self.layout.hsl_g1.width())
        self.mixer_hsl_g2.Update(self.percentage_hsl_g2, self.layout.hsl_g2.width())
        self.mixer_hsl_g3.Update(self.percentage_hsl_g3, self.layout.hsl_g3.width())
        self.mixer_cmyk_g1.Update(self.percentage_cmyk_g1, self.layout.cmyk_g1.width())
        self.mixer_cmyk_g2.Update(self.percentage_cmyk_g2, self.layout.cmyk_g2.width())
        self.mixer_cmyk_g3.Update(self.percentage_cmyk_g3, self.layout.cmyk_g3.width())

        # Relocate Panel Cursor due to Size Variation
        self.panel_hsv.Update_Panel(self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value(), self.layout.panel_hsv_fg.width(), self.layout.panel_hsv_fg.height(), self.HEX_6_SVG())
        self.panel_hsl.Update_Panel(self.layout.hsl_2_value.value(), self.layout.hsl_3_value.value(), self.layout.panel_hsl_fg.width(), self.layout.panel_hsl_fg.height(), self.HEX_6_SVG())

    # Change the Canvas
    def canvasChanged(self, canvas):
        pass
