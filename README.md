Output YANG model Catalog information in either JSON format or XML format by using pyang plugin
Here is two example on how to use pyang plugin to output YANG model catalog information in JSON format or XML format:
w00274778@NJA150614658-F MINGW32 /c/pyang-master
$ pyang -f module-catalog --module-catalog-format xml ietf-interfaces.yang
<ietf-interfaces><prefix>if</prefix><namespace>urn:ietf:params:xml:ns:yang:ietf-interfaces</namespace><name>ietf-interfaces</name><revision>2014-05-08</revision></ietf-interfaces>
{"prefix": "if", "namespace": "urn:ietf:params:xml:ns:yang:ietf-interfaces", "name": "ietf-interfaces", "revision": "2014-05-08"}
<ietf-interfaces><prefix>if</prefix><namespace>urn:ietf:params:xml:ns:yang:ietf-interfaces</namespace><name>ietf-interfaces</name><revision>2014-05-08</revision></ietf-interfaces>
<ietf-interfaces><prefix>if</prefix><namespace>urn:ietf:params:xml:ns:yang:ietf-interfaces</namespace><name>ietf-interfaces</name><revision>2014-05-08</revision></ietf-interfaces>
w00274778@NJA150614658-F MINGW32 /c/pyang-master
$ pyang -f module-catalog --module-catalog-format json ietf-interfaces.yang
{"prefix": "if", "namespace": "urn:ietf:params:xml:ns:yang:ietf-interfaces", "name": "ietf-interfaces", "revision": "2014-05-08"}
{"prefix": "if", "namespace": "urn:ietf:params:xml:ns:yang:ietf-interfaces", "name": "ietf-interfaces", "revision": "2014-05-08"}
<ietf-interfaces><prefix>if</prefix><namespace>urn:ietf:params:xml:ns:yang:ietf-interfaces</namespace><name>ietf-interfaces</name><revision>2014-05-08</revision></ietf-interfaces>
<ietf-interfaces><prefix>if</prefix><namespace>urn:ietf:params:xml:ns:yang:ietf-interfaces</namespace><name>ietf-interfaces</name><revision>2014-05-08</revision></ietf-interfaces>
