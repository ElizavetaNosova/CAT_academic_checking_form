	$('#docx-file').change(function() {
		$('#docx-form').ajaxSubmit({
			method: 'post',
			type: 'post',
			url: '/upload_docx_file',
			success: function(data) {
				// После загрузки файла очистим форму.
				console.log(data);
				//window.location.replace(encodeURI("/spelling_form?file_id=" + data.file_id));
			}
		// }).done(function(data) {
		// 		// После загрузки файла очистим форму.
		// 		console.log(data);
		// 		//window.location.replace(encodeURI("/spelling_form?file_id=" + data.file_id));
		// 	});
	});