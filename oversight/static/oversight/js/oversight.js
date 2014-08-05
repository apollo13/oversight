$(document).ready(function(){
	render_plot('chart');
});

var render_plot = function(id) {
	var url = $('#'+id).data('url');

	$.ajax({
		url: url,
		dataType:"json",
		success: function(response) {
			var log_plot = false;
			var data = [];
			var series = []
			$.each(response, function(index, value) {
				data.push($.map(value.points, function(elem, index) {
					return [[new Date(elem[0]), parseFloat(elem[1])]];
				}));
				series.push({showMarker: false,
                     logPlot: value.log_plot,
                     label: value.name});
				if (value.log_plot) {
					log_plot = true;
				}
			});
			$.each(series, function(index, value) {
				if (log_plot && !value.logPlot) {
					value.yaxis = 'y2axis';
				}
			});
			var yaxis = {};
			if (log_plot) {
				yaxis = {
					renderer: $.jqplot.LogAxisRenderer,
					syncTicks: true,
					tickOptions: {
						formatString: "%.2e",
					}
				};
			}
			$.jqplot(id, {
				title: "",
				data: data,
				axes: {
					xaxis: {
						renderer:$.jqplot.DateAxisRenderer,
						tickRenderer: $.jqplot.CanvasAxisTickRenderer,
						tickOptions: {
							angle: -30,
							fontSize: '10pt'
						}
					},
					yaxis: yaxis,
				},
				legend: {
					show: true,
					location: 'nw'
				},
				series: series
			});
		}
	});
};
