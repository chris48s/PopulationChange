$(document).ready(function() {
	
	google.load('visualization', '1', {packages: ['corechart']});
	google.setOnLoadCallback(drawChart([]));
	
	//add data to chart
	function drawChart(data_array) {
		
		var data = new google.visualization.DataTable();
		
		//set up columns
		data.addColumn('string', 'Year');
		data.addColumn('number', 'Census (linear interpolation)');
		data.addColumn('number', 'Mid-Year Population Estimates (revised)');
		data.addColumn('number', 'Mid-Year Population Estimates (superseded)');
		
		//add our data
		data.addRows(data_array);
		
		//chart options
		var options = {
			width: 1000,
			height: 500,
			interpolateNulls: true,
			hAxis: {
				title: 'Year'
			},
			vAxis: {
				title: 'Population'
			}
		};
		
		var chart = new google.visualization.LineChart(
			document.getElementById('chart'));
		
		//draw it
		chart.draw(data, options);
	}
	
	
	$('#submit').on('click', function() {
		
		//erase existing chart data
		drawChart([]);
		$('#status').text('Loading...');
		
		//grab new data from server
		$.ajax({
			dataType:	'json',
			url:		'get_chart_json/',
			data: 		{ 'LA': $('#LA').val() }
		}).done(function(data) {
			drawChart(data);
			$('#status').text('Done.');
		}).fail(function() {
			$('#status').text('Failed.');
		});
		
	});
	
});
