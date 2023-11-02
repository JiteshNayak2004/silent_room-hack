#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: NBFM Rx
# Author: dakshinakali
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



from gnuradio import qtgui

class NBFM_Rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "NBFM Rx", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NBFM Rx")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "NBFM_Rx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.freq = freq = 147e6
        self.vol = vol = 8
        self.sql = sql = 42
        self.samp_rate = samp_rate = 10e6
        self.nbfm_bandwidth = nbfm_bandwidth = 12e3
        self.ifg = ifg = 32
        self.center_freq = center_freq = freq+500e3
        self.bbg = bbg = 32

        ##################################################
        # Blocks
        ##################################################
        self._vol_range = Range(0, 20, 1, 8, 200)
        self._vol_win = RangeWidget(self._vol_range, self.set_vol, "Vol", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._vol_win, 7, 1, 1, 1)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._sql_range = Range(-80, 80, 1, 42, 200)
        self._sql_win = RangeWidget(self._sql_range, self.set_sql, "Squelch", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._sql_win, 6, 1, 1, 1)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_tool_bar = Qt.QToolBar(self)
        self._freq_tool_bar.addWidget(Qt.QLabel("FREQ" + ": "))
        self._freq_line_edit = Qt.QLineEdit(str(self.freq))
        self._freq_tool_bar.addWidget(self._freq_line_edit)
        self._freq_line_edit.returnPressed.connect(
            lambda: self.set_freq(eng_notation.str_to_num(str(self._freq_line_edit.text()))))
        self.top_grid_layout.addWidget(self._freq_tool_bar, 3, 1, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=4,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            int(samp_rate/nbfm_bandwidth),
            firdes.low_pass(
                1,
                samp_rate,
                nbfm_bandwidth,
                1e3,
                window.WIN_HAMMING,
                6.76))
        self._ifg_range = Range(0, 40, 5, 32, 200)
        self._ifg_win = RangeWidget(self._ifg_range, self.set_ifg, "IF Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._ifg_win, 4, 1, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(vol)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(0.05)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_cc(1000, 30, 1000, 1)
        self._bbg_range = Range(0, 62, 2, 32, 200)
        self._bbg_win = RangeWidget(self._bbg_range, self.set_bbg, "BB Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._bbg_win, 5, 1, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, center_freq-freq, 1, 0, 0)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(sql, 75e-6, 10, True)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=48000,
        	quad_rate=48000,
        	tau=75e-6,
        	max_dev=5e3,
          )
        self.analog_agc3_xx_0 = analog.agc3_cc(1e-3, 100e-6, 1.0, 1, 1)
        self.analog_agc3_xx_0.set_max_gain(65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc3_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.analog_agc3_xx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.analog_pwr_squelch_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.analog_nbfm_rx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "NBFM_Rx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_center_freq(self.freq+500e3)
        Qt.QMetaObject.invokeMethod(self._freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq)))
        self.analog_sig_source_x_0.set_frequency(self.center_freq-self.freq)

    def get_vol(self):
        return self.vol

    def set_vol(self, vol):
        self.vol = vol
        self.blocks_multiply_const_vxx_1.set_k(self.vol)

    def get_sql(self):
        return self.sql

    def set_sql(self, sql):
        self.sql = sql
        self.analog_pwr_squelch_xx_0.set_threshold(self.sql)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.nbfm_bandwidth, 1e3, window.WIN_HAMMING, 6.76))

    def get_nbfm_bandwidth(self):
        return self.nbfm_bandwidth

    def set_nbfm_bandwidth(self, nbfm_bandwidth):
        self.nbfm_bandwidth = nbfm_bandwidth
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.nbfm_bandwidth, 1e3, window.WIN_HAMMING, 6.76))

    def get_ifg(self):
        return self.ifg

    def set_ifg(self, ifg):
        self.ifg = ifg

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.analog_sig_source_x_0.set_frequency(self.center_freq-self.freq)

    def get_bbg(self):
        return self.bbg

    def set_bbg(self, bbg):
        self.bbg = bbg




def main(top_block_cls=NBFM_Rx, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
