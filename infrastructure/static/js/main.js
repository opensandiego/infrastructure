$(document).ready(function() {
  $('#nav').on('click','#search', function() {
    value = $(this).val()
    if(value == "Search...") {
      $(this).val('');
    }
  }).on('blur', '#search', function() {
    value = $(this).val()
    if(value == '') {
      $(this).val('Search...');
    }
  });
  $( "form#projects-filter" ).on( "submit", function( event ) {
    event.preventDefault();
    form_data = $(this).serialize();
    $.ajax({
      url: '/projects_list',
      data: form_data,
    }).done(function(data) { 
      $('#project-list').html(data);
    });
  });
  $(document).on("click", ".remote #pagination a", function(event) {
    event.preventDefault();
    $('form #page').val($(this).data('page'));
    $('form').submit();
  });
  $('#projects_filter').on('click', '#submit', function(event) {
    $('form #page').val('1');
  });
  if($('#project').length > 0) {
    project_width =  $('#project').width();
    project_id = $('#project').data('id');
    first_column_width = $('#project #map').width();
    proj4.defs('EPSG:2230', '+proj=lcc +lat_1=33.88333333333333 +lat_2=32.78333333333333 +lat_0=32.16666666666666 +lon_0=-116.25 +x_0=2000000.0001016 +y_0=500000.0001016001 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs');
    var map = L.mapbox.map('map', 'milafrerichs.map-ezn7qjpd')
    .setView([32.70752, -117.15706], 14);

    geojsonFeature = JSON.parse(geojson);
    geojsonFeature["crs"]["properties"]["name"] = "urn:ogc:def:crs:EPSG::2230";
    marker = L.Proj.geoJson(geojsonFeature).addTo(map);
    map.fitBounds(marker.getBounds());
    map.setZoom(14);

    cost_data = $('#project-cost').data('cost').split(',');
    cost_data = cost_data.map(function(d) { return parseInt(d); });
    cost_labels = $('#project-cost').data('cost-labels').split(',');
    cost_x_scale = d3.scale.ordinal().rangeRoundBands([0, first_column_width-20], .1).domain(cost_data);
    cost_x_axis_scale = d3.scale.ordinal().rangeRoundBands([0, first_column_width-20], .1).domain(cost_labels);
    cost_y_scale = d3.scale.linear().range([100,0]).domain([0, d3.max(cost_data)]);
    var svg_element = d3.select('#cost-breakdown').append('svg').attr('height','160').attr('width',first_column_width).append('g').attr('transform','translate(20,20)');
    svg_element.selectAll('rect').data(cost_data).enter().append('rect').attr('x',function(d) { return cost_x_scale(d); }).attr("width", cost_x_scale.rangeBand()).attr('y', function(d) {return cost_y_scale(d)}).attr('height',function(d) {return 120-cost_y_scale(d);}).attr("fill","#AAB3AB");
    x_axis = d3.svg.axis().scale(cost_x_axis_scale).orient('bottom');
    svg_element.append('g').attr('class','axis x').attr("transform", "translate(0,120)").call(x_axis);
  }

  if($('#main').length > 0) {
    markers = new L.MarkerClusterGroup();
    proj4.defs('EPSG:2230', '+proj=lcc +lat_1=33.88333333333333 +lat_2=32.78333333333333 +lat_0=32.16666666666666 +lon_0=-116.25 +x_0=2000000.0001016 +y_0=500000.0001016001 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs');
    $.getJSON('/projects/', function(data) {
      $.each(data, function(index, project) {
        geojsonFeature = JSON.parse(project.geometry);
        if(geojsonFeature) {
          geojsonFeature["properties"]["marker-symbol"] = project.asset_image;
          geojsonFeature["properties"]["marker-size"] = "medium";
          geojsonFeature["properties"]["marker-color"] = project.asset_color;
          geojsonFeature["properties"]["stroke"] = project.asset_color;
          geojsonFeature["properties"]["color"] = project.asset_color;
          var marker = L.Proj.geoJson(geojsonFeature, {
            pointToLayer: L.mapbox.marker.style,
            style: function(feature) {
              return feature.properties; 
            }
          });
          var markerContent = "<h3>"+project.SP_PROJECT_NM+"</h3><a href='/cip/project/"+project.id+"'>Detail</a>"
          marker.bindPopup(markerContent);
          markers.addLayer(marker);
        }
      });
      map.addLayer(markers);
    });
    var map = L.mapbox.map('map', 'milafrerichs.map-ezn7qjpd')
    .setView([32.70752, -117.15706], 11);
  }
  if($('#project-list .tabs').length > 0) {
    $('#project-list').on('click', '.tabs li a',function(e) {
      $('.tab-view').hide();
      $('#' + $(this).data('tab')).show();
      $('#project-list .tabs li').removeClass('active');
      $(this).parent('li').addClass('active');
    });
  }
});
