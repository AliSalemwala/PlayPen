window.addEventListener('DOMContentLoaded', function(){
  // verify below
  document.body.style.cursor = "wait";
  var cfgtable = document.getElementById("cfgtable");
  populateList (cfgtable);
});

function populateList (table){
  var cfgDetails;
  
//  fetch ('https://api.myjson.com/bins/jeo5a')
  fetch ('http://localhost:5000/phylogeny/cfg/' + localStorage.md5Name + '/' + localStorage.neighbourName + '.json')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    var graphs = myJson.graphs;
    console.log (JSON.stringify(myJson));
    Object.keys(graphs).map ((key) => {
      let row = table.insertRow();
      let cell = row.insertCell();
      cell.innerHTML = graphs[key].g_id;
      cell.onclick = () => {
        makeGraph (graphs[key])
      }
    })
    // verify below
    document.body.style.cursor = "default";
  });
}

function makeGraph(graphDetails){
    var cy = cytoscape({
      container: document.getElementById('cy'),
  
      boxSelectionEnabled: true,
      autounselectify: true,
  
      layout: {
        name: 'dagre'
      },
  
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#FFFFFF'
          }
        },
  
        {
          selector: 'edge',
          style: {
            'width': 4,
            'target-arrow-shape': 'triangle',
            'line-color': '#9dbaea',
            'target-arrow-color': '#9dbaea',
            'curve-style': 'bezier'
          }
        }
      ],
  
      elements: {
        nodes: graphDetails.nodes,
        edges: graphDetails.edges
      }
    });
    
  cy.on('tap', 'node', function(){
    document.getElementsByClassName('modal-body')[0].innerHTML = this.data ('text');
    document.getElementById('myModal').style.display = 'block';
    // verify below
//    cy.fit (this);
/*
    cy.animation ({
      style: {'opacity': 0},
      duration: 1000
    }).play();

    cy.animate({
      pan: { x: this.position().x, y: this.position().y },
      zoom: 1
    }, {
      duration: 1000,
      easing: 'ease-in-out-circ'
    }
    
    );
    */
  });

  addModalListener (cy);
}

function addModalListener(cy){
  document.getElementById ("myModal").addEventListener(() => {
    if (this.style.display == "none"){
      cy.fit();
      alert ("dit");
    }
  });
}