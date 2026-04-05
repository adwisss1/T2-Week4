# ============================================================
# Nama  : [Nama Anda]
# NIM   : [NIM Anda]
# Kelas : [Kelas Anda]
# ============================================================
# Tugas 2 - Week 4: Event & Signal Handling
# Mata Kuliah: Pemrograman Visual
# Topik: Kalkulator dengan Event Handling (PyQt5)
# ============================================================

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon


# ─────────────────────────────────────────────────────────────
#  Stylesheet — tema "Dark Mint" dengan font Courier New
# ─────────────────────────────────────────────────────────────
STYLE = """
/* Jendela utama */
QMainWindow {
    background-color: #0d1117;
}

/* Widget pusat */
#centralWidget {
    background-color: #0d1117;
}

/* Card container */
#card {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 16px;
}

/* Label judul */
#titleLabel {
    color: #58e6a8;
    font-family: 'Courier New', Courier, monospace;
    font-size: 20px;
    font-weight: bold;
    letter-spacing: 3px;
}

/* Label sub */
#subLabel {
    color: #8b949e;
    font-family: 'Courier New', Courier, monospace;
    font-size: 10px;
    letter-spacing: 2px;
}

/* Label field */
QLabel#fieldLabel {
    color: #8b949e;
    font-family: 'Courier New', Courier, monospace;
    font-size: 11px;
    letter-spacing: 1px;
}

/* Input angka */
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

QLineEdit:focus {
    border: 1.5px solid #58e6a8;
}

QLineEdit#inputError {
    border: 1.5px solid #ff6b6b;
    color: #ff6b6b;
}

/* Dropdown operasi */
QComboBox {
    background-color: #0d1117;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 10px 14px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 14px;
}

QComboBox:focus {
    border: 1.5px solid #58e6a8;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #161b22;
    color: #e6edf3;
    border: 1px solid #30363d;
    selection-background-color: #58e6a8;
    selection-color: #0d1117;
    font-family: 'Courier New', Courier, monospace;
}

/* Tombol Hitung */
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

QPushButton#btnHitung:hover {
    background-color: #3dd68c;
}

QPushButton#btnHitung:pressed {
    background-color: #2db87a;
}

QPushButton#btnHitung:disabled {
    background-color: #1f2937;
    color: #4b5563;
}

/* Tombol Clear */
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

QPushButton#btnClear:hover {
    background-color: #ff6b6b;
    color: #0d1117;
}

QPushButton#btnClear:pressed {
    background-color: #e05555;
    color: #0d1117;
}

/* Area hasil */
#hasilFrame {
    background-color: #0d1117;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 4px;
}

#hasilLabel {
    color: #58e6a8;
    font-family: 'Courier New', Courier, monospace;
    font-size: 28px;
    font-weight: bold;
    letter-spacing: 2px;
}

#hasilKeterangan {
    color: #8b949e;
    font-family: 'Courier New', Courier, monospace;
    font-size: 10px;
    letter-spacing: 2px;
}

/* Pesan error / status bawah */
#statusBar {
    background-color: #161b22;
    border-top: 1px solid #30363d;
    border-radius: 0 0 16px 16px;
}

#statusLabel {
    color: #ff6b6b;
    font-family: 'Courier New', Courier, monospace;
    font-size: 10px;
    letter-spacing: 1px;
}

/* Pesan error inline */
#errorInline {
    color: #ff6b6b;
    font-family: 'Courier New', Courier, monospace;
    font-size: 10px;
}

/* Divider */
#divider {
    background-color: #30363d;
    max-height: 1px;
    min-height: 1px;
}
"""

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

        card = QWidget()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(16)

        title = QLabel("KALKULATOR")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(title)

        # Divider
        div1 = QFrame()
        div1.setObjectName("divider")
        card_layout.addWidget(div1)
        card_layout.addSpacing(4)

        # ── Input Angka Pertama ───────────────────────────────
        lbl1 = QLabel("ANGKA PERTAMA")
        lbl1.setObjectName("fieldLabel")
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("masukkan angka...")
        self.err1 = QLabel("")
        self.err1.setObjectName("errorInline")

        card_layout.addWidget(lbl1)
        card_layout.addWidget(self.input1)
        card_layout.addWidget(self.err1)

        # ── Operasi ───────────────────────────────────────────
        lbl_op = QLabel("OPERASI")
        lbl_op.setObjectName("fieldLabel")
        self.combo_op = QComboBox()
        self.combo_op.addItems(["+ Tambah", "− Kurang", "× Kali", "÷ Bagi"])

        card_layout.addWidget(lbl_op)
        card_layout.addWidget(self.combo_op)

        # ── Input Angka Kedua ─────────────────────────────────
        lbl2 = QLabel("ANGKA KEDUA")
        lbl2.setObjectName("fieldLabel")
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("masukkan angka...")
        self.err2 = QLabel("")
        self.err2.setObjectName("errorInline")

        card_layout.addWidget(lbl2)
        card_layout.addWidget(self.input2)
        card_layout.addWidget(self.err2)

        card_layout.addSpacing(4)

        # ── Tombol ────────────────────────────────────────────
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

        # ── Area Hasil ────────────────────────────────────────
        hasil_frame = QFrame()
        hasil_frame.setObjectName("hasilFrame")
        hasil_layout = QVBoxLayout(hasil_frame)
        hasil_layout.setContentsMargins(12, 14, 12, 14)
        hasil_layout.setSpacing(2)

        ket = QLabel("OUTPUT")
        ket.setObjectName("hasilKeterangan")
        ket.setAlignment(Qt.AlignCenter)

        self.hasil_label.setAlignment(Qt.AlignCenter)
        # Pastikan label hasil memiliki style dan ukuran yang jelas
        self.hasil_label.setStyleSheet("color: #58e6a8;")
        self.hasil_label.setMinimumHeight(40)
        self.hasil_label.setFont(QFont('Courier New', 20, QFont.Bold))

        hasil_layout.addWidget(ket)
        hasil_layout.addWidget(self.hasil_label)
        card_layout.addWidget(hasil_frame)

        outer.addWidget(card)

        # ── Status Bar ────────────────────────────────────────
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

    # ── Signal & Slot Connections ─────────────────────────────
    def _connect_signals(self):
        # Validasi real-time saat teks berubah
        self.input1.textChanged.connect(self._validasi_input)
        self.input2.textChanged.connect(self._validasi_input)

        # Tombol
        self.btn_hitung.clicked.connect(self._hitung)
        self.btn_clear.clicked.connect(self._clear)

    # ── Validasi Real-Time ────────────────────────────────────
    def _validasi_input(self):
        """Dipanggil setiap kali isi QLineEdit berubah (signal textChanged)."""
        valid1 = self._cek_input(self.input1, self.err1)
        valid2 = self._cek_input(self.input2, self.err2)

        kedua_valid = valid1 and valid2

        # Aktifkan / nonaktifkan tombol Hitung
        self.btn_hitung.setEnabled(kedua_valid)

        # Update status bar
        if kedua_valid:
            self.status_label.setText("")
        else:
            self.status_label.setText("⚠  Input tidak valid — tombol Hitung dinonaktifkan")

    def _cek_input(self, line_edit: QLineEdit, err_label: QLabel) -> bool:
        """Kembalikan True jika isi QLineEdit adalah angka yang valid."""
        teks = line_edit.text().strip()

        # Bidang kosong
        if teks == "":
            line_edit.setObjectName("inputError")
            line_edit.setStyleSheet("border: 1.5px solid #ff6b6b; color: #ff6b6b;")
            err_label.setText("⚠  Kolom tidak boleh kosong")
            return False

        # Coba parse sebagai float
        try:
            float(teks)
            line_edit.setStyleSheet("")          # kembali normal
            err_label.setText("")
            return True
        except ValueError:
            line_edit.setStyleSheet("border: 1.5px solid #ff6b6b; color: #ff6b6b;")
            err_label.setText("⚠  Input harus berupa angka")
            return False

    # ── Hitung ────────────────────────────────────────────────
    def _hitung(self):
        """Dipanggil saat tombol Hitung diklik atau Enter ditekan."""
        a = float(self.input1.text().strip())
        b = float(self.input2.text().strip())
        op_index = self.combo_op.currentIndex()

        try:
            if op_index == 0:
                hasil = a + b
                simbol = "+"
            elif op_index == 1:
                hasil = a - b
                simbol = "−"
            elif op_index == 2:
                hasil = a * b
                simbol = "×"
            else:  # bagi
                if b == 0:
                    QMessageBox.warning(self, "Error", "Pembagi tidak boleh nol!")
                    return
                hasil = a / b
                simbol = "÷"

            # Format hasil: hilangkan .0 jika bilangan bulat
            if hasil == int(hasil):
                teks_hasil = f"{int(hasil)}"
            else:
                teks_hasil = f"{hasil:.6g}"

            # Tampilkan hasil di kolom OUTPUT
            self.hasil_label.setText(teks_hasil)
            self.hasil_label.setStyleSheet("color: #58e6a8;")

            # Jangan duplikasi hasil di status bawah — cukup beri tanda sukses singkat
            self.status_label.setText("Hasil ditampilkan")
            self.status_label.setStyleSheet("color: #58e6a8;")

        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", str(e))

    # ── Clear ─────────────────────────────────────────────────
    def _clear(self):
        """Reset semua input dan hasil."""
        self.input1.clear()
        self.input2.clear()
        self.input1.setStyleSheet("")
        self.input2.setStyleSheet("")
        self.err1.setText("")
        self.err2.setText("")
        self.hasil_label.setText("—")
        self.status_label.setText("")
        self.status_label.setStyleSheet("")
        self.btn_hitung.setEnabled(False)
        self.input1.setFocus()

    # ── Close Event ───────────────────────────────────────────
    def closeEvent(self, event):
        """Konfirmasi QMessageBox sebelum menutup jendela."""
        reply = QMessageBox.question(
            self,
            "Keluar Aplikasi",
            "Apakah Anda yakin ingin menutup kalkulator?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# ─────────────────────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)

    window = KalkulatorApp()
    window.show()

    sys.exit(app.exec_())