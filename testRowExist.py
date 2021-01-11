from QualiAnnotations import findRowIndex 
from QualiAnnotations import getTable
 
table = getTable() 
print "\n", table 
 
# Classification-Binary-small.csv (no roi, no zSlice) 
# Make sure to comment other lines to prevent setting zSlice and roi
folder = r"F:\Kidney\Phenotypes\long\Original" 
image  = "11F9_11G5_cropped-WELL024--B01--SUBPO01--LOOP001--COLOR2.tif"
roi, zSlice = "", ""
#image  ="bla" 
#zSlice  = "A" 

# ClassifTable-Mitosis-singleCol.csv (zSlice, no roi) 
#folder, image, zSlice = "C:\Users\Laurent Thomas\Desktop","mitosis.tif","C:2,Z:4,T:31" 
#roi = "test" 
 
# AnnotationEmbryos.csv (roi, no zSlice) 
#folder, image, roi = "C:\Users\Laurent Thomas\Desktop","embryos.jpg", "1130-0223" 

# Mitosis (slice + roi)
folder, image, zSlice, roi = "C:\Users\Laurent Thomas\Desktop", "mitosis.tif", "C:1,Z:1,T:4", "0031-0060-0128"

print "Row existing at row index (NB: 0-based, different than 1-based row number:", findRowIndex(table, folder, image)

if zSlice:
	print "Row with zSlice existing at row index :",         findRowIndex(table, folder, image, zSlice)

if roi:
	print "Row with roi existing at row index:",             findRowIndex(table, folder, image, "", roi)

if zSlice and roi:
	print "Row with zSlice AND roi existing at row index :", findRowIndex(table, folder, image, zSlice, roi) 