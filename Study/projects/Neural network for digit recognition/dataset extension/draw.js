

const canvas = document.querySelector('canvas');
const clear = document.getElementById('clear');
const ctx = canvas.getContext('2d');

const canvasOffsetX = canvas.offsetLeft;
const canvasOffsetY = canvas.offsetTop;
canvas.width = 400;
canvas.height = 400;

ctx.strokeStyle = 'white';
ctx.fillStyle = 'black';
ctx.lineWidth = 32;
window.csvContent = "data:text/csv;charset=utf-8,";
// Заполняем канвас пикселями 5x5
for (let x = 0; x < canvas.width; x += 8) {
  for (let y = 0; y < canvas.height; y += 8) {
    ctx.fillRect(x, y, 8, 8);
  }
}

let isDrawing = false;

clear.addEventListener('click', e => {
  if (e.target.id === 'clear') {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Заполняем канвас пикселями 5x5
    for (let x = 0; x < canvas.width; x += 8) {
      for (let y = 0; y < canvas.height; y += 8) {
        ctx.fillRect(x, y, 8, 8);
      }
    }
  }
});

function startDrawing(e) {
  isDrawing = true;
  ctx.beginPath();
  ctx.moveTo(Math.floor(e.offsetX / 10) * 10, Math.floor(e.offsetY / 10) * 10);
}

function stopDrawing() {
  isDrawing = false;
}

function drawLine(e) {
  if (!isDrawing) return;
  ctx.lineTo(Math.floor(e.offsetX / 10) * 10, Math.floor(e.offsetY / 10) * 10);
  ctx.stroke();
}
function centerImage(matrix){
  let temp=[]
  let y_first=-1;
  let x_first=50;
  let y_last;
  let x_last=0;
  for (let y = 0; y < 50; y += 1) {
    for (let x = 0; x < 50; x += 1){
      temp.push([0]);
      if(y_first==-1 && matrix[y*50+x][0]!=0) {
        y_first=y;
      }
      if(matrix[y*50+x][0]!=0 && x<x_first){
        x_first=x;
      }
      if(matrix[y*50+x][0]!=0 && x>x_last){
        x_last=x;
      }
      if(matrix[y*50+x][0]!=0){
        y_last=y;
        
      }
      
    }

  }
  
  let indent_y=Math.floor((50-(y_last-y_first))/2);
  let indent_x=Math.floor((50-(x_last-x_first))/2);
  for(let y=y_first;y<=y_last;y+=1){
    let j = indent_x;
    for(let x=x_first;x<=x_last;x+=1){
      temp[indent_y*50+j]=matrix[y*50+x]
      j+=1;
    }
    indent_y+=1;
  }
  return temp
}
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mousemove', drawLine);

const rezButton = document.getElementById('result');

const func1 = () => {
  window.name = document.getElementById("name").value;
}
rezButton.addEventListener('click', () => {
  
  let imageMatrix=[];

  for (let y = 0; y < canvas.height; y += 8) {
    for (let x = 0; x < canvas.width; x += 8) {
      const pixelData = ctx.getImageData(x, y, 1, 1).data;
      imageMatrix.push([pixelData[2]/255]);
    }
  }
  imageMatrix=centerImage(imageMatrix);
  let rez=net.feedforward(imageMatrix);
  const sortedIndexes = rez.map((value, index) => index)
  .sort((a, b) => rez[b] - rez[a])
  .slice(0, 3);
  console.log(sortedIndexes,name);
  
  window.csvContent+=name+","+imageMatrix+"\n";
  
});
const saveButton = document.getElementById('save');

saveButton.addEventListener('click', () =>{const encodedUri = encodeURI(csvContent);
  const link = document.createElement('a');
  link.href = encodedUri;
  link.download = 'pixel_colors.csv';
  link.click();})
