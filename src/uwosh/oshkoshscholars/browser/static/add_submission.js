jQuery(function($) {

	// clean up the UI a bit
	$('ul.formTabs').hide();


	// hide Title and Summary fields
	// set their values from the Submission Title and Abstract fields

	$('#formfield-form-widgets-IDublinCore-title').hide();
	$('#formfield-form-widgets-IDublinCore-description').hide();

	$('#form-widgets-submission_title').on('blur', function() {
		title = $('#form-widgets-submission_title').val();
		$('#form-widgets-IDublinCore-title').val(title);
		abstract = $('#content').val() || '[insert abstract here]';
		$('#form-widgets-IDublinCore-description').val(abstract);
	});

	$('#content	').on('blur', function() {
		// XXX this does not work
		abstract = $('#content').val() || 'no abstract';
		$('#form-widgets-IDublinCore-description').val(abstract);
	});


	// wrap student fields

	$('#formfield-form-widgets-student_name,#formfield-form-widgets-student_email,#formfield-form-widgets-student_major,#formfield-form-widgets-student_phone,#formfield-form-widgets-student_bio').wrapAll(
		"<fieldset style='background: #eeeeee; border-style: solid;' id='student1'></fieldset>"
	);
	$('fieldset#student1').append("<legend for='student1'>Primary Student Author</legend>");

	$('#formfield-form-widgets-student_name2,#formfield-form-widgets-student_email2,#formfield-form-widgets-student_major2,#formfield-form-widgets-student_phone2,#formfield-form-widgets-student_bio2').wrapAll(
		"<fieldset style='background: #eeeeee; border-style: solid;' id='student2'></fieldset>"
	);
	$('fieldset#student2').append("<legend for='student2'>Student Author #2</legend>");

	$('#formfield-form-widgets-student_name3,#formfield-form-widgets-student_email3,#formfield-form-widgets-student_major3,#formfield-form-widgets-student_phone3,#formfield-form-widgets-student_bio3').wrapAll(
		"<fieldset style='background: #eeeeee; border-style: solid;' id='student3'></fieldset>"
	);
	$('fieldset#student3').append("<legend for='student3'>Student Author #3</legend>");

	$('#formfield-form-widgets-student_name4,#formfield-form-widgets-student_email4,#formfield-form-widgets-student_major4,#formfield-form-widgets-student_phone4,#formfield-form-widgets-student_bio4').wrapAll(
		"<fieldset style='background: #eeeeee; border-style: solid;' id='student4'></fieldset>"
	);
	$('fieldset#student4').append("<legend for='student4'>Student Author #4</legend>");

	$('#formfield-form-widgets-student_name5,#formfield-form-widgets-student_email5,#formfield-form-widgets-student_major5,#formfield-form-widgets-student_phone5,#formfield-form-widgets-student_bio5').wrapAll(
		"<fieldset style='background: #eeeeee; border-style: solid;' id='student5'></fieldset>"
	);
	$('fieldset#student5').append("<legend for='student5'>Student Author #5</legend>");


    // hide the extra student fields

    $('fieldset#student2').hide();
    $('fieldset#student3').hide();
    $('fieldset#student4').hide();
    $('fieldset#student5').hide();


    // buttons to show student fields on demand

    $('fieldset#student2').before("<br><a style='color: white; background: black;' href='javascript:void(0);' class='showstudent2'>+ show Student #2</a><br>"); 
    $(document).on("click", "a.showstudent2" , function() {
	    $('fieldset#student2').show(400);
	    $('a.showstudent2').hide();
    });

    $('fieldset#student3').before("<br><a style='color: white; background: black;' href='javascript:void(0);' class='showstudent3'>+ show Student #3</a><br>"); 
    $(document).on("click", "a.showstudent3" , function() {
	    $('fieldset#student3').show(400);
	    $('a.showstudent3').hide();
    });

    $('fieldset#student4').before("<br><a style='color: white; background: black;' href='javascript:void(0);' class='showstudent4'>+ show Student #4</a><br>"); 
    $(document).on("click", "a.showstudent4" , function() {
	    $('fieldset#student4').show(400);
	    $('a.showstudent4').hide();
    });

    $('fieldset#student5').before("<br><a style='color: white; background: black;' href='javascript:void(0);' class='showstudent5'>+ show Student #5</a><br>"); 
    $(document).on("click", "a.showstudent5" , function() {
	    $('fieldset#student5').show(400);
	    $('a.showstudent5').hide();
    });


    // wrap fields for faculty advisors

    $('#formfield-form-widgets-faculty_name,#formfield-form-widgets-faculty_email,#formfield-form-widgets-faculty_phone,#formfield-form-widgets-faculty_department').wrapAll(
		"<fieldset style='background: #eeeeee; border-style: solid;' id='faculty1'></fieldset>"
	);
	$('fieldset#faculty1').append("<legend for='faculty1'>Faculty Advisor</legend>");

    $('#formfield-form-widgets-faculty_name2,#formfield-form-widgets-faculty_email2,#formfield-form-widgets-faculty_phone2,#formfield-form-widgets-faculty_department2').wrapAll(
		"<fieldset style='background: #eeeeee; border-style: solid;' id='faculty2'></fieldset>"
	);

    // hide the extra faculty advisor fields

	$('fieldset#faculty2').append("<legend for='faculty2'>Faculty Advisor #2</legend>");

	$('fieldset#faculty2').hide();


    // button to show faculty advisor #2 on demand

    $('fieldset#faculty2').before("<br><br><a style='color: white; background: black;'href='javascript:void(0);' class='showfac2'>+ show Faculty Advisor #2 </a><br>"); 
    $(document).on("click", "a.showfac2" , function() {
	    $('fieldset#faculty2').show(400);
	    $('a.showfac2').hide();
	});


	// wrap author agreement fields
	$('#formfield-form-widgets-not_been_submitted,#formfield-form-widgets-does_not_contain,#formfield-form-widgets-obtained_irb_or_iacuc,#formfield-form-widgets-have_read_guidelines,#formfield-form-widgets-will_attend,#formfield-form-widgets-will_make_effort').wrapAll(
		"<fieldset style='background: #eeeeee; border-style: solid;' id='author-agreement'>"
	);
	$('fieldset#author-agreement').prepend("<legend for='author-agreement'>Author Agreement</legend><h3>The primary author certifies that:</h3><br>");

	// enforce only yes answers on author agreement questions
	$('#form-widgets-not_been_submitted-1, #form-widgets-does_not_contain-1, #form-widgets-obtained_irb_or_iacuc-1, #form-widgets-have_read_guidelines-1, #form-widgets-will_attend-1, #form-widgets-will_make_effort-1').click(function() {
		alert('You must answer \'yes\' to all author agreement questions');
		return false;
	});

	// enforce minimal email values

	$('#form-widgets-student_email').on('blur', function() {
		val = $(this).val();
		res = val.match(/.@.+\..+/);
		if (res == null || res.length == 0) { alert('invalid email address: ' + val); }
	    });

	$('#form-widgets-student_email2').on('blur', function() {
		val = $(this).val();
		res = val.match(/.@.+\..+/);
		if (res == null || res.length == 0) { alert('invalid email address: ' + val); }
	    });

	$('#form-widgets-student_email3').on('blur', function() {
		val = $(this).val();
		res = val.match(/.@.+\..+/);
		if (res == null || res.length == 0) { alert('invalid email address: ' + val); }
	    });

	$('#form-widgets-student_email4').on('blur', function() {
		val = $(this).val();
		res = val.match(/.@.+\..+/);
		if (res == null || res.length == 0) { alert('invalid email address: ' + val); }
	    });

	$('#form-widgets-student_email5').on('blur', function() {
		val = $(this).val();
		res = val.match(/.@.+\..+/);
		if (res == null || res.length == 0) { alert('invalid email address: ' + val); }
	    });

	$('#form-widgets-faculty_email').on('blur', function() {
		val = $(this).val();
		res = val.match(/.@.+\..+/);
		if (res == null || res.length == 0) { alert('invalid email address: ' + val); }
	    });

	$('#form-widgets-faculty_email2').on('blur', function() {
		val = $(this).val();
		res = val.match(/.@.+\..+/);
		if (res == null || res.length == 0) { alert('invalid email address: ' + val); }
	    });
});