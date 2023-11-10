import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFormLayout, QShortcut,
                            QFileDialog, QHBoxLayout, QSizePolicy, QSlider, QStyle, QAction, QLineEdit, QGridLayout, QMenu, QMessageBox, QToolButton)
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
        self.openFileAction = QAction(QIcon('images/open.jpeg'), 'Open &File', self)        
        self.openFileAction.setShortcut('Ctrl+O')
        self.openFileAction.setStatusTip('Open movie')
        self.openFileAction.triggered.connect(self.openFile)

        # Create quit app action
        self.quitAction = QAction(QIcon('images/exit.png'), '&Quit', self)        
        self.quitAction.setShortcut('Ctrl+Q')
        self.quitAction.setStatusTip('Exit application')
        self.quitAction.triggered.connect(self.exitCall)

        # Create open multiple files action
        self.openMultipleAction = QAction(QIcon('images/open.jpeg'), 'Open Multiple Files', self)        
        self.openMultipleAction.setShortcut('Ctrl+Shift+O')
        self.openMultipleAction.setStatusTip('Open Multiple Files')
        self.openMultipleAction.triggered.connect(self.openMultipleFiles)

        # Create open directory action
        self.openDirectoryAction = QAction(QIcon('images/directory.jpeg'), 'Open Directory', self)        
        self.openDirectoryAction.setShortcut('Ctrl+F')
        self.openDirectoryAction.setStatusTip('Open Directory')
        self.openDirectoryAction.triggered.connect(self.openDirectory)

        # Create open disc action
        self.openDiscAction = QAction(QIcon('images/disc.png'), 'Open Disc', self)        
        self.openDiscAction.setShortcut('Ctrl+D')
        self.openDiscAction.setStatusTip('Open Disc')
        self.openDiscAction.triggered.connect(self.openDisc)

        # Create open network stream action
        self.openNetworkStreamAction = QAction(QIcon('images/network.png'), 'Open Network Stream', self)        
        self.openNetworkStreamAction.setShortcut('Ctrl+N')
        self.openNetworkStreamAction.setStatusTip('Open Network Stream')
        self.openNetworkStreamAction.triggered.connect(self.openNetworkStream)

        # Create open capture device action
        self.openCaptureDeviceAction = QAction(QIcon('images/device.png'), 'Open Capture Device', self)        
        self.openCaptureDeviceAction.setShortcut('Ctrl+C')
        self.openCaptureDeviceAction.setStatusTip('Open Capture Device')
        self.openCaptureDeviceAction.triggered.connect(self.openCaptureDevice)

        # Create open location from clipboard action 
        self.openLocationFromClipboardAction = QAction(QIcon('images/clipboard.png'), 'Open Location From Clipboard', self)        
        self.openLocationFromClipboardAction.setShortcut('Ctrl+V')
        self.openLocationFromClipboardAction.setStatusTip('Open Location From Clipboard')
        self.openLocationFromClipboardAction.triggered.connect(self.openLocationFromClipboard)

        # Create open recent media action // Add BLACK RIGHT-POINTING TRIANGLE U+25C0
        self.openRecentMediaAction = QAction(QIcon('images/open.jpeg'), 'Open Recent Media', self)        
        self.openRecentMediaAction.setStatusTip('Open Recent Media')
        self.openRecentMediaAction.hovered.connect(self.openRecentMedia)

        # create action to save playlist to file
        self.savePlaylistToFileAction = QAction(QIcon('images/save.jpeg'), 'Save Playlist to File', self)
        self.savePlaylistToFileAction.setShortcut('Ctrl+Y')
        self.savePlaylistToFileAction.triggered.connect(self.savePlaylistToFile)

        # Create action to convert / save
        self.convertOrSaveAction = QAction(QIcon(), 'Conve&rt / Save...', self)
        self.convertOrSaveAction.setShortcut('Ctrl+R')
        self.convertOrSaveAction.triggered.connect(self.convertOrSave)

        # Create menu bar and add action
        self.menuBar = self.menuBar()

        # Create Media menu on the menubar and add action
        self.mediaMenu = self.menuBar.addMenu('&Media')
        self.mediaMenu.addActions([self.openFileAction, self.openMultipleAction,
                                   self.openDirectoryAction,
                                   self.openDiscAction,
                                   self.openNetworkStreamAction,
                                   self.openCaptureDeviceAction,
                                   self.openLocationFromClipboardAction,
                                   self.openRecentMediaAction])
        self.mediaMenu.addSeparator()
        self.mediaMenu.addAction(self.savePlaylistToFileAction)
        self.mediaMenu.addAction(self.convertOrSaveAction)
        self.mediaMenu.addSeparator()
        self.mediaMenu.addAction(self.quitAction)
        
        # Create actions for the playback menu
        self.titleAction = QAction(QIcon(), 'T&itle', self)
        self.chapterAction = QAction(QIcon(), 'Chapter', self)
        self.programAction = QAction(QIcon(), 'Program', self)
        self.customBackgroundsAction = QAction(QIcon(), 'Custom Backgrounds', self)
        self.rendererAction = QAction(QIcon(), 'Renderer', self)
        self.speedAction = QAction(QIcon(), 'Speed', self)
        self.jumpForwardAction = QAction(QIcon(), '&Jump Forward', self)
        self.jumpBackwardAction = QAction(QIcon(), 'Jump Bac&kward', self)
        self.jumpToSpecificTimeAction = QAction(QIcon(), 'Jump To Specific &Time', self)
        self.jumpToSpecificTimeAction.setShortcut('Ctrl+T')
        self.playAction = QAction(QIcon(self.style().standardIcon(QStyle.SP_MediaPlay)), '&Play', self)
        self.playAction.setEnabled(False)
        self.playAction.triggered.connect(self.play)
        self.stopAction = QAction(QIcon(self.style().standardIcon(QStyle.SP_MediaStop)), '&Stop', self)
        self.stopAction.setEnabled(False)
        self.stopAction.triggered.connect(self.stopMedia)
        self.previousAction = QAction(QIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward)), 'Pre&vious', self)
        self.previousAction.setEnabled(False)
        self.previousAction.triggered.connect(self.backSlider)
        self.nextAction = QAction(QIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward)), 'Ne&xt', self)
        self.nextAction.setEnabled(False)
        self.nextAction.triggered.connect(self.forwardSlider)
        self.recordAction = QAction(QIcon('images/recordIcon.png'), 'Record', self)
        self.recordAction.setEnabled(False)

        # Create playback menu on the menubar and add action
        self.playbackMenu = self.menuBar.addMenu('&Playback')
        self.playbackMenu.addActions([self.titleAction, 
                                      self.chapterAction, 
                                      self.programAction, 
                                      self.customBackgroundsAction])
        self.playbackMenu.addSeparator()
        self.playbackMenu.addAction(self.rendererAction)
        self.playbackMenu.addSeparator()
        self.playbackMenu.addAction(self.speedAction)
        self.playbackMenu.addSeparator()
        self.playbackMenu.addActions([self.jumpForwardAction, 
                                      self.jumpBackwardAction, 
                                      self.jumpToSpecificTimeAction])
        self.playbackMenu.addSeparator()
        self.playbackMenu.addActions([self.playAction, 
                                      self.stopAction, 
                                      self.previousAction, 
                                      self.nextAction, 
                                      self.recordAction])


        # Create actions for the audio menu
        self.audioTrackAction = QAction(QIcon(), 'Audio Track', self)
        self.audioDeviceAction = QAction(QIcon(), 'Audio Device', self)
        self.stereoModeAction = QAction(QIcon(), 'Stereo Mode', self)
        self.visualizationsAction = QAction(QIcon(), 'Visualizations', self)
        self.increaseVolumeAction = QAction(QIcon(), '&Increase Volume', self)
        self.decreaseVolumeAction = QAction(QIcon(), 'D&ecrease Volume', self)
        self.muteAction = QAction(QIcon(), '&Mute', self)
        # Create audio menu on the menubar and add action
        self.audioMenu = self.menuBar.addMenu('&Audio')
        self.audioMenu.addActions([self.audioTrackAction, 
                                   self.audioDeviceAction,
                                   self.stereoModeAction])
        self.audioMenu.addSeparator()
        self.audioMenu.addAction(self.visualizationsAction)
        self.audioMenu.addSeparator()
        self.audioMenu.addActions([self.increaseVolumeAction,
                                   self.decreaseVolumeAction,
                                   self.muteAction])

        # Create actions to be added to the video menu
        self.videoTrackAction = QAction(QIcon(), 'Video &Track', self)
        self.fullscreenAction = QAction(QIcon(), '&Fullscreen', self, checkable=True)
        self.alwaysFitWindowAction = QAction(QIcon(), 'Always Fit &Window', self, checkable=True)
        self.setAsWallPaperAction = QAction(QIcon(), 'Set as Wall&paper', self, checkable=True)
        self.zoomAction = QAction(QIcon(), '&Zoom', self)
        self.aspectRatioAction = QAction(QIcon(), '&Aspect Ratio', self)
        self.cropAction = QAction(QIcon(), '&Crop', self)
        self.deinterlaceAction = QAction(QIcon(), '&Deinterlace', self)
        self.deinterlaceModeAction = QAction(QIcon(), '&Deinterlace mode', self)
        self.takeSnapshotAction = QAction(QIcon(), 'Take &Snapshot', self)
        # Create video menu on the menubar and add action
        self.videoMenu = self.menuBar.addMenu('&Video')
        self.videoMenu.addAction(self.videoTrackAction)
        self.videoMenu.addSeparator()
        self.videoMenu.addActions([self.fullscreenAction,
                                   self.alwaysFitWindowAction,
                                   self.setAsWallPaperAction])
        self.videoMenu.addSeparator()
        self.videoMenu.addActions([self.zoomAction,
                                   self.aspectRatioAction,
                                   self.cropAction])
        self.videoMenu.addSeparator()
        self.videoMenu.addActions([self.deinterlaceAction,
                                   self.deinterlaceModeAction])
        self.videoMenu.addSeparator()
        self.videoMenu.addAction(self.takeSnapshotAction)


        # Create actions to be added to subtitle menu
        self.addSubtitleFileAction = QAction(QIcon(), 'Add Subtitle File..', self)
        self.subTrackAction = QAction(QIcon(), 'Sub Track', self)
        # Create subtitle menu on the menubar and add action
        self.subtitleMenu = self.menuBar.addMenu('Subti&tle')
        self.subtitleMenu.addActions([self.addSubtitleFileAction, 
                                      self.subTrackAction])

        # Create actions to add to tools menu
        self.effectsAndFiltersAction = QAction(QIcon(), 'Effects and Filters', self)
        self.effectsAndFiltersAction.setShortcut('Ctrl+E')
        self.trackSynchronizationAction = QAction(QIcon(), 'Track Synchronization', self)
        self.mediaInformationAction = QAction(QIcon('images/info.png'), 'Media Information', self)
        self.codecInformationAction = QAction(QIcon('images/info.png'), '&Codec Information', self)
        self.vlmConfigurationAction = QAction(QIcon(), '&VLM Configuration', self)
        self.programGuideAction = QAction(QIcon(), 'Program Guide', self)
        self.messagesAction = QAction(QIcon(), 'Messages', self)
        self.pluginsAndExtensionsAction = QAction(QIcon(), 'Plugins and extensions', self)
        self.customizeInterfaceAction = QAction(QIcon(), 'Customize Interface..', self)
        self.preferencesAction = QAction(QIcon(), 'Preferences', self)
        # Create tools menu on the menubar and add action
        self.toolsMenu = self.menuBar.addMenu('Tool&s')
        self.toolsMenu.addActions([self.effectsAndFiltersAction,
                                   self.trackSynchronizationAction,
                                   self.mediaInformationAction,
                                   self.codecInformationAction,
                                   self.vlmConfigurationAction,
                                   self.programGuideAction,
                                   self.messagesAction,
                                   self.pluginsAndExtensionsAction])
        self.toolsMenu.addSeparator()
        self.toolsMenu.addActions([self.customizeInterfaceAction,
                                   self.preferencesAction])

        # Create actions to be added to the view menu
        self.playlistAction = QAction(QIcon(), 'Play&list', self)
        self.dockedPlaylistAction = QAction(QIcon(), 'Docked Playlist', self, checkable=True)
        self.alwaysOnTopAction = QAction(QIcon(), 'Always on &Top', self, checkable=True)
        self.minimalInterfaceAction = QAction(QIcon(), 'Mi&nimal Interface', self, checkable=True)
        self.fullscreenInterfaceAction = QAction(QIcon(), '&Fullscreen Interface', self, checkable=True)
        self.advancedControlsAction = QAction(QIcon(), '&Advanced Controls', self, checkable=True)
        self.statusBarAction = QAction(QIcon(), 'Status Bar', self, checkable=True)
        self.addInterfaceAction = QAction(QIcon(), 'Add Interface', self)
        self.VLsubAction = QAction(QIcon(), 'VLsub', self, checkable=True)
        # Create view menu on the menubar and add action
        self.viewMenu = self.menuBar.addMenu('V&iew')
        self.viewMenu.addActions([self.playlistAction,
                                  self.dockedPlaylistAction])
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.alwaysOnTopAction)
        self.viewMenu.addSeparator()
        self.viewMenu.addActions([self.minimalInterfaceAction,
                                  self.fullscreenInterfaceAction,
                                  self.advancedControlsAction,
                                  self.statusBarAction])
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.addInterfaceAction)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.VLsubAction)

        # Create actions to be added to Help menu
        self.helpAction = QAction(QIcon('images/help.png'), '&Help', self)
        self.helpAction.setShortcut('F1')
        self.aboutAction = QAction(QIcon('images/info.png'), '&About', self)
        self.aboutAction.setShortcut('Shift+F1')
        # Create Help menu on the menubar and add action
        self.helpMenu = self.menuBar.addMenu('&Help')
        self.helpMenu.addActions([self.helpAction, 
                                  self.aboutAction])

        # Create layouts to place inside widget
        self.controlLayout = QHBoxLayout()
        self.controlLayout.setContentsMargins(0, 0, 0, 0)
        self.controlLayout.addWidget(self.backward)
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.stopButton)
        self.controlLayout.addWidget(self.forward)
        # self.controlLayout.addWidget(self.positionSlider)

        # Create two horizontal widgets in the control widget
        self.timeAndSlider = QHBoxLayout()
        self.timeAndSlider.addWidget(self.positionSlider)
        
        # Central widget that is the focus of this app
        self.centralWidget = QWidget()

        # Create layout for the central widget
        self.layout = QVBoxLayout()
        
        self.lowerLayout = QVBoxLayout()
        self.lowerLayout.addLayout(self.timeAndSlider)
        self.lowerLayout.addLayout(self.controlLayout)

        
        self.controlwidget = QWidget()
        self.controlwidget.setLayout(self.lowerLayout)

        self.layout.addWidget(self.video_widget)
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

        
        # Create an empty list to hold a list of recently viewed media. Each item in the list should be clickable
        self.recent_list = []
 
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath() + "/Videos", "Media (*.webm *.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.VOB *.m4v *.3gp *.mp3 *.m4a *.m4a *.wav *.ogg *.flac *.m3u *.m3u8)")
        
        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.stopButton.setEnabled(True)
            self.forward.setEnabled(True)
            self.backward.setEnabled(True)

            self.playAction.setEnabled(True)
            self.stopAction.setEnabled(True)
            self.recordAction.setEnabled(True)
            self.previousAction.setEnabled(True)
            self.nextAction.setEnabled(True)
    
    # To do at work
    def savePlaylistToFile(self):
        pass

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
        # Add the list to a custom drop down menu
        menu = QMenu()
        # Add the recent_list to the menu
        menu.addActions(self.recent_list)
        
    def openDisc(self):
        pass 

    def convertOrSave(self):
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

    def mousePressEvent(self, event):
        if event == Qt.RightButton:
            self.contextMenuEvent(event)
    
    def mouseClickEvent(self, event):
        pass

    def handleFullScreen(self):  
        if QtCore.Qt.WindowFullScreen:
            # self.windowState()
            self.showNormal()
        else:
            self.menuBar.hide()
            self.controlwidget.hide()
            self.showFullScreen()

    def hideFullScreen(self):
        pass 

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

    
        
    def contextMenuEvent(self, event):
        # Setting contextMenuPolicy
        self.menu = QMenu(self.centralWidget)
        # Populating the widget with actions
        self.openMediaAction = QAction(QIcon(), 'Open Media', self)
        self.toolsAction = QAction(QIcon(), 'Tool&s', self)
        self.viewAction = QAction(QIcon(), 'V&iew', self)

        self.menu.addAction(self.playAction)
        self.menu.addAction(self.stopAction)
        self.menu.addAction(self.previousAction)
        self.menu.addAction(self.nextAction)
        self.menu.addAction(self.recordAction)
        self.menu.addSeparator()
        self.menu.addAction(self.viewAction)
        self.menu.addAction(self.toolsAction)
        self.menu.addAction(self.playlistAction)
        self.menu.addAction(self.openMediaAction)
        self.menu.addSeparator()
        self.menu.addAction(self.quitAction)

        # Launching the menu 
        self.menu.exec(event.globalPos())
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = VideoWidget()
    w.showMaximized()
    sys.exit(app.exec_())