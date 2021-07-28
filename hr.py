# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtGui import *
from threading import Thread
import cv2
from database import Database


class HR(QWidget):
    def __init__(self):
        super(HR, self).__init__()

        loader = QUiLoader()
        self.ui = loader.load("mainwindow.ui")

        self.ui.btn1_select.clicked.connect(self.select_workers)
        self.ui.btn2_update.clicked.connect(self.update_workers)
        self.ui.btn3_insert.clicked.connect(self.insert_workers)

        self.ui.show()
    def select_workers(self):
        window.hide()
        select_workers.ui.show()
    def update_workers(self):
        window.hide()
        update_workers.ui.show()
    def insert_workers(self):
        window.hide()
        insert_workers.ui.show()

class Select_workers(HR):
    def __init__(self):
        super(Select_workers,self).__init__()
        loader=QUiLoader()
        self.ui=loader.load('mainwindow_select.ui')
        self.database_show=Database.select()

        for worker in self.database_show:
            self.show_workers(worker[1], worker[2], worker[3],worker[4])

    def show_workers(self,first_name,last_name,na_code,pic):

        label_first_name=QLabel()
        label_first_name.setText(first_name)

        label_last_name=QLabel()
        label_last_name.setText(last_name)

        label_na_code=QLabel()
        label_na_code.setText(str(na_code))

        label_pic=QLabel()
        label_pic.setPixmap(QPixmap(pic))


        self.ui.vl_select1.addWidget(label_na_code)
        self.ui.vl_select2.addWidget(label_first_name)
        self.ui.vl_select3.addWidget(label_last_name)
        self.ui.vl_select4.addWidget(label_pic)

class Insert_workers(HR):
    def __init__(self):
        super(Insert_workers, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load('mainwindow_insert.ui')
        self.ui.btn_new_worker.clicked.connect(self.new_worker)
        self.ui.btn_pic.clicked.connect(self.picture)
        self.ui.btn_faces.clicked.connect(self.face)

    def face(self):
        thread = Thread(target=self.faces)
        thread.start()

    def faces(self):
        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        video_cap = cv2.VideoCapture(0)

        while True:
            validation, frame = video_cap.read()

            if validation is not True:
                break

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_detector.detectMultiScale(frame_gray, 1.3)

            for (x, y, w, h) in faces:
                rows, columns = frame_gray.shape

                half_frame = frame_gray[0:rows, 0:columns // 2]
                flip_frame = cv2.flip(half_frame, 1)
                frame_gray[:, columns // 2:] = flip_frame

                detect_face = frame_gray[y:y + h, x:x + w]
                cv2.imwrite('detect_face.jpg', detect_face)

            cv2.imwrite('faces.jpg', frame_gray)
            pixmap = QPixmap('faces')
            self.ui.pb_face.setPixmap(pixmap)
        video_cap.release()

    def picture(self):
        thread = Thread(target=self.start_picture)
        thread.start()

    def start_picture(self):
        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        video_cap = cv2.VideoCapture(0)

        while True:
            validation, frame = video_cap.read()

            if validation is not True:
                break

            frame_gary = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(frame_gary, 1.3)
            for i, (x, y, w, h) in enumerate(faces):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                self.detect_face = frame[y:y + h, x:x + w]
                cv2.imwrite(f'detect_face.jpg', self.detect_face)

            cv2.imwrite('face.jpg', frame)
            pixmap= QPixmap('face.jpg')
            self.ui.pb_insert.setPixmap(pixmap)
        video_cap.release()


    def new_worker(self):
        first_name = self.ui.tb_first_name.text()
        last_name = self.ui.tb_last_name.text()
        na_code= self.ui.tb_na_code.text()
        if first_name != '' and last_name != ''and na_code!='':
            response = Database.insert(first_name, last_name, na_code)
            if response == True:
                select_workers.show_workers(first_name, last_name, na_code,'image.png')

                msg = QMessageBox()
                msg.setText('Done')
                msg.exec()
        else:
            msg = QMessageBox()
            msg.setText('Error: Fill In The Blanks')
            msg.exec()


class Update_workers(HR):
    def __init__(self):
        super(Update_workers, self).__init__()
        loader = QUiLoader()
        self.database_show = Database.select()
        self.ui=loader.load("mainwindow_update.ui")
        self.ui.btn_search.clicked.connect(self.search)
        self.ui.btn_edit.clicked.connect(self.edit)

    def search(self):
        search_code = self.ui.tb_search.text()
        for worker in self.database_show:
            if search_code == str(worker[3]):
                self.ui.tb_first_name.setText(worker[1])
                self.ui.tb_last_name.setText(worker[2])
                self.ui.tb_na_code.setText(str(worker[3]))

    def edit(self):
        search_code = self.ui.tb_search.text()
        first_name = self.ui.tb_first_name.text()
        last_name = self.ui.tb_last_name.text()
        na_code = self.ui.tb_na_code.text()


        Database.update(na_code, first_name, last_name, search_code)

        msg = QMessageBox()
        msg.setText('Done')
        msg.exec()


if __name__ == "__main__":
    app = QApplication([])
    window = HR()
    select_workers= Select_workers()
    update_workers= Update_workers()
    insert_workers= Insert_workers()
    sys.exit(app.exec())



