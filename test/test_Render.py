import sys
sys.path.append("C:\\temp Daten\\Lernbereich\\Git\\myhamidi\\Py")
import Render

# Test
Rnr = Render.clsGrid(1,2,"")
Rnr.show([[0,1]], "Hello World",500)

# Test
Rnr = Render.clsGrid(2,1,"")
Rnr.show([[0],[1]], "Hello World",500)

# Test
Rnr = Render.clsGrid(2,3,"")
Rnr.show([[0,1,0],[0,0,0]], "Hello World",500)

# Test
Rnr = Render.clsGrid(3,2,"")
Rnr.show([[0,1],[0,0],[0,0]], "Hello World",500)