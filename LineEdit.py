import re

from PyQt5.Qt import *

class LineEdit(QLineEdit):

    types = {
        'email': r'^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$',
        'phone': r'^\+\d{2}\(\d{3}\)\d{3}-\d{2}-\d{2}$',
        'url': r'^((https?|ftp)\:\/\/)?([a-z0-9]{1})((\.[a-z0-9-])|([a-z0-9-]))*\.([a-z]{2,6})(\/?)$',
        'text': r'/^.*$/'
    }


    def __init__(self, default_text='', type_='text', tooltips=True):
        
        super(LineEdit, self).__init__()

        self.__default_text = default_text
        self.__edit_is_empty = True
        self.__tooltips = tooltips

        self.__type = type_
        self.__reg_exp = LineEdit.types[type_]

        self.textChanged.connect(self._update)

        if not self.hasFocus():
            self.focusOutEvent('')


    def focusInEvent(self, event):

        if self.__edit_is_empty:
            self.setText('')


    def focusOutEvent(self, event):

        if self.__edit_is_empty:
            self.setText(self.__default_text)


    def _update(self):

        if self.text() == self.__default_text or self.text() == '':
            self._set_tool_tip('neutral')
            self.__edit_is_empty = True

        elif re.match(self.__reg_exp, self.text()):
            self._set_tool_tip('success')
            self.__edit_is_empty = False

        else:
            self._set_tool_tip('alarm') 
            self.__edit_is_empty = False


    def _set_tool_tip(self, name):

        tips = {
            'alarm': f'<span style="color: red;">Enter correct {self.__type}.</span>',
            'success': '<span style="color: green;">Correct.</span>',
            'neutral': ''
        }

        tip = tips[name]

        if self.__tooltips and self.__type != 'text':
            self.setToolTip(tip)


    def result(self):
        if re.match(self.__reg_exp, self.text()):
            return self.text()
            
        return None        