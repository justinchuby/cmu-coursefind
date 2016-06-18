//$('.datepicker').pickadate({
//    selectMonths: true, // Creates a dropdown to control month
//    selectYears: true, // Creates a dropdown of 15 years to control year
//    format: 'd mmm, yyyy',
//  });
//
//$('.timepicker').pickatime({
//      twelvehour: false
//    });

// Initialize collapse button
$(".button-collapse").sideNav();
// Initialize collapsible (uncomment the line below if you use the dropdown variation)
//$('.collapsible').collapsible();

// clearForm() from http://stackoverflow.com/questions/6653556/jquery-javascript-function-to-clear-all-the-fields-of-a-form answer by ktamlyn
function clearForm()
{
    $(':input').not(':button, :submit, :reset, :hidden, :checkbox, :radio').val('');
    $(':checkbox, :radio').prop('checked', false);
    $('#search-text').focus();
}
