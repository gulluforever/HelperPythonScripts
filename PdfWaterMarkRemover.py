import subprocess
import os
COMMAND = r"""sed -e "s/-www.jntufirstonnet.in/ /" uncompressed.pdf > 1.pdf"""
COMMAND1 = r"""sed -e "s/All Jntu Anantapur Updates/ /" 1.pdf > 2.pdf"""
COMMAND2 = r"""sed -e "s/All Jntu Anantapur Question papers/ /" 2.pdf > 3.pdf"""
COMMAND3 = r"""sed -e "s/www.jntufirstonnet.in/ /" 3.pdf > unwatermarked.pdf"""
for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        fileName, fileExtension = os.path.splitext(os.path.join(subdir, file))
        if '.pdf' in fileExtension:
            try:
                fname = fileName+fileExtension
                print 'working on'+fname
                subprocess.call(['pdftk',fname,'output','uncompressed.pdf','uncompress'])
                proc = subprocess.Popen(COMMAND, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                std_out, std_err = proc.communicate()
                proc = subprocess.Popen(COMMAND1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                std_out, std_err = proc.communicate()
                proc = subprocess.Popen(COMMAND2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                std_out, std_err = proc.communicate()
                proc = subprocess.Popen(COMMAND3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                std_out, std_err = proc.communicate()
                subprocess.call(['pdftk','unwatermarked.pdf','output',os.path.join('output',file),'compress'])
            except:
                print Exception
        
    
