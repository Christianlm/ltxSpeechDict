# -*- coding: UTF-8 -*-

#Copyright (C)2018
# Released under GPL 2
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.


import globalPluginHandler
import os
import speechDictHandler
import languageHandler
import ui
import addonHandler
addonHandler.initTranslation()

_pluginDir = os.path.dirname(__file__)
_dicFileName = "ltx.dic"

def getDicFolder(pluginDir=_pluginDir):
	langs = [languageHandler.getLanguage(), "en"]
	for lang in langs:
		dicFolder = os.path.join(pluginDir, "dic", lang)
		if os.path.isdir(dicFolder):
			return dicFolder
		if "_" in lang:
			tryLang = lang.split("_")[0]
			dicFolder = os.path.join(pluginDir, "dic", tryLang)
			if os.path.isdir(dicFolder):
				return dicFolder
			if tryLang == "en":
				break
		if lang == "en":
			break
	return None

def getDicPath(dicFileName=_dicFileName):
	dicPath = getDicFolder()
	if dicPath is not None:
		dicFile = os.path.join(dicPath, dicFileName)
		if os.path.isfile(dicFile):
			dicPath = dicFile
	return dicPath

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def activateLtxDict(self):
		if self.ltx == True or self.SD is None:
			return
		self.SD.load(self.dicFile)
		speechDictHandler.dictionaries["temp"].extend(self.SD)
		self.ltx = True

	def deactivateLtxDict(self):
		if self.ltx == False or self.SD is None:
			return
		for entry in self.SD:
			speechDictHandler.dictionaries["temp"].remove(entry)
		self.ltx = False

	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self.ltx = False
		self.dicFile = getDicPath()
		if self.dicFile is not None:
			self.SD = speechDictHandler.SpeechDict()
		else:
			self.SD = None

	def terminate(self):
		self.deactivateLtxDict()
		self.dicFile = None
		self.SD = None

	def script_dicttoggle(self, gesture):
		if self.SD is None:
			# Translators: warning when the dictionary is not found.
			ui.message("Latex dictionary not available.")
			return
		if self.ltx == True:
			self.deactivateLtxDict()
			# Translators: warning when the dictionary is unloaded.
			ui.message(_("Latex dictionary %s") % _("off"))
		else:
			self.activateLtxDict()
			# Translators: warning when the dictionary is loaded.
			ui.message(_("Latex dictionary %s") % _("on"))
	script_dicttoggle.__doc__ = _("Toggles on and off the speaking of Latex dictionary.")

	__gestures = {
		"kb:NVDA+shift+i": "dicttoggle"
	}
