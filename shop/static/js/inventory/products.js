function submitProductUpdateForm(product_id, csrf_token) {
    //var edit_data = document.forms.namedItem('edit_form_id'+id)
    var formDataToSubmit = document.forms.namedItem('update_product_form_'+product_id);
    var formdata = new FormData(formDataToSubmit);
    var http = new XMLHttpRequest();
    var url = "/products/update_product";
    http.open('POST', url, true);
    http.setRequestHeader('Accept', 'application/json');
    http.setRequestHeader('Content-Type', 'multipart/form-data');
    //var params = 'product_id='+ product_id +'&value='+formdata.get('edit_input_'+id);
    console.log(formdata.get('image'))
    var object = {};
    formdata.forEach(function(value, key){
        console.log(key);
        if(key == 'image'){object[key] = formdata.get('image')}
        else{object[key] = value;}
    });
    var params = JSON.stringify(object);
    console.log(params);
    params['product_id'] = product_id;
    http.setRequestHeader('X-CSRFToken', csrf_token);
    http.send(params);
    http.onload = function(){
        data = http.responseText;
    }
}

function setSelectDefault(product_id, product_type, product_unit) {
    var select_p_type_field = document.getElementById("update_p_type_select_"+product_id);
    select_p_type_field.value = product_type;

    var select_unit_field = document.getElementById("update_unit_select_"+product_id);
    select_unit_field.value = product_unit;
}