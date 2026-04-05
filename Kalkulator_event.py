# Nama  : Baiq Adelia Dwi Savitri
# NIM   : F1D02310006
# Kelas : D

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QMessageBox, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

#  Stylesheet (tema Dark Mint)
STYLE = """
QMainWindow, #centralWidget { background-color: #0d1117; }

#card {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 16px;
}

#titleLabel {
    color: #58e6a8;
    font-family: 'Courier New', Courier, monospace;
    font-size: 20px;
    font-weight: bold;
    letter-spacing: 3px;
}

QLabel#fieldLabel, #errorInline, #statusLabel, #hasilKeterangan {
    font-family: 'Courier New', Courier, monospace;
}
QLabel#fieldLabel   { color: #8b949e; font-size: 11px; letter-spacing: 1px; }
#errorInline        { color: #ff6b6b; font-size: 10px; }
#hasilKeterangan    { color: #8b949e; font-size: 10px; letter-spacing: 2px; }
#statusLabel        { color: #ff6b6b; font-size: 10px; letter-spacing: 1px; }

QLineEdit {
    background-color: #0d1117;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 10px 14px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 15px;
    selection-background-color: #58e6a8;
    selection-color: #0d1117;
}
QLineEdit:focus { border: 1.5px solid #58e6a8; }

QComboBox {
    background-color: #0d1117;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 10px 14px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 14px;
}
QComboBox:focus            { border: 1.5px solid #58e6a8; }
QComboBox::drop-down       { border: none; padding-right: 8px; }
QComboBox QAbstractItemView {
    background-color: #161b22;
    color: #e6edf3;
    border: 1px solid #30363d;
    selection-background-color: #58e6a8;
    selection-color: #0d1117;
    font-family: 'Courier New', Courier, monospace;
}

QPushButton#btnHitung {
    background-color: #58e6a8;
    color: #0d1117;
    border: none;
    border-radius: 8px;
    padding: 11px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 2px;
}
QPushButton#btnHitung:hover    { background-color: #3dd68c; }
QPushButton#btnHitung:pressed  { background-color: #2db87a; }
QPushButton#btnHitung:disabled { background-color: #1f2937; color: #4b5563; }

QPushButton#btnClear {
    background-color: transparent;
    color: #ff6b6b;
    border: 1.5px solid #ff6b6b;
    border-radius: 8px;
    padding: 11px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 2px;
}
QPushButton#btnClear:hover   { background-color: #ff6b6b; color: #0d1117; }
QPushButton#btnClear:pressed { background-color: #e05555; color: #0d1117; }

#hasilFrame {
    background-color: #0d1117;
    border: 1px solid #30363d;
    border-radius: 10px;
}

#statusBar {
    background-color: #161b22;
    border-top: 1px solid #30363d;
    border-radius: 0 0 16px 16px;
}

#divider { background-color: #30363d; max-height: 1px; min-height: 1px; }
"""


# Main Window 
class KalkulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KALKULATOR")
        self.setFixedSize(440, 600)
        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        outer = QVBoxLayout(central)
        outer.setContentsMargins(24, 24, 24, 0)
        outer.setSpacing(0)

        # Card
        card = QWidget()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(8)

        # Header
        title = QLabel("KALKULATOR")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        div = QFrame()
        div.setObjectName("divider")
        card_layout.addWidget(div)
        card_layout.addSpacing(4)

        # Angka Pertama
        card_layout.addWidget(self._field_label("ANGKA PERTAMA"))
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("masukkan angka...")
        card_layout.addWidget(self.input1)
        self.err1 = self._err_label()
        card_layout.addWidget(self.err1)

        # Operasi
        card_layout.addWidget(self._field_label("OPERASI"))
        self.combo_op = QComboBox()
        self.combo_op.addItems(["+ Tambah", "− Kurang", "× Kali", "÷ Bagi"])
        card_layout.addWidget(self.combo_op)

        # Angka Kedua
        card_layout.addWidget(self._field_label("ANGKA KEDUA"))
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("masukkan angka...")
        card_layout.addWidget(self.input2)
        self.err2 = self._err_label()
        card_layout.addWidget(self.err2)

        # Tombol
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.btn_hitung = QPushButton("HITUNG  [↵]")
        self.btn_hitung.setObjectName("btnHitung")
        self.btn_hitung.setEnabled(False)
        self.btn_hitung.setShortcut("Return")

        self.btn_clear = QPushButton("CLEAR  [ESC]")
        self.btn_clear.setObjectName("btnClear")
        self.btn_clear.setShortcut("Escape")

        btn_row.addWidget(self.btn_hitung)
        btn_row.addWidget(self.btn_clear)
        card_layout.addLayout(btn_row)

        # Area Hasil
        hasil_frame = QFrame()
        hasil_frame.setObjectName("hasilFrame")
        hasil_frame.setFixedHeight(78)
        hasil_layout = QVBoxLayout(hasil_frame)
        hasil_layout.setContentsMargins(8, 2, 8, 4)
        hasil_layout.setSpacing(0)

        ket = QLabel("OUTPUT")
        ket.setObjectName("hasilKeterangan")
        ket.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        ket.setFixedHeight(14)
        ket.setStyleSheet("font-size:10px; margin-top:0px; margin-bottom:0px;")

        self.hasil_label = QLabel("—")
        self.hasil_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.hasil_label.setContentsMargins(0, 0, 0, 0)
        self.hasil_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.hasil_label.setStyleSheet(
            "color: #58e6a8; font-family: 'Courier New'; font-size: 28px; font-weight: bold; line-height: 1;"
        )
        self.hasil_label.setFont(QFont('Courier New', 28, QFont.Bold))
        self.hasil_label.setMinimumHeight(36)

        hasil_layout.addWidget(ket, alignment=Qt.AlignHCenter | Qt.AlignTop)
        hasil_layout.addWidget(self.hasil_label, alignment=Qt.AlignHCenter | Qt.AlignVCenter)
        card_layout.addWidget(hasil_frame)

        outer.addWidget(card)
        status_bar = QWidget()
        status_bar.setObjectName("statusBar")
        status_bar.setFixedHeight(36)
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(20, 0, 20, 0)

        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.status_label)

        outer.addWidget(status_bar)
    def _field_label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("fieldLabel")
        return lbl

    def _err_label(self):
        lbl = QLabel("")
        lbl.setObjectName("errorInline")
        return lbl

    def _connect_signals(self):
        self.input1.textChanged.connect(self._validasi_input)
        self.input2.textChanged.connect(self._validasi_input)
        self.btn_hitung.clicked.connect(self._hitung)
        self.btn_clear.clicked.connect(self._clear)
        
    def _validasi_input(self):
        valid1 = self._cek_input(self.input1, self.err1)
        valid2 = self._cek_input(self.input2, self.err2)
        kedua_valid = valid1 and valid2
        self.btn_hitung.setEnabled(kedua_valid)
        self.status_label.setText(
            "" if kedua_valid else "⚠  Input tidak valid — tombol Hitung dinonaktifkan"
        )

    def _cek_input(self, line_edit, err_label):
        teks = line_edit.text().strip()
        if teks == "":
            line_edit.setStyleSheet("border: 1.5px solid #ff6b6b; color: #ff6b6b;")
            err_label.setText("⚠  Kolom tidak boleh kosong")
            return False
        try:
            float(teks)
            line_edit.setStyleSheet("")
            err_label.setText("")
            return True
        except ValueError:
            line_edit.setStyleSheet("border: 1.5px solid #ff6b6b; color: #ff6b6b;")
            err_label.setText("⚠  Input harus berupa angka")
            return False

    # Hitung
    def _hitung(self):
        a = float(self.input1.text().strip())
        b = float(self.input2.text().strip())
        op_index = self.combo_op.currentIndex()
        ops = [
            (lambda x, y: x + y, "+"),
            (lambda x, y: x - y, "−"),
            (lambda x, y: x * y, "×"),
        ]
        try:
            if op_index == 3:
                if b == 0:
                    QMessageBox.warning(self, "Error", "Pembagi tidak boleh nol!")
                    return
                hasil, simbol = a / b, "÷"
            else:
                fn, simbol = ops[op_index]
                hasil = fn(a, b)

            teks_hasil = f"{int(hasil)}" if hasil == int(hasil) else f"{hasil:.6g}"
            self.hasil_label.setText(teks_hasil)
            self.status_label.setText(f"  {a} {simbol} {b} = {teks_hasil}")
            self.status_label.setStyleSheet("color: #58e6a8;")
        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", str(e))

    # Clear
    def _clear(self):
        for inp in (self.input1, self.input2):
            inp.clear()
            inp.setStyleSheet("")
        self.err1.setText("")
        self.err2.setText("")
        self.hasil_label.setText("—")
        self.status_label.setText("")
        self.status_label.setStyleSheet("")
        self.btn_hitung.setEnabled(False)
        self.input1.setFocus()

    # Close Event
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Keluar Aplikasi",
            "Apakah Anda yakin ingin menutup kalkulator?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        event.accept() if reply == QMessageBox.Yes else event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    window = KalkulatorApp()
    window.show()
    sys.exit(app.exec_())