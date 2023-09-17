import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFormLayout, QShortcut,
                            QFileDialog, QHBoxLayout, QSizePolicy, QSlider, QStyle, QAction, QLineEdit, QGridLayout, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon, QKeySequence
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtCore import QDir, Qt, QUrl, QEvent


from style import style

class VideoWidget(QMainWindow):
    def __init__(self, parent=None):
        super(VideoWidget, self).__init__(parent)    

        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("Video Player")
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.video_widget = QVideoWidget()
        
        self.forward = QPushButton()
        self.forward.setEnabled(False)
        self.forward.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))

        self.backward = QPushButton()
        self.backward.setEnabled(False)
        self.backward.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))

        self.stopButton = QPushButton()
        self.stopButton.setEnabled(False)
        self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopButton.clicked.connect(self.stopMedia)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create open file action
        self.openFileAction = QAction(QIcon('open.jpeg'), 'Open &File', self)        
        self.openFileAction.setShortcut('Ctrl+O')
        self.openFileAction.setStatusTip('Open movie')
        self.openFileAction.triggered.connect(self.openFile)

        # Create quit app action
        self.quitAction = QAction(QIcon('exit.png'), '&Quit', self)        
        self.quitAction.setShortcut('Ctrl+Q')
        self.quitAction.setStatusTip('Exit application')
        self.quitAction.triggered.connect(self.exitCall)

        # Create open multiple files action // To do on the bus
        self.openMultipleAction = QAction(QIcon('open.jpeg'), 'Open Multiple Files', self)        
        self.openMultipleAction.setShortcut('Ctrl+Shift+O')
        self.openMultipleAction.setStatusTip('Open Multiple Files')
        self.openMultipleAction.triggered.connect(self.openMultipleFiles)

        # Create open directory action // To do on the bus
        self.openDirectoryAction = QAction(QIcon('directory.jpeg'), 'Open Directory', self)        
        self.openDirectoryAction.setShortcut('Ctrl+F')
        self.openDirectoryAction.setStatusTip('Open Directory')
        self.openDirectoryAction.triggered.connect(self.openDirectory)

        # Create open disc action // To do on the bus
        self.openDiscAction = QAction(QIcon('disc.png'), 'Open Disc', self)        
        self.openDiscAction.setShortcut('Ctrl+D')
        self.openDiscAction.setStatusTip('Open Disc')
        self.openDiscAction.triggered.connect(self.openDisc)

        # Create open network stream action // To do on the bus
        self.openNetworkStreamAction = QAction(QIcon('network.png'), 'Open Network Stream', self)        
        self.openNetworkStreamAction.setShortcut('Ctrl+N')
        self.openNetworkStreamAction.setStatusTip('Open Network Stream')
        self.openNetworkStreamAction.triggered.connect(self.openNetworkStream)

        # Create exit action // To do on the bus
        self.openCaptureDeviceAction = QAction(QIcon('device.png'), 'Open Capture Device', self)        
        self.openCaptureDeviceAction.setShortcut('Ctrl+C')
        self.openCaptureDeviceAction.setStatusTip('Open Capture Device')
        self.openCaptureDeviceAction.triggered.connect(self.openCaptureDevice)

        # Create exit action // To do on the bus
        self.openLocationFromClipboardAction = QAction(QIcon('clipboard.png'), 'Open Location From Clipboard', self)        
        self.openLocationFromClipboardAction.setShortcut('Ctrl+V')
        self.openLocationFromClipboardAction.setStatusTip('Open Location From Clipboard')
        self.openLocationFromClipboardAction.triggered.connect(self.openLocationFromClipboard)

        # Create exit action // To do on the bus
        self.openRecentMediaAction = QAction(QIcon('open.jpeg'), 'Open Recent Media', self)        
        self.openRecentMediaAction.setStatusTip('Open Recent Media')
        self.openRecentMediaAction.triggered.connect(self.openRecentMedia)

        # Create menu bar and add action
        self.menuBar = self.menuBar()

        # Create Media menu on the menubar and add action
        self.mediaMenu = self.menuBar.addMenu('&Media')
        self.mediaMenu.addAction(self.openFileAction)
        self.mediaMenu.addAction(self.openMultipleAction)
        self.mediaMenu.addAction(self.openDirectoryAction)
        self.mediaMenu.addAction(self.openDiscAction)
        self.mediaMenu.addAction(self.openNetworkStreamAction)
        self.mediaMenu.addAction(self.openCaptureDeviceAction)
        self.mediaMenu.addAction(self.openLocationFromClipboardAction)
        self.mediaMenu.addAction(self.openRecentMediaAction)
        self.mediaMenu.addAction(self.quitAction)

        # Create playback menu on the menubar and add action
        self.playbackMenu = self.menuBar.addMenu('&Playback')

        # Create audio menu on the menubar and add action
        self.audioMenu = self.menuBar.addMenu('&Audio')

        # Create video menu on the menubar and add action
        self.videoMenu = self.menuBar.addMenu('&Video')

        # Create video menu on the menubar and add action
        self.subtitleMenu = self.menuBar.addMenu('Subti&tle')

        # Create tools menu on the menubar and add action
        self.toolsMenu = self.menuBar.addMenu('Too&ls')

        # Create view menu on the menubar and add action
        self.viewMenu = self.menuBar.addMenu('V&iew')

        # Create Help menu on the menubar and add action
        self.helpMenu = self.menuBar.addMenu('&Help')

        # Create layouts to place inside widget
        self.controlLayout = QHBoxLayout()
        self.controlLayout.setContentsMargins(0, 0, 0, 0)
        self.controlLayout.addWidget(self.backward)
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.stopButton)
        self.controlLayout.addWidget(self.forward)
        self.controlLayout.addWidget(self.positionSlider)
        
        self.centralWidget = QWidget()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video_widget)

        self.controlwidget = QWidget()
        self.controlwidget.setLayout(self.controlLayout)

        self.layout.addWidget(self.controlwidget)
        self.layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        # Shortcuts for volume and seeking
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Up), self)
        self.shortcut.activated.connect(self.volumeUp)

        self.shortcut = QShortcut(QKeySequence(Qt.Key_Down), self)
        self.shortcut.activated.connect(self.volumeDown)

        self.shortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.shortcut.activated.connect(self.forwardSlider)

        self.shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.shortcut.activated.connect(self.backSlider)

        self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier + Qt.Key_Right), self)
        self.shortcut.activated.connect(self.forwardSlider10)

        self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier + Qt.Key_Left), self)
        self.shortcut.activated.connect(self.backSlider10)

        self.mediaPlayer.setVideoOutput(self.video_widget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
 
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath() + "/Videos", "Media (*.webm *.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.VOB *.m4v *.3gp *.mp3 *.m4a *.m4a *.wav *.ogg *.flac *.m3u *.m3u8)")
        
        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.stopButton.setEnabled(True)
            self.forward.setEnabled(True)
            self.backward.setEnabled(True)

    # To do on the bus
    def openMultipleFiles(self):
        pass

    # To do on the bus
    def openDirectory(self):
        pass

    # To do on the bus
    def openNetworkStream(self):
        pass

    # To do on the bus
    def openCaptureDevice(self):
        pass

    # To do on the bus
    def openLocationFromClipboard(self):
        pass

    # To do on the bus
    def openRecentMedia(self):
        pass

    def openDisc(self):
        pass 

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        elif self.mediaPlayer.state() == QMediaPlayer.PausedState:
            self.mediaPlayer.play()
        else:
            self.mediaPlayer.play()

    def exitCall(self):
        sys.exit(app.exec_())

    def mediaStateChanged(self, state):
        if state == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        elif state == QMediaPlayer.StoppedState:
            self.positionSlider.setValue(0)
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
        
    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

    def stopMedia(self):
        self.mediaPlayer.stop()

    def volumeUp(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() + 10)
        print("Volume: " + str(self.mediaPlayer.volume()))

    def volumeDown(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() - 10)
        print("Volume: " + str(self.mediaPlayer.volume()))

    def forwardSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 1000*60)

    def forwardSlider10(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 10000*60)

    def backSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 1000*60)

    def backSlider10(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 10000*60)

# Create a full screen functionality. On double click, show full screen
    def mouseDoubleClickEvent(self, event):
        self.handleFullScreen()

    def handleFullScreen(self):
        self.menuBar.hide()
        self.controlwidget.hide()
        self.showFullScreen()

    def hideSlider(self):
        self.playButton.hide()
        # self.position
        pass 

    def showSlider(self):
        pass

    def hideOrShowSlider(self):
        if self.positionSlider.isVisible():
            self.hideSlider()
        else:
            self.showSlider()

    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = VideoWidget()
    w.showMaximized()
    sys.exit(app.exec_())