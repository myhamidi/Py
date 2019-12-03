import Render

# Test
Rnr = Render.clsGrid(1,2,"")
Rnr.renderArray([[0,1]], "Hello World",500)

# Test
Rnr = Render.clsGrid(2,1,"")
Rnr.renderArray([[0],[1]], "Hello World",500)

# Test
Rnr = Render.clsGrid(2,3,"")
Rnr.renderArray([[0,1,0],[0,0,0]], "Hello World",500)

# Test
Rnr = Render.clsGrid(3,2,"")
Rnr.renderArray([[0,1],[0,0],[0,0]], "Hello World",500)