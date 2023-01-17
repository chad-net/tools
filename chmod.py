import os  

path = "../*"  
for root, dirs, files in os.walk(path):  
  for n in dirs:  
    os.chown(os.path.join(root, n), 644, 20)
  for n in files:
    os.chown(os.path.join(root, n), 644, 20)
    