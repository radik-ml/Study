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
    try {
      this.biases1 = await readCSVFile('biases1.csv');
      this.biases2 = await readCSVFile('biases2.csv');
      this.weights1 = await readCSVFile('weight1.csv');
      this.weights2 = await readCSVFile('weight2.csv');
  } catch (error) {
      console.error('Ошибка при чтении CSV файлов:', error);
  }
      weight1FileInput.addEventListener('change', async (event) => {
        const weight1File = event.target.files[0];
        this.weights1 = await this.readFileAsMatrix(weight1File);
        //console.log('Weight 1 Matrix:', this.weights1);
    });

    weight2FileInput.addEventListener('change', async (event) => {
        const weight2File = event.target.files[0];
        this.weights2 = await this.readFileAsMatrix(weight2File);
        //console.log('Weight 2 Matrix:', this.weights2);
    });
    biases1FileInput.addEventListener('change', async (event) => {
      const biases1File = event.target.files[0];
      this.biases1 = await this.readFileAsMatrix(biases1File);
      //console.log('Biases 1 Matrix:', this.biases2);
  });

  biases2FileInput.addEventListener('change', async (event) => {
      const biases2File = event.target.files[0];
      this.biases2 = await this.readFileAsMatrix(biases2File);
      //console.log('Biases 2 Matrix:', this.biases2);
  });

      // Добавьте остальную логику, где используются данные из файлов
  }

  async readFileAsMatrix(file) {
    return new Promise((resolve, reject) => {
        if (!(file instanceof Blob)) {
            reject(new Error('The input is not a valid file.'));
            return;
        }

        const reader = new FileReader();
        reader.onload = (event) => {
            const contents = event.target.result;
            const rows = contents.split('\n');
            const matrix = rows.map(row => row.split(',').map(parseFloat));
            matrix.pop()
            resolve(matrix);
        };

        reader.onerror = (error) => {
            reject(error);
        };

        reader.readAsText(file);
    });
  }
  sigmoid(x)
  {
    //console.log(x)
    for (let i = 0; i < x.length; i++){
      x[i]= 1 / (1 + Math.exp(-x[i]))}
    return x
  }
  relu(x){
    //console.log(x)
    for (let i = 0; i < x.length; i++){
      if(x[i]<0){
        x[i]=[0];
      }
    }
    return x;
  }
  dotProduct(v1, v2) {
    let res = [];
    //console.log(v1)
    for (let i = 0; i < v1.length; i++) {
      res[i] = [];
      for (let j = 0; j < v2[0].length; j++) {
        let sum = 0;
        for (let k = 0; k < v1[0].length; k++) {
          //console.log(v1[i][k] , v2[k][j])
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
    //console.log(result)
    return result;
    }
  feedforward(a) {
    // Return the output of the network if "a" is input.
    let b1 = this.biases1;
    let w1 = this.weights1;
    let b2 = this.biases2;
    let w2 = this.weights2;
    let layear1 = this.relu(this.sum(this.dotProduct(w1, a),b1));
    //console.log(layear1)
    //console.log(this.dotProduct(w2, layear1))
    //console.log(this.sum(this.dotProduct(w2, layear1),b2))
    let output = this.sigmoid(this.sum(this.dotProduct(w2, layear1),b2));
    //console.log(output)
    return output;
  }

}

const net = new NeuralNetwork();