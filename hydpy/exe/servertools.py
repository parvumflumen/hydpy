# -*- coding: utf-8 -*-
"""

>>> from hydpy.core.examples import prepare_full_example_1
>>> prepare_full_example_1()

>>> from hydpy import TestIO
>>> import subprocess, time
>>> with TestIO():
...     process = subprocess.Popen('hyd.py start_server LahnHBV', shell=True)

>>> from urllib import request
>>> t0 = time.perf_counter()
>>> while time.perf_counter()-t0 < 10.0:
...     try:
...         bytestring = request.urlopen('http://localhost/zonez').read()
...         print(str(bytestring, encoding='utf-8'))
...         break
...     except BaseException:
...         time.sleep(0.1)
land_dill: [ 2.  2.  3.  3.  4.  4.  5.  5.  6.  6.  7.  7.]
land_lahn_1: [ 2.  2.  3.  3.  4.  4.  5.  5.  6.  6.  7.  7.  8.]
land_lahn_2: [ 2.  2.  3.  3.  4.  4.  5.  5.  6.  6.]
land_lahn_3: [ 2.  2.  3.  3.  4.  4.  5.  5.  6.  6.  7.  7.  8.  9.]

>>> _ = request.urlopen('http://localhost/close_server')
>>> _ = process.communicate()


"""
# import...
# ...from standard library
import http.server
# ...from HydPy
from hydpy import pub
from hydpy.core import hydpytools


class HydPyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        name = self.path[1:]
        if name == 'close_server':
            self.server.server_close()
        results = []
        for element in self.server.hp.elements:
            par = getattr(element.model.parameters.control, name, None)
            if par is not None:
                results.append(f'{element.name}: {par}')
        self.wfile.write(bytes('\n'.join(results), encoding='utf-8'))


class HydPyHTTPServer(http.server.HTTPServer):

    hp: hydpytools.HydPy

    def prepare_hydpy(self, projectname):
        self.hp = hydpytools.HydPy(projectname)
        hp = self.hp
        pub.timegrids = '1996-01-01', '1996-01-06', '1d'
        pub.sequencemanager.generalfiletype = 'nc'
        hp.prepare_network()
        hp.init_models()
        hp.prepare_inputseries()
        pub.sequencemanager.open_netcdf_reader(
            flatten=True, isolate=True, timeaxis=0)
        hp.load_inputseries()
        pub.sequencemanager.close_netcdf_reader()
        hp.load_conditions()


def start_server(projectname, *, logfile=None) -> None:
    server = HydPyHTTPServer(('', 80), HydPyHTTPRequestHandler)
    server.prepare_hydpy(projectname)
    server.serve_forever()


pub.scriptfunctions['start_server'] = start_server
