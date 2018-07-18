var cy = cytoscape({
  container: document.getElementById('cy'),

  boxSelectionEnabled: false,
  autounselectify: true,

  style: cytoscape.stylesheet()
    .selector('node')
      .css({
        'height': 80,
        'width': 80,
        'background-fit': 'cover',
        'border-color': '#000',
        'border-width': 3,
        'border-opacity': 0.5
      })
    .selector('edge')
      .css({
        'curve-style': 'bezier',
        'width': 6,
        'target-arrow-shape': 'triangle',
        'line-color': '#ffaaaa',
        'target-arrow-color': '#ffaaaa'
      })
    
		.selector('#0')
		  .css({
			'background-image': '0.png'
		  })
		.selector('#1')
		  .css({
			'background-image': '1.png'
		  })
		.selector('#2')
		  .css({
			'background-image': '2.png'
		  })
		.selector('#3')
		  .css({
			'background-image': '3.png'
		  })
		.selector('#1')
		  .css({
			'background-image': '1.png'
		  })
		.selector('#4')
		  .css({
			'background-image': '4.png'
		  })
		.selector('#5')
		  .css({
			'background-image': '5.png'
		  })
		.selector('#6')
		  .css({
			'background-image': '6.png'
		  })
		.selector('#7')
		  .css({
			'background-image': '7.png'
		  })
		.selector('#8')
		  .css({
			'background-image': '8.png'
		  })
		.selector('#4')
		  .css({
			'background-image': '4.png'
		  })
		.selector('#5')
		  .css({
			'background-image': '5.png'
		  })
		.selector('#6')
		  .css({
			'background-image': '6.png'
		  })
		.selector('#7')
		  .css({
			'background-image': '7.png'
		  })
		.selector('#8')
		  .css({
			'background-image': '8.png'
		  })
		.selector('#2')
		  .css({
			'background-image': '2.png'
		  })
		.selector('#9')
		  .css({
			'background-image': '9.png'
		  })
		.selector('#10')
		  .css({
			'background-image': '10.png'
		  })
		.selector('#11')
		  .css({
			'background-image': '11.png'
		  })
		.selector('#12')
		  .css({
			'background-image': '12.png'
		  })
		.selector('#13')
		  .css({
			'background-image': '13.png'
		  })
		.selector('#9')
		  .css({
			'background-image': '9.png'
		  })
		.selector('#10')
		  .css({
			'background-image': '10.png'
		  })
		.selector('#11')
		  .css({
			'background-image': '11.png'
		  })
		.selector('#12')
		  .css({
			'background-image': '12.png'
		  })
		.selector('#13')
		  .css({
			'background-image': '13.png'
		  })
		.selector('#3')
		  .css({
			'background-image': '3.png'
		  })
		.selector('#14')
		  .css({
			'background-image': '14.png'
		  })
		.selector('#15')
		  .css({
			'background-image': '15.png'
		  })
		.selector('#14')
		  .css({
			'background-image': '14.png'
		  })
		.selector('#15')
		  .css({
			'background-image': '15.png'
		  }),

  elements: {
    nodes: [
      { data: { id: '0' } },{ data: { id: '1' } },{ data: { id: '2' } },{ data: { id: '3' } },{ data: { id: '1' } },{ data: { id: '4' } },{ data: { id: '5' } },{ data: { id: '6' } },{ data: { id: '7' } },{ data: { id: '8' } },{ data: { id: '4' } },{ data: { id: '5' } },{ data: { id: '6' } },{ data: { id: '7' } },{ data: { id: '8' } },{ data: { id: '2' } },{ data: { id: '9' } },{ data: { id: '10' } },{ data: { id: '11' } },{ data: { id: '12' } },{ data: { id: '13' } },{ data: { id: '9' } },{ data: { id: '10' } },{ data: { id: '11' } },{ data: { id: '12' } },{ data: { id: '13' } },{ data: { id: '3' } },{ data: { id: '14' } },{ data: { id: '15' } },{ data: { id: '14' } },{ data: { id: '15' } },
    ],
    edges: [
      { data: { source: '0', target: '1' } },{ data: { source: '0', target: '2' } },{ data: { source: '0', target: '3' } },{ data: { source: '1', target: '4' } },{ data: { source: '1', target: '5' } },{ data: { source: '1', target: '6' } },{ data: { source: '1', target: '7' } },{ data: { source: '1', target: '8' } },{ data: { source: '2', target: '9' } },{ data: { source: '2', target: '10' } },{ data: { source: '2', target: '11' } },{ data: { source: '2', target: '12' } },{ data: { source: '2', target: '13' } },{ data: { source: '3', target: '14' } },{ data: { source: '3', target: '15' } },
    ]
  },

  layout: {
    name: 'breadthfirst',
    //circle: true,
    root: '0',
	minDist: 40
  },
});