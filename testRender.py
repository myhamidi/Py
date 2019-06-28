import render

Monitor = render.clsGrid(8,8,"Hi")

for _ in range(10):
    for i in range(8):
        for j in range(8):  
            arr = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
            arr[i][j] = 1
            Monitor.renderArray(arr,str(i*10+j),10)