from python_qt_binding.QtGui import QSortFilterProxyModel
from python_qt_binding.QtCore import QObject, QModelIndex

from arni_gui.topic_item import TopicItem
from arni_gui.tree_topic_item import TreeTopicItem
from arni_gui.ros_model import ROSModel

import sys

if sys.version_info[0] is 2 or (sys.version_info[0] is 3 and sys.version_info[1] < 2):
    from lru_cache import lru_cache
else:
    from functools import lru_cache


class ItemFilterProxy(QSortFilterProxyModel):
    """
    The ItemFilterProxy which is a QSortFilterProxyModel helps to filter the data going to the view so the user only sees what he wants to see (which he can modified by telling the view).
     """


    def __init__(self, parent=None):
        """
        Initializes the ItemFilterProxy

        :param parent: the parent-object
        :type parent: QObject
        """
        super(ItemFilterProxy, self).__init__(parent)
        self.__show_hosts = True
        self.__show_nodes = True
        self.__show_connections = True
        self.__show_topics = True
        self.__show_subscribers = True

        self.__filter_string = ""

    def invalidateFilter(self):
        """
        Invalidates the filter
        """
        QSortFilterProxyModel.invalidateFilter(self)
        # invalidate cache
        self.filterAcceptsRow.cache_clear()

    # creating cache with infinite size
    @lru_cache(None)
    def filterAcceptsRow(self, source_row, source_parent):
        """
        Tells by analysing the given row if it should be shown or not. This behaviour can be modified via
        setFilterRegExp method so that e.g. only the entries of a specific host can be shown.

        :param source_row: the source of the parent
        :type source_row: int
        :param source_parent: the source of the parent
        :type source_parent: QModelIndex

        :returns: True if the row should be shown
        :rtype: bool
        """
        entries = []
        item = source_parent.internalPointer()
        child = None
        if item is not None:
            if isinstance(item, TreeTopicItem):
                child = item.get_child(source_row, self.sourceModel().parent(
                    source_parent).internalPointer())
            else:
                child = source_parent.internalPointer().get_child(source_row)
            entries = [child.get_type(), child.get_seuid(), child.get_state(), child.get_short_data()]
        else:
            child = self.sourceModel().get_root_item().get_child(source_row)
            entries = [child.get_type(), child.get_seuid(), child.get_state(), child.get_short_data()]

        child_childs = child.get_childs( self.sourceModel().parent(
                    source_parent).internalPointer())

        for i in range(0, len(child_childs)):
            if self.filterAcceptsRow(i, self.sourceModel().index(source_row, 0, source_parent)):
                return True

        correct_type = False
        data = entries[0]

        if self.__show_hosts and data == "host":
            correct_type = True
        elif self.__show_nodes and data == "node":
            correct_type = True
        elif self.__show_connections and data == "connection":
            if self.__show_subscribers:
                correct_type = True
            else:
                if child.is_subscriber:
                    correct_type = False
                else:
                    correct_type = True
        elif self.__show_topics is True:
            if data == "topic":
                correct_type = True

        if "--sub" in child.get_seuid():
            print(child.get_seuid() + " " + str(correct_type))
        if correct_type is False:
            return False

        # todo: speed this implementation a lot up by not using the model!!!
        if self.__filter_string is not "":
            tests = [self.__filter_string in entries[i] for i in range(0, len(entries))]
            if True in tests:
                return QSortFilterProxyModel.filterAcceptsRow(self, source_row, source_parent)
            else:
                return False
        return QSortFilterProxyModel.filterAcceptsRow(self, source_row, source_parent)

    def setFilterRegExp(self, string):
        self.invalidateFilter()
        QSortFilterProxyModel.setFilterRegExp(self, string)

    def lessThan(self, left, right):
        """
        Defines the sorting of behaviour when comparing two entries of model item by telling how to compare these.

        :param left: the left-hand side
        :type left: QModellIndex
        :param right: the right-hand side
        :type right: QModellIndex

        :returns: bool
        """
        return left < right

    def show_hosts(self, show_hosts):
        """
        Set true if hosts should be shown

        :param show_hosts: true if hosts should be shown
        :type show_hosts: bool
        """
        self.__show_hosts = show_hosts
        self.invalidateFilter()

    def show_nodes(self, show_nodes):
        """
        Set true if nodes should be shown

        :param show_nodes: true if nodes should be shown
        :type show_nodes: bool
        """
        self.__show_nodes = show_nodes
        self.invalidateFilter()

    def show_connections(self, show_connections):
        """
        Set true if connections should be shown

        :param show_connections: true if connections should be shown
        :type show_connections: bool
        """
        self.__show_connections = show_connections
        self.invalidateFilter()

    def show_topics(self, show_topics):
        """
        Set true if topics should be shown

        :param show_topics: true if topics should be shown
        :type show_topics: bool
        """
        self.__show_topics = show_topics
        self.invalidateFilter()

    def show_subscribers(self, show_subscribers):
        """
        Set true if subscriber should be shown

        :param show_subscriber: true if subscriber should be shown
        :type show_subscriber: bool
        """
        self.__show_subscribers = show_subscribers
        self.invalidateFilter()

    def set_filter_string(self, filter_string):
        self.invalidateFilter()
        self.__filter_string = filter_string
