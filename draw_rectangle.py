#!/usr/bin/env python
# coding: utf8
"""
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Harald Hentschel, 01/2023
description:
inkscape-extension that generates a rectangle with special dimensions

license: CC BY-NC 4.0
https://creativecommons.org/licenses/by-nc/4.0/

find it on github
https://github.com/Mr-DblH/inkscape-draw-rectangle

mastodon
https://mastodon.social/@MrDblH


v1
- generate rectangles, DIN and special ratios


- - - - - - - - - - - - - - - - -

sources: [5], [6] and [7]

- A-series
  - side_1 = side_2 * sqrt(2)
  - area A0 shall be 1m^2
    1 = side_1^2 * sqrt(2) => a=1/(2^(1/4)) = about 0.840
    => side_2 = side_1 * sqrt(2) about 1.189

- B-series
  - B0 side_1 = 1m; side_2 = side_1*sqrt(2)
  - B1 side_1 = sqrt(A1_1 * A1_2) * sqrt(A0_1 * A0_2)

- C-series
  - side 1 is the shorter one
  - C0 side_1= sqrt(A0_1 * B0_1) * sqrt(A0_2 * B0_2)





- - - - - - - - - - - - - - - - -
sources, 01.01.2023:
[1] https://www.linux-magazine.com/Issues/2020/239/Magic-Circle
[2] https://inkscapetutorial.org/pages/extension.html
[3] https://inkscape.gitlab.io/extensions/documentation/
[4] https://www.onlineprinters.de/magazin/din-formate/
[5] https://home.ph-freiburg.de/deisslerfr/geometrie_II/sicher_geoII_05_06_loesungen/din-format-loesungen.pdf
[6] https://www.home.uni-osnabrueck.de/gskalla/Eigene/papierformat.html
[7] https://www.din-formate.de/berechnung-format-reihe-din-b0-b1-b2-b3-b4-b5-b6-b7-b8-b9-b10-seiten-masse-papier-groesse-in-mm-qm.html
[8] https://gitlab.com/inkscape/extensions/-/blob/master/text_merge.py

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

"""
import inkex
from math import sqrt, pow, pi, e


# ==============================================================================
# SETTINGS
DEBUG_MODE = False


# ==============================================================================
class DrawSizedRectangle(inkex.EffectExtension):
  # defaults like the above (hard-coded)

  def add_arguments(self, pars):
    """
    @pars: parsing the chosen option
    """
    # tab_DIN
    pars.add_argument("--ratio_letterDIN", type=str, default="A")
    pars.add_argument("--ratio_numberDIN", type=str, default="6")
    pars.add_argument("--islandscapeDIN", type=inkex.Boolean, default=False)
    pars.add_argument("--colorDIN", type=inkex.Color, default="#fdc322")
    pars.add_argument("--isdescDIN", type=inkex.Boolean, default=True)
    pars.add_argument("--islayerDIN", type=inkex.Boolean, default=True)
    # tab_ratio
    pars.add_argument("--defaultsizeRatio", type=float, default=100.0)
    pars.add_argument("--ratioRatio", type=str, default=1.00)
    pars.add_argument("--islandscapeRatio", type=inkex.Boolean, default=False)
    pars.add_argument("--colorRatio", type=inkex.Color, default="#fdc322")
    pars.add_argument("--isdescRatio", type=inkex.Boolean, default=True)
    pars.add_argument("--islayerRatio", type=inkex.Boolean, default=True)

    # tabs
    pars.add_argument("--tab", type=str, default="tab_DIN")






  def draw_final_rectangle(self, side_1, side_2, text, color):
    """
    draws the final rectangle
    @side_1: float
    @side_2: float
    @text: str - text of format to be generated
    @return: generated rectangle_element
    """
    current_layer = self.svg.get_current_layer()
    rectElement = inkex.Rectangle().new(0,0, side_1, side_2)
    rect_root = current_layer.add(rectElement)
    rect_root.style = {
        'stroke': "none",
        'fill': str(color)
    }
    # set name of object in the layers' menu
    rect_root.set(inkex.addNS('label', 'inkscape'), "ratio_" + str(text))

    return rect_root





  def draw_description(self, side_1, side_2, text, color):
    """
    shows text inside of the rectangle for better understanding
    @side_1: float
    @side_2: float
    @text: str - text of format to be generated
    @return: generated text_element
    """
    current_layer = self.svg.get_current_layer()
    textElement = inkex.TextElement()
    text_root = current_layer.add(textElement)
    text_root.set("xml:space", "preserve")
    text_root.text = str(text)
    text_root.style = {
        "font-size": "115%",
        "fill": str(color),
        "fill-opacity": 1,
        "stroke": "none",
    }
    # set name of object in the layers' menu
    text_root.set(inkex.addNS('label', 'inkscape'), "ratio_" + str(text) + "_t")

    return text_root


  def generate_chosen_format_string(self, letter, number):
    """
    generates and returns the a string of the chosen format
    @letter: str
    @number: str
    @return: str - e.g. A4
    """
    return str(letter) + str(number)






  def effect(self):
    # init color, landscape-mode, grouping, description
    chosen_color = "#fdc322"
    islandscape = False
    islayer = True
    isdesc = True

    # check tab
    if "tab_DIN" in str(self.options.tab):

      # debugging
      if (DEBUG_MODE):
        self.debug("TAB DIN")

      # extra conditions
      chosen_color = self.options.colorDIN
      islandscape = self.options.islandscapeDIN
      islayer = self.options.islayerDIN
      isdesc = self.options.isdescDIN

      chosen_format = self.generate_chosen_format_string(self.options.ratio_letterDIN, self.options.ratio_numberDIN)
      # A0
      side_A0_1 = (1/ (2**0.25))*1000 #about 0.840 *1000
      side_A0_2 = side_A0_1 * sqrt(2) #about 1.189 *1000
      # B0
      side_B0_1 = 1*1000
      side_B0_2 = side_B0_1 * sqrt(2)
      # C0
      side_C0_1 = sqrt(side_A0_1*side_B0_1)
      side_C0_2 = sqrt(side_A0_2*side_B0_2)

      if chosen_format == "A0":
        side_1 = side_A0_1
        side_2 = side_A0_2

      elif chosen_format == "A1":
        side_1 = side_A0_2/2
        side_2 = side_A0_1

      elif chosen_format == "A2":
        side_1 = side_A0_1/2
        side_2 = side_A0_2/2

      elif chosen_format == "A3":
        side_1 = side_A0_2/4
        side_2 = side_A0_1/2

      elif chosen_format == "A4":
        side_1 = side_A0_1/4
        side_2 = side_A0_2/4

      elif chosen_format == "A5":
        side_1 = side_A0_2/8
        side_2 = side_A0_1/4

      elif chosen_format == "A6":
        side_1 = side_A0_1/8
        side_2 = side_A0_2/8

      elif chosen_format == "A7":
        side_1 = side_A0_2/16
        side_2 = side_A0_1/8

      elif chosen_format == "A8":
        side_1 = side_A0_1/16
        side_2 = side_A0_2/16

      elif chosen_format == "A9":
        side_1 = side_A0_2/32
        side_2 = side_A0_1/16

      elif chosen_format == "A10":
        side_1 = side_A0_1/32
        side_2 = side_A0_2/32

      # B0-series
      elif chosen_format == "B0":
        side_1 = side_B0_1
        side_2 = side_B0_2

      elif chosen_format == "B1":
        side_1 = side_B0_2/2
        side_2 = side_B0_1

      elif chosen_format == "B2":
        side_1 = side_B0_1/2
        side_2 = side_B0_2/2

      elif chosen_format == "B3":
        side_1 = side_B0_2/4
        side_2 = side_B0_1/2

      elif chosen_format == "B4":
        side_1 = side_B0_1/4
        side_2 = side_B0_2/4

      elif chosen_format == "B5":
        side_1 = side_B0_2/8
        side_2 = side_B0_1/4

      elif chosen_format == "B6":
        side_1 = side_B0_1/8
        side_2 = side_B0_2/8

      elif chosen_format == "B7":
        side_1 = side_B0_2/16
        side_2 = side_B0_1/8

      elif chosen_format == "B8":
        side_1 = side_B0_1/16
        side_2 = side_B0_2/16

      elif chosen_format == "B9":
        side_1 = side_B0_2/32
        side_2 = side_B0_1/16

      elif chosen_format == "B10":
        side_1 = side_B0_1/32
        side_2 = side_B0_2/32

      # C-series
      elif chosen_format == "C0":
        side_1 = side_C0_1
        side_2 = side_C0_2

      elif chosen_format == "C1":
        side_1 = side_C0_2/2
        side_2 = side_C0_1

      elif chosen_format == "C2":
        side_1 = side_C0_1/2
        side_2 = side_C0_2/2

      elif chosen_format == "C3":
        side_1 = side_C0_2/4
        side_2 = side_C0_1/2

      elif chosen_format == "C4":
        side_1 = side_C0_1/4
        side_2 = side_C0_2/4

      elif chosen_format == "C5":
        side_1 = side_C0_2/8
        side_2 = side_C0_1/4

      elif chosen_format == "C6":
        side_1 = side_C0_1/8
        side_2 = side_C0_2/8

      elif chosen_format == "C7":
        side_1 = side_C0_2/16
        side_2 = side_C0_1/8

      elif chosen_format == "C8":
        side_1 = side_C0_1/16
        side_2 = side_C0_2/16

      elif chosen_format == "C9":
        side_1 = side_C0_2/32
        side_2 = side_C0_1/16

      elif chosen_format == "C10":
        side_1 = side_C0_1/32
        side_2 = side_C0_2/32

      else:
        side_1 = side_A0_1
        side_2 = side_A0_2
        chosen_format = "A0 | faulty code"


    elif "tab_ratio" in str(self.options.tab):

      # debugging
      if (DEBUG_MODE):
        self.debug("TAB RATIO")

      # extra conditions
      chosen_color = self.options.colorRatio
      islandscape = self.options.islandscapeRatio
      islayer = self.options.islayerRatio
      isdesc = self.options.isdescRatio


      side_1 = self.options.defaultsizeRatio
      if self.options.ratioRatio == "sqrt(2)":
        side_2 = sqrt(2)*side_1
        chosen_format = "1_sqrt2"

      elif self.options.ratioRatio == "phi":
        side_2 = ( (1+sqrt(5)) / 2 ) * side_1
        chosen_format = "1_phi"

      elif self.options.ratioRatio == "e":
        side_2 = e * side_1
        chosen_format = "1_e"

      elif self.options.ratioRatio == "pi":
        side_2 = pi * side_1
        chosen_format = "1_pi"

      elif self.options.ratioRatio == "2":
        side_2 = 2 * side_1
        chosen_format = "1_2"

      elif self.options.ratioRatio == "3":
        side_2 = 3*  side_1
        chosen_format = "1_3"

      elif self.options.ratioRatio == "23":
        side_2 = 3/2 * self.options.defaultsizeRatio
        chosen_format = "2_3"

      elif self.options.ratioRatio == "34":
        side_2 = 4/3 * self.options.defaultsizeRatio
        chosen_format = "3_4"

      elif self.options.ratioRatio == "916":
        side_2 = 16/9 * self.options.defaultsizeRatio
        chosen_format = "9_16"

      else:
        side_2 = side_1
        chosen_format = "1_1"









    #
    # draw the rectangle
    #

    # swap sides if needed
    if (islandscape):
      side_1, side_2 = side_2, side_1

    # draw object
    rect_ele = self.draw_final_rectangle(side_1, side_2, chosen_format, chosen_color)

    # show or draw text as description
    text_ele = self.draw_description(side_1, side_2, chosen_format, chosen_color)


    # group the element if wanted
    if (islayer):
      new_layer = self.svg.add(inkex.Group.new('ratio_'+chosen_format))
      new_layer.append(text_ele)
      new_layer.append(rect_ele)


      # delete text_ele if wanted
      if (not isdesc):
        text_ele.delete()







# =============================== // START //  =================================
if __name__ == "__main__":
  rect = DrawSizedRectangle()
  rect.run()