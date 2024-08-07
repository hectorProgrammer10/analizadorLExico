////

let contenedor = [];
function analizar() {
  executeCommand();
  let codigo = document.getElementById("codigo").value;

  let objetoLexico = {
    valor: "",
    tipo: "",
  };
  $.ajax({
    url: "/analizar", // Esta es la ruta de Flask que manejará la solicitud
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({ codigo: codigo }),
    success: function (response) {
      // Iterar sobre la lista de objetos
      response.forEach(function (obj) {
        objetoLexico = {
          valor: obj.valor,
          tipo: obj.tipo,
        };
        contenedor.push(objetoLexico);
      });
    },
    // Esta función se ejecutará si hay un error en la solicitud
    error: function (error) {
      console.error("Error en la solicitud:", error);
    },
  });
  imprimir(contenedor);
  analisisSintactico();
}
let exampleAnterior = "-";
let examplesG = "";
let examplesS = "";
function imprimir(resultado) {
  let div = document.getElementById("resultado");
  let filas = " ";
  let contadorID = 0;
  let contadorReservada = 0;
  let contadorParen = 0;
  let contadorSim = 0;
  let contadorError = 0;
  toggleExamples(exampleAnterior);
  contenedor.forEach(function (obj) {
    let datostabla = {
      pr: " ",
      id: " ",
      cad: " ",
      num: " ",
      sim: " ",
      tipo: " ",
      error: " ",
    };
    console.log(`${obj.valor}---${obj.tipo}`);
    if (obj.tipo == "ID") {
      datostabla.id = "X";
      contadorID = contadorID + 1;
      datostabla.cad = contadorID;
      exampleAnterior = "-";
    } else if (
      obj.tipo == "CD" ||
      obj.tipo == "LS" ||
      obj.tipo == "PWD" ||
      obj.tipo == "MKDIR" ||
      obj.tipo == "RM" ||
      obj.tipo == "CP" ||
      obj.tipo == "MV" ||
      obj.tipo == "TOUCH" ||
      obj.tipo == "CAT" ||
      obj.tipo == "ECHO"
    ) {
      examplesG = obj.valor;
      examplesS = `examples-${examplesG}`;
      exampleAnterior = examplesS;
      // console.log(`${obj.valor} oooo`);
      toggleExamples(examplesS);
      datostabla.pr = "X";
      contadorReservada = contadorReservada + 1;
      datostabla.cad = contadorReservada;
    } else if (obj.tipo == "LPAREN" || obj.tipo == "RPAREN") {
      datostabla.tipo = "PAREN";
      contadorParen = contadorParen + 1;
      datostabla.cad = contadorParen;
    } else if (
      obj.tipo == "MNUS" ||
      obj.tipo == "SL" ||
      obj.tipo == "MY" ||
      obj.tipo == "DOT"
    ) {
      datostabla.sim = "X";
      contadorSim = contadorSim + 1;
      datostabla.cad = contadorSim;
    } else if (obj.tipo == "ERROR") {
      datostabla.error = "X";
      contadorError = contadorError + 1;
      datostabla.cad = contadorError;
    }
    filas += `<tr>
    <td>${obj.valor}</td>
    <td>${datostabla.pr}</td>
    <td>${datostabla.id}</td>
    <td>${datostabla.cad}</td>
    <td>${datostabla.num}</td>
    <td>${datostabla.sim}</td>
    <td>${datostabla.tipo}</td>
    <td>${datostabla.error}</td>
  </tr>`;
  });
  div.innerHTML = `<table class="mi-tabla">
    <tr>
      <th>TOKEN</th>
      <th>PR</th>
      <th>ID</th>
      <th>CANTIDAD</th>
      <th>NUM</th>
      <th>SIM</th>
      <th>TIPO</th>
      <th>ERROR</th>
    </tr>
    ${filas}
  </table>`;
  contenedor = [];
}

function borrar() {
  let codigo = document.getElementById("codigo");
  let div = document.getElementById("resultado");
  let resultadoSintactico = document.getElementById("resultadoSintactico");
  codigo.value = " ";
  div.innerHTML = " ";
  resultadoSintactico.innerHTML = " ";
  contenedor = [];
}

// ------

function analisisSintactico() {
  let codigo = document.getElementById("codigo").value;
  //analizarSintactico
  $.ajax({
    url: "/analizarSintactico", // Esta es la ruta de Flask que manejará la solicitud
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({ codigo: codigo }),
    success: function (response) {
      console.log(response);
      imprimirSintactico(response);
    },
    // Esta función se ejecutará si hay un error en la solicitud
    error: function (error) {
      console.error("Error en la solicitud:", error);
    },
  });
}

function imprimirSintactico(resultado) {
  let resultadoSemantico = document.getElementById("resultadoSemantico");
  let resultadoSintactico = document.getElementById("resultadoSintactico");
  if (resultado.resultado == "Error en la estructura for") {
    resultadoSintactico.innerHTML = `${resultado.resultado}<br>posicion : ${resultado.posicion}<br>token : ' ${resultado.token} '`;
  } else {
    resultadoSintactico.innerHTML = `${resultado.resultado}`;
    if (resultado.resultado == "Error! Operación no encontrada") {
      resultadoSemantico.innerHTML = " ";
    }
  }
}

// -------
function analisisSemantico() {
  let codigo = document.getElementById("codigo").value;
  //analizarSintactico
  $.ajax({
    url: "/analizarSemantico", // Esta es la ruta de Flask que manejará la solicitud
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({ codigo: codigo }),
    success: function (response) {
      console.log(response);
      imprimirSemantico(response);
    },
    // Esta función se ejecutará si hay un error en la solicitud
    error: function (error) {
      console.error("Error en la solicitud:", error);
    },
  });
}
function imprimirSemantico(resultado) {
  let resultadoS = document.getElementById("resultadoSemantico");
  resultadoS.innerHTML = `${resultado.resultado}`;
}
function toggleExamples(id) {
  if (id == "-") {
    console.log(" ");
  } else {
    var examples = document.getElementById(id);
    if (examples.style.display === "none" || examples.style.display === "") {
      examples.style.display = "block";
    } else {
      examples.style.display = "none";
    }
  }
}

var socket = io();

function executeCommand() {
  var command = document.getElementById("codigo").value;
  console.log(command);
  socket.emit("execute_command", { data: command });
}

socket.on("command_output", function (msg) {
  var outputDiv = document.getElementById("resultadoSemantico");
  outputDiv.innerHTML = " ";
  outputDiv.innerHTML += msg.data + "<br>";
  outputDiv.scrollTop = outputDiv.scrollHeight; // Scroll to bottom
});
