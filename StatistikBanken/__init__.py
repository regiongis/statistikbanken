# -*- coding: utf-8 -*-
"""
/***************************************************************************
 StatistikBanken
                                 A QGIS plugin
 Dette plugin henter data fra Statistikbanken
                             -------------------
        begin                : 2017-04-20
        copyright            : (C) 2017 by Daníel Örn Árnason
        email                : danielarnason85@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load StatistikBanken class from file StatistikBanken.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .statistikbanken import StatistikBanken
    return StatistikBanken(iface)
