import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFormLayout,
                            QFileDialog, QHBoxLayout, QSizePolicy, QSlider, QStyle, QAction, QLineEdit, QGridLayout, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
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

        # Create new action
        self.openAction = QAction(QIcon('open.png'), '&Open', self)        
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Open movie')
        self.openAction.triggered.connect(self.openFile)

        # Create exit action
        self.exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.exitAction)

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
        self.layout.addLayout(self.controlLayout)
        self.layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

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

    def volume(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = VideoWidget()
    w.showMaximized()
    sys.exit(app.exec_())