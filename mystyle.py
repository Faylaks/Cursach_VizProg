# background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 2,
#                                 stop: 0.4 #9fc5e8, stop: 0.6 #f7ed55,);
style = """
    QWidget{
        background: #f4ccaa;
    }
    QLabel{
        color:#000;
    }
    QPushButton{
            color: black;
            background: #bcf3a4;
            border: 1px #DADADA solid;
            padding: 5px 10px;
            border-radius: 2px;
            font-weight: bold;
            font-size: 9pt;
            outline: none;
    }
    QPushButton:disabled{
        border: 1px solid #999999;
        background-color: #cccccc;
        color: #666666;
        outline: none;
    }
    #table_header{
        color:#000;
        font-size: 10pt;
        font-weight: bold;
        border: 1px dotted #746127;
    }
    QMenuBar{
        padding: 0;
        margin: 0;
        font-size: 8pt;
    }
    #box_action{
        border:0;
        padding: 0;
        margin: 0;
    }
    QPushButton:hover{
        border: 1px #C6C6C6 solid;
        color: #fff;
        background: #274e13;
    }
    QLineEdit{
        padding: 1px;
        border-style: solid;
        border: 2px solid #ffefad;
        border-radius: 8px;
    }
    QScrollBar:vertical { 
        border: none;
        background: white;
        width: 10px;
        margin: 0px 0px 0px 0px;
        } 
        
        QScrollBar::add-line:vertical { 
        background: black;
        height: 15px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
        } 
        
        QScrollBar::sub-line:vertical { 
        background: black;
        height: 15px;
        subcontrol-position: top; 
        subcontrol-origin: margin; 
        } 
        
        QScrollBar::handle:vertical {
        background: #bcf3a4;
        min-height: 20px;
    }
    QComboBox {
        border: 1px solid gray;
        border-radius: 3px;
        padding: 1px 18px 1px 3px;
        min-width: 6em;
    }
    QComboBox:editable {
        background: black;
    }

    QComboBox:!editable, QComboBox::drop-down:editable {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                    stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    }

    /* QComboBox gets the "on" state when the popup is open */
    QComboBox:!editable:on, QComboBox::drop-down:editable:on {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                    stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);
    }

    QComboBox:on { /* shift the text when the popup opens */
        padding-top: 3px;
        padding-left: 4px;
    }

    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;

        border-left-width: 1px;
        border-left-color: darkgray;
        border-left-style: solid; /* just a single line */
        border-top-right-radius: 3px; /* same radius as the QComboBox */
        border-bottom-right-radius: 3px;
    }

    QComboBox::down-arrow {
        image: url(/usr/share/icons/crystalsvg/16x16/actions/1downarrow.png);
    }

    QComboBox::down-arrow:on { /* shift the arrow when popup is open */
        top: 1px;
        left: 1px;
    }
    QTabWidget::pane { /* The tab widget frame */
        border-top: 2px solid #C2C7CB;
    }

    QTabWidget::tab-bar {
        left: 5px; /* move to the right by 5px */
    }

    /* Style the tab using the tab sub-control. Note that
        it reads QTabBar _not_ QTabWidget */
    QTabBar::tab {
        background: #bc8383;
        border: 2px solid #C4C4C3;
        border-bottom-color: #C2C7CB; /* same as the pane color */
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        min-width: 8ex;
        padding: 2px;
    }

    QTabBar::tab:selected, QTabBar::tab:hover {
        background: #ffcbcb;
    }

    QTabBar::tab:selected {
        border-color: #9B9B9B;
        border-bottom-color: #C2C7CB; /* same as pane color */
    }

    QTabBar::tab:!selected {
        margin-top: 2px; /* make non-selected tabs look smaller */
    }
"""