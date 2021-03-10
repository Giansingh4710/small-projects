
def getHTML():
    filee=open("C:\\Users\\gians\\Desktop\\stuff\\GianGurwinderSinghJi.txt","r")
    data=filee.readlines()
    allKhatas=""
    for i in range(len(data)):
        line=data[i];
        dictform=line.split(" $$$ ");
        title=dictform[0];
        lst=dictform[1].split(" # ");
        views=lst[0];
        date=lst[1];
        link=lst[2];
        newKhata="<tr>"+"<td>"+title+"</td>"+"<td>"+"<a href=\'"+link[0:-1]+"\' target='_blank'>"+link+"</a>"+" </td>"+"<td>"+date+"</td>"+"</tr>";
        allKhatas+=newKhata
    return allKhatas
html=f'''<html>
  <head>
    <style>
      body[
        background-color:#001F3E;
        color:white;         
      ]
      table [
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
      ]

      td, th, li [
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
      ]

      tr:nth-child(even) [
        background-color: #057ac9;
      ]
      h1 [
        border: 1px solid white;
        -webkit-box-shadow: 14px -7px 15px 9px #000000; 
        box-shadow: 14px -7px 15px 9px #000000;
      ]
    </style>
  </head>
  <body>
    <div>
    <h2>Giani Gurwinder Singh Ji Nangli</h2>
    <h1 class="avatar" id="pic"><img src="GianiJi.jpg" alt="Giani gurwinder Singh Ji Nangli" />Giani gurwinder Singh Ji Nangl</h1>
    <table id="khata">
      <tr>
        <th id="column">TITLE</th>
        <th id="column">LINK</th>
        <th id="column">DATE</th>
      </tr>
      {getHTML()}
    </table>
    </div>
    <script type="text/javascript" src="script.js" async></script>
  </body>
</html>'''

html=html.replace("[","{")
html=html.replace("]","}")
print(html)

filee=open("C:\\Users\\gians\\Desktop\\CS\\pythons\\small-projects\\SikhStuff\\WebsiteForGianiJi\\index.html","w")
filee.write(html)
filee.close()