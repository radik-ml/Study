
function readCSVFile(url) {
  return fetch(url)
    .then(response => response.text())
    .then(data => {
      const rows = data.split('\n');
      const matrix = rows.map(row => row.split(',').map(parseFloat));
      matrix.pop()
      return matrix;
    });
}
class NeuralNetwork {
  constructor() {
    this.initializeData();
  }

  async initializeData() {
    this.biases1 = await readCSVFile('https://raw.githubusercontent.com/giperbaba/WebAlgorithms/master/neuronAlgorithm/biases1.csv');
    this.biases2 = await readCSVFile('https://raw.githubusercontent.com/giperbaba/WebAlgorithms/master/neuronAlgorithm/biases2.csv');
    this.weights1 = await readCSVFile('https://raw.githubusercontent.com/giperbaba/WebAlgorithms/master/neuronAlgorithm/weight1.csv');
    this.weights2 = await readCSVFile('https://raw.githubusercontent.com/giperbaba/WebAlgorithms/master/neuronAlgorithm/weight2.csv');
  }
  sigmoid(x)
  {
    for (let i = 0; i < x.length; i++){
      x[i]= 1 / (1 + Math.exp(-x[i]))}
    return x
  }
  relu(x){

    for (let i = 0; i < x.length; i++){
      if(x[i]<0){
        x[i]=[0];
      }
    }
    return x;
  }
  matrixProduct(v1, v2) {
    let res = [];
    for (let i = 0; i < v1.length; i++) {
      res[i] = [];
      for (let j = 0; j < v2[0].length; j++) {
        let sum = 0;
        for (let k = 0; k < v1[0].length; k++) {
          sum += v1[i][k] * v2[k][j];
        }
        res[i][j] = sum;
      }
    }
    return res;
  }
  sum(matrix1,matrix2){
    let result = [];
    for (let i = 0; i < matrix1.length; i++) {
      // Проверяем, является ли matrix1 одномерным массивом
      if (!Array.isArray(matrix1[i])) {
        result.push(matrix1[i] + matrix2[i][0]);
      } else {
        let row = [];
        for (let j = 0; j < matrix1[i].length; j++) {
          row.push(matrix1[i][j] + matrix2[i][j]);
        }
        result.push(row);
      }
    }
    return result;
  }
  feedforward(inputImage) {

    let layear1 = this.relu(this.sum(this.matrixProduct(this.weights1, inputImage),this.biases1));

    let output = this.sigmoid(this.sum(this.matrixProduct(this.weights2, layear1),this.biases2));

    return output;
  }

}

const net = new NeuralNetwork();
