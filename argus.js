function InteractiveTrainer(workarea) {
	this.workarea = $(workarea);
	this.all_divs = [];
	this.is_selected_element = -1;
	this.offset = [];
/*
	this.workarea.html(
'		<div class="col-md-8">'+
'			<div style="margin:1em">'+
'				<img id="target" class="img-responsive">'+
'			</div>'+
'		</div>'+
'		<div class="col-md-4">'+
'			<div style="margin:1em">'+
'				<input id="updatebtn" type="button" class="btn" value="Update">'+
'			</div>'+
'		</div>'
	);
*/
	this.jcrop_api = null;
	

}

InteractiveTrainer.prototype = {

		show_image: function(labels) {
	
			console.log(labels);
//			var img = $('img', this.workarea);
//			img.attr('src', 'image.jpg');
			console.log(typeof(labels));

			for (i = 0; i < labels.length; i++) {
			//for (var label in JSON.parse(labels)) {
				var _x = labels[i][1][0];
				var _y = labels[i][1][1]; 
				var _w = labels[i][1][2];
				var _h = labels[i][1][3];
		
				var $div = $('<div />').width(_w).height(_h).css({
					position: 'absolute',
					zIndex: 2000,
					top: _x,
					left: _y,
					border: "2px solid #ff0000",
					background: "rgba(0, 255, 127, 0.3)",
					
							
				});
			
				$div.attr("id", i);
				$div.append("<p>"+labels[i][2]+"</p>")
				console.log("Pringint labels " + labels[i]);
				var selfObj = this;

				//var is_selected_element = this.is_selected_element;
				$div.mousedown(

					function(e){
						selfObj.is_selected_element = parseInt($(this).attr('id'));
						$(this).hide();
						var x1 = $(this).css('left');
						x1 = parseInt(x1)
						var y1 = $(this).css('top');
						y1 = parseInt(y1);
						var width = $(this).width()
						var height = $(this).height();
				
						var x2 = x1 + width;
						var y2 = y1 + height;
				
						selfObj.jcrop_api.setSelect([x1,y1,x2,y2]);
						selfObj.hide_other_elements($(this).attr('id'));
						return false;
					}
	
				);

				var $img = $('.jcrop-holder');
				
				$img.click(function(e) {
					console.log("mouse position " + e.pageX + e.pageY);
				});
				$img.append($div).css({
					position : 'absolute'
		    		});
				this.all_divs.push($div);
			}
			
			

	
		},

		learn_features: function() {
			console.log('learn_features');
			// call $.ajax POST on api.php with op "learn_features"
		},

		identify_objects: function(frm) {
			console.log('identify_objects');
			console.log(frm);
			
			
			var form = document.getElementById('file-form');
			var fileSelect = document.getElementById('file-select');
			var uploadButton = document.getElementById('upload-button');
			var files = fileSelect.files;
			var formData = new FormData();
			var file = files[0];
			var labels = [];
			formData.append('test_image', file, file.name);

			var xhr = new XMLHttpRequest();
			xhr.open('POST', 'api.php?op=identify_objects', false);

			xhr.onload = function () {
				if (xhr.status === 200) {
					//console.log(xhr.responseText);
					response =  JSON.parse(xhr.responseText) ;
					//console.log(response)
					//var _id = response._id;
					//var label1 = response.labels.label1._id;
		    			// File(s) uploaded.
					uploadButton.innerHTML = 'Upload';
				} else {
					alert('An error occurred!');
				}
			};

			xhr.send(formData);	
			

			
			var _id = response._id;
			var _labels = response.labels;
			for (i=0; i<_labels.length; i++) {
				var label_id = _labels[i]._id;
				var box = _labels[i].box[0].concat(_labels[i].box[1]);
				var tag = _labels[i].tag;
				//item["label_id"] = label_id;
				//item["box"] = box;
				labels.push([label_id, box, tag]);
			}
			
		
			// send image to api.php using $.ajax POST request with op "identify_objects"
			//var labels = { _id: "1", labels: [] }; // get labels from ajax result
			this.activate_jcrop();
			this.offset[0] = $('.jcrop-holder').offset().left;
			this.offset[1] = $('.jcrop-holder').offset().top;
			this.show_image(labels);
			
			var $img = $('.jcrop-holder');
			var selfObj = this;
			this.update_z_values();

			
		},

		update_z_values: function() {
			for (var i=0; i<this.all_divs.length; i++) {
				var outer_div = this.all_divs[i];
				var outer_div_x = parseInt(outer_div.css('left'));
				var outer_div_y = parseInt(outer_div.css('top'));
				var outer_div_width = outer_div.width();
				var outer_div_height = outer_div.height();
				var outer_last_corner_x = outer_div_x + outer_div_width;
				var outer_last_corner_y = outer_div_y + outer_div_height;
				for (var j=0; j<this.all_divs.length; j++) {
					if (i!= j) {
						var inner_div = this.all_divs[j];
						var inner_div_x = parseInt(inner_div.css('left'));
						var inner_div_y = parseInt(inner_div.css('top'));
						var inner_div_width = inner_div.width();
						var inner_div_height = inner_div.height();
						var inner_last_corner_x = inner_div_x + inner_div_width;
						var inner_last_corner_y = inner_div_y + inner_div_height;
						if ((outer_div_x < inner_div_x) && (outer_div_y < inner_div_y) && (outer_last_corner_x > inner_last_corner_x) && (outer_last_corner_y > inner_last_corner_y)) {
							inner_div.css('z-index', outer_div.css('z-index') + 1);
							//console.log(parseInt(inner_div.css("z-index")) + 1);
						} 
				
					}					
				}
			}

		},

		
		activate_jcrop: function() {
			var self_obj = this;

			jQuery(function($) {
				$('#target').Jcrop({
 		 		}, function() {
					self_obj.jcrop_api = this;
				});
			});
		},
	
		hide_other_elements: function(index) {

			var outer_div = this.all_divs[index];
			var outer_div_x = parseInt(outer_div.css('left'));
			var outer_div_y = parseInt(outer_div.css('top'));
			var outer_div_width = outer_div.width();
			var outer_div_height = outer_div.height();
			var outer_last_corner_x = outer_div_x + outer_div_width;
			var outer_last_corner_y = outer_div_y + outer_div_height;
			for (var i=0; i < this.all_divs.length; i++) {

				if (i!= index) {
					var inner_div = this.all_divs[i];
					var inner_div_x = parseInt(inner_div.css('left'));
					var inner_div_y = parseInt(inner_div.css('top'));
					var inner_div_width = inner_div.width();
					var inner_div_height = inner_div.height();
					var inner_last_corner_x = inner_div_x + inner_div_width;
					var inner_last_corner_y = inner_div_y + inner_div_height;
					if ((outer_div_x > inner_div_x) && (outer_div_y > inner_div_y) && (outer_last_corner_x < inner_last_corner_x) && (outer_last_corner_y < inner_last_corner_y)) {
						inner_div.hide();
						} 
				
						

					if (((outer_div_x < inner_div_x < outer_last_corner_x) && (outer_div_y < inner_div_y < outer_last_corner_y)) || ((outer_div_x < inner_div_x + inner_div_width < outer_last_corner_x) && (outer_div_y < inner_div_y < outer_last_corner_y)) || ((outer_div_x < inner_div_x < outer_last_corner_x) && (outer_div_y < inner_div_y + inner_div_height < outer_div_last_corner_y)) || ((outer_div_x < inner_div_x + inner_div_width < outer_last_corner_x) && (outer_div_y < inner_div_y + inner_div_height < outer_div_last_corner_y)))    {
				

						inner_div.hide();			
				
					}
				}
			}
			
		}

};

function start() {
	
	it = new InteractiveTrainer($('#workarea'));
	$('#upload-button').click(function(e) {
		e.preventDefault();
		it.identify_objects(this);
	});

	
	$('#crop').click(function(e) {
		console.log(it.is_selected_element);
		
		//for(j=0; j<it.all_divs.length; j++) {
			if (it.is_selected_element >= 0) {
				console.log('it is selected element');	
				new_coordinates = it.jcrop_api.tellSelect();
				new_h = new_coordinates.h;
				new_w = new_coordinates.w;
				new_x1 = new_coordinates.x;
				new_x2 = new_coordinates.x2
				new_y1 = new_coordinates.y;
				new_y2 = new_coordinates.y2;
				if (it.all_divs[it.is_selected_element].text() !=  $('#tag').val()) {
					it.all_divs[it.is_selected_element].text(($('#tag').val()));
				}
				console.log(it.all_divs[it.is_selected_element].text());
				it.all_divs[it.is_selected_element].width(new_w).height(new_h).css({
					top: new_y1,
					left: new_x1
				})
				it.all_divs[it.is_selected_element].show()
				it.is_selected_element = -1
				it.jcrop_api.release();
				it.update_z_values();
				for (var i=0; i < it.all_divs.length; i++) {	
					it.all_divs[i].show();
				}
				$("tag").val("");
				return false;

			}
			else {
				new_coordinates = it.jcrop_api.tellSelect();
				_h = new_coordinates.h;
				_w = new_coordinates.w;
				_x = new_coordinates.x;
				_x2 = new_coordinates.x2
				_y = new_coordinates.y;
				_y2 = new_coordinates.y2;
			
				
				$tag = $('#tag').val();
				var $div = $('<div />').width(_w).height(_h).css({
					position: 'absolute',
					zIndex: 2000,
					left: _x,
					top: _y,
					border: "2px solid #ff0000",
					background: "rgba(0, 255, 127, 0.3)",
							
				});
				$div.append("<p>"+$tag+"</p>")
			
				$div.attr("id", it.all_divs.length);


				//var selfObj = this;
/*
				$div.mouseover().css({
						cursor: 'move'
				});
*/				

				//var is_selected_element = this.is_selected_element;
				$div.mousedown(

					function(e){
						it.is_selected_element = parseInt($(this).attr('id'));
						$(this).hide();
						var x1 = $(this).css('left');
						x1 = parseInt(x1)
						var y1 = $(this).css('top');
					y1 = parseInt(y1);
					var width = $(this).width()
					var height = $(this).height();
				
					var x2 = x1 + width;
					var y2 = y1 + height;
				
					it.jcrop_api.setSelect([x1,y1,x2,y2]);
					it.hide_other_elements($(this).attr('id'));
					return false;
				}
	
				);

				var $img = $('.jcrop-holder');
			
				$img.append($div).css({
					position : 'absolute'
		    		});
				it.all_divs.push($div);
				it.jcrop_api.release();
				it.update_z_values();
				return false;
			}

			
		//}
	})

	

	$('#updatebtn').on('click', this.learn_features);
}

function previewFile() {
  	var preview = document.querySelector('img');
  	var file    = document.querySelector('input[type=file]').files[0];
  	var reader  = new FileReader();
	
	reader.onloadend = function () {
		preview.src = reader.result;
	}

	if (file) {
		reader.readAsDataURL(file);
	} else {
		preview.src = "";
	}
}

$(document).ready(start);
