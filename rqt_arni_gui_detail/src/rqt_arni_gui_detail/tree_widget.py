import os
import rospy
import rospkg

from python_qt_binding import loadUi
from python_qt_binding.QtCore import QObject
from python_qt_binding.QtCore import *
from python_qt_binding.QtGui import *

from arni_gui.ros_model import ROSModel
from arni_gui.size_delegate import SizeDelegate
from arni_gui.item_filter_proxy import ItemFilterProxy


class TreeWidget(QWidget):
    def __init__(self):
        super(TreeWidget, self).__init__()
        self.setObjectName('treewidget')

        # Get path to UI file which is a sibling of this file
        rp = rospkg.RosPack()
        ui_file = os.path.join(rp.get_path('rqt_arni_gui_detail'), 'resources', 'TreeWidget.ui')
        # Extend the widget with all attributes and children from UI file
        loadUi(ui_file, self)
        self.setObjectName('TreeWidgetUi')
        

        self.__model = ROSModel()
        self.__filter_proxy = ItemFilterProxy()
        self.__filter_proxy.setSourceModel(self.__model)        
        self.item_tree_view.setModel(self.__filter_proxy)

        self.__size_delegate = SizeDelegate()
        self.item_tree_view.setItemDelegate(self.__size_delegate)       


    def connect_slots(self):
        # : show_nodes_check_box
        self.show_nodes_check_box.stateChanged.connect(self.__on_show_nodes_check_box_state_changed)
        #: show_hosts_check_box
        self.show_hosts_check_box.stateChanged.connect(self.__on_show_hosts_check_box_state_changed)
        #: show_topics_check_box
        self.show_topics_check_box.stateChanged.connect(self.__on_show_topics_check_box_state_changed)
        #: show_connections_check_box
        self.show_connections_check_box.stateChanged.connect(self.__on_show_connections_check_box_state_changed)
        #: show_erroneous_check_box
        self.show_erroneous_check_box.stateChanged.connect(self.__on_show_erroneous_check_box_state_changed)
        #: apply_push_button
        self.apply_push_button.clicked.connect(self.__on_apply_push_button_clicked)
        #: minus_push_button
        self.minus_push_button.clicked.connect(self.__on_minus_push_button_clicked)
        #: plus_push_button
        self.plus_push_button.clicked.connect(self.__on_plus_push_button_clicked)
     


    def __on_show_nodes_check_box_state_changed(self, activated):
        """Displays or delete the nodes in the box wether the check box is set or unset.

        :param activated: 2 if checkBox is set, 0 if checkBox is unset
        :type activated: Integer
        """
        if activated is 2:
            self.__filter_proxy.show_nodes(True)
        else:
            self.__filter_proxy.show_nodes(False)

    def __on_show_hosts_check_box_state_changed(self, activated):
        """Displays or delete the hosts in the box wether the checkBox is set or unset.

        :param activated: 2 if checkBox is set, 0 if check is unset
        :type activated: Integer
        """
        if activated is 2:
            self.__filter_proxy.show_hosts(True)
        else:
            self.__filter_proxy.show_hosts(False)


    def __on_show_topics_check_box_state_changed(self, activated):
        """Displays or delete the topics in the box wether the checkBox is set or unset.

        :param activated: 2 if checkBox is set, 0 if check is unset
        :type activated: Integer
        """
        if activated is 2:
            self.__filter_proxy.show_topics(True)
        else:
            self.__filter_proxy.show_topics(False)


    def __on_show_connections_check_box_state_changed(self, activated):
        """Displays or delete the connections in the box wether the checkBox is set or unset.

        :param activated: 2 if checkBox is set, 0 if check is unset
        :type activated: Integer
        """
        if activated is 2:
            self.__filter_proxy.show_connections(True)
        else:
            self.__filter_proxy.show_connections(False)


    def __on_show_erroneous_check_box_state_changed(self, activated):
        """If this checkBox is set, only erroneous hosts and nodes will be displayed.

        :param activated: 2 if checkBox is set, 0 if check is unset
        :type activated: Integer
        """
        pass

    #TODO say the filter_proxy to filter the items in the tree_view according to the content of the filter-box
    def __on_apply_push_button_clicked(self):
        """Filters the content in the box according to the content of the filter_line_edit"""
        pass

    def __on_minus_push_button_clicked(self):
        """Checks if the minus_push_button is clicked and zoomes out (decrease the size of the font)"""
        self.__size_delegate.set_smaller_font_size() 

    def __on_plus_push_button_clicked(self):
        """Checks if the plus_push_button is clicked and zoomes in (increase the size of the font)"""
        self.__size_delegate.set_bigger_font_size()


