# -*- coding: utf-8 -*-
"""
/***************************************************************************
 StatistikBanken
                                 A QGIS plugin
 Dette plugin henter data fra Statistikbanken
                              -------------------
        begin                : 2017-04-20
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Daníel Örn Árnason
        email                : danielarnason85@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator
# Import the code for the dialog
from statistikbanken_dialog import StatistikBankenDialog
import os.path

from statistikbanken_api import Statbank_api

class StatistikBanken:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'StatistikBanken_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Statistikbanken')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'StatistikBanken')
        self.toolbar.setObjectName(u'StatistikBanken')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('StatistikBanken', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = StatistikBankenDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path =  os.path.join(self.plugin_dir, 'icon.png')
        self.add_action(
            icon_path,
            text=self.tr(u'Hent data fra DST'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&Statistikbanken'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def populate_tree(self):
        """
        Fylder treewidget med data fra Statistikbankens API
        """
        self.tree = self.dlg.treeWidget
        self.data = self.StatBank_api.get_all_subjects()

        self.fill_widget(self.tree, self.data)

    def fill_item(self, item, value):
        for val in value:
            child = QTreeWidgetItem()
            item.addChild(child)
            child.setText(0, val['description'])
            if val['hasSubjects']:
                self.fill_item(child, val['subjects'])


    def fill_widget(self, widget, value):
        widget.clear()
        self.fill_item(widget.invisibleRootItem(), value)

    def connections(self):

        # klik paa item i træ og faa tabelinfo 
        try:
            self.dlg.treeWidget.itemClicked.disconnect()
        except:
            pass
        self.dlg.treeWidget.itemClicked.connect(self.get_tables)

    def get_tables(self):

        valgt_emne = self.tree.currentItem()
        emne_id = self.find_id_in_data(self.data, valgt_emne.text(0))


    def find_id_in_data(self, data, valgt_emne):
        
        for item in data:
            if item['description'] == valgt_emne:
                print(item['id'])
                return item['id']
            elif item['description'] != valgt_emne and item['hasSubjects'] == True:
                new_item = item['subjects']
                self.find_id_in_data(new_item, valgt_emne)


    def run(self):
        """Run method that performs all the real work"""

        # Vores funktioner
        self.StatBank_api = Statbank_api()

        # forbindelser til events
        self.connections()

        # fylder treeWidget med data
        self.populate_tree()

        # show the dialog
        self.dlg.show()

        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
