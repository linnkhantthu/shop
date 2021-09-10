var c_id_list = [];
var c_id_dict = {}
function choices_trash(c_id) {
    var temp = ""
    temp = c_id.replace('div', '');
    hide_tag('div'+temp)
    c_id_dict['id'] = parseInt(temp);
    c_id_list.push(c_id_dict)
    c_id_dict = {}
}
function submit_choices(url) {
    var success_list = [];
    var success_list_str = "";
    var fail_list = [];
    var fail_list_str = "";
    var csrf_token = document.getElementById("csrf_token").getAttribute("value");
    var http = new XMLHttpRequest();
    http.open('post', url);
    http.setRequestHeader('content-type', 'application/json');
    http.setRequestHeader('X-CSRFToken', csrf_token);
    http.onload = function(){
        var response = JSON.parse(http.responseText);
        response.forEach(res => {
            var p_id = res['id']
            var product_name = res['product_name'];
            var status = res['status'];
            if (status) {
                success_list.push(product_name);
            }
            else{
                show_tag('div'+p_id);
                fail_list.push(product_name);
            }
        });

        success_list.forEach((sl, index) => {
            if(index == success_list.length - 2){
                success_list_str += sl + ' and ';
            }
            else if(index == success_list.length - 1){
                success_list_str += sl + '.';
            }
            else{
                success_list_str += sl + ',';
            }
            removeOptionFromSelect('prod_type', sl);
        });
        fail_list.forEach((sl, index) => {
            if(index == fail_list.length - 2){
                fail_list_str += sl + ' and ';
            }
            else if(index == fail_list.length - 1){
                fail_list_str += sl + '.';
            }
            else{
                fail_list_str += sl + ',';
            }
        });
        if (fail_list_str != "" && success_list_str != "") {
            document.getElementById('flash-msg').innerHTML =
                '<div class="alert alert-info">'+
                    'Deleted: ' + success_list_str +
                   'Could not delete: '+ fail_list_str +
                '</div>';
        }
        else if(fail_list_str == "" && success_list_str != ""){
            document.getElementById('flash-msg').innerHTML =
                '<div class="alert alert-info">'+
                    'Deleted: ' + success_list_str +
                '</div>';
        }
        else if(fail_list_str != "" && success_list_str == ""){
            document.getElementById('flash-msg').innerHTML =
                '<div class="alert alert-info">'+
                'Could not delete: '+ fail_list_str +
                '</div>';
        }
        else{
            // nothing will happen
        }
        // reinitialize the list because I don't want to reload the page.
        c_id_list = []

    }
    http.send(JSON.stringify(c_id_list));
}

//no need to remove a tag
function hide_tag(id) {
    var x = document.getElementById(id);
    x.style.display = "none";
}
function show_tag(id) {
    var x = document.getElementById(id);
    x.style.display = "block";
}

//remove desired option from select
function removeOptionFromSelect(id, value) {
    var selectObj = document.getElementById(id);
    for(var i=0; i<selectObj.length;i++){
        if(selectObj.options[i].value == value){
            selectObj.remove(i);
        }
    }
}

//edit desired option from select
function editOptionFromSelect(id, old_value, new_value) {
    var selectObj = document.getElementById(id);
    for(var i=0; i<selectObj.length;i++){
        if(selectObj.options[i].value == old_value){
            selectObj.options[i].value = new_value;
            selectObj.options[i].innerHTML = new_value;
        }
    }
}

// choices_edit
var pt_choice_id_list = []
function choices_edit(id, edit_choice_id, url, csrf_token) {
    var temp = ""
    temp = id.replace('div', '');
    pt_choice_id_list.push(parseInt(temp));
    var choice_span = document.getElementById(edit_choice_id);

    //create_form
    var edit_pt_form = document.createElement('form');
    edit_pt_form.setAttribute('action', '');
    edit_pt_form.setAttribute('method', 'post');
    edit_pt_form.setAttribute('name', 'edit_form_id'+temp);
    edit_pt_form.setAttribute('onsubmit', 'return false');

    //create input
    var edit_input = document.createElement('input');
    edit_input.setAttribute('type', 'text');
    edit_input.setAttribute('name', 'edit_input_'+temp);
    edit_input.setAttribute('id', 'edit_input_'+temp);
    edit_input.setAttribute('value', choice_span.textContent);

    var old_choice_value = choice_span.textContent;

    //submit icon
    var edit_submit_icon = document.createElement('i');
    edit_submit_icon.setAttribute('class', 'fa fa-check')
    edit_submit_icon.setAttribute('style', 'margin-left:2px; color:green;, font-size:10px;')
    edit_submit_icon.setAttribute('id', 'edit_submit_id'+temp);
    edit_submit_icon.setAttribute('onClick', 'submit_pt_func("'+temp+'", "'+url+'", "'+csrf_token+'", "'+old_choice_value+'")');


    //append input to form
    edit_pt_form.appendChild(edit_input);
    edit_pt_form.appendChild(edit_submit_icon);

    //hide edit icon
    hide_tag('edit_icon_id'+temp);

    //append form to span
    choice_span.innerHTML = ""; // remove inner text
    choice_span.appendChild(edit_pt_form);

}

function submit_pt_func(id, url, csrf_token, old_choice_value) {
    var edit_data = document.forms.namedItem('edit_form_id'+id)
    var formdata = new FormData(edit_data);
    var http = new XMLHttpRequest();
    http.open('POST', url, true);
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    var params = 'id='+ id +'&value='+formdata.get('edit_input_'+id);
    var new_choice_value = formdata.get('edit_input_'+id);
    http.setRequestHeader('X-CSRFToken', csrf_token);
    http.send(params);
    http.onload = function(){
        data = http.responseText;
        var choice_span = document.getElementById('span_pt_choices'+id);
        if(data == 'true'){
            choice_span.innerHTML = new_choice_value;
            editOptionFromSelect('prod_type', old_choice_value, new_choice_value);
            show_tag('edit_icon_id'+id)
        }
        else{
            var error_tag = document.createElement('small');
            error_tag.innerHTML = data;
            choice_span.appendChild(error_tag);
        }
    }
}