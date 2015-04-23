all:
	sftp -b batch_copy.txt pi@192.168.0.102
html:
	sftp -b batch_copy_html.txt pi@192.168.0.102
py:
	sftp -b batch_copy_py.txt pi@192.168.0.102
