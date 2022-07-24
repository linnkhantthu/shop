function submitProductUpdateForm(product_id, csrf_token) {
    //var edit_data = document.forms.namedItem('edit_form_id'+id)
    var formDataToSubmit = document.forms.namedItem('update_product_form_'+product_id);
    var formdata = new FormData(formDataToSubmit);
    formdata.append('product_id', parseInt(product_id));
    var http = new XMLHttpRequest();
    var url = "/products/update_product";
    http.open('POST', url, true);
    //http.setRequestHeader('Content-Type', 'multipart/form-data');
    //var params = 'name='+formdata.get('name')+'&'+'image='+formdata.get('image');
    http.setRequestHeader('X-CSRFToken', csrf_token);
    http.send(formdata);
    http.onload = function(){
        var data = JSON.parse(http.responseText);
        var result = data['result'];
        if(result.length != 0){
            var result_str;
            result.forEach(e => {
                result_str += e + '\n';
            });
            alert(result_str);
        }
        else{
            var table_name = document.getElementById('table_name_'+product_id);
            var table_image = document.getElementById('table_image_'+product_id);
            var table_type = document.getElementById('table_p_type_'+product_id);
            var table_unit = document.getElementById('table_unit_'+product_id);
            var table_price = document.getElementById('table_price_'+product_id);
            var table_image_modal = document.getElementById('table_image_modal_'+product_id);
            var table_price_modal_span = document.getElementById('table_price_modal_span_'+product_id);
            var table_unit_modal_span = document.getElementById('table_unit_modal_span_'+product_id);
            
            table_name.innerHTML = formdata.get('name');
            table_type.innerHTML = formdata.get('p_type');
            table_unit.innerHTML = formdata.get('unit');
            table_price.innerHTML = formdata.get('price');
            table_price_modal_span.innerHTML = formdata.get('price');
            table_unit_modal_span.innerHTML = formdata.get('unit');
            
            if(formdata.get('image').name != ''){
                table_image.src = "/static/products_images/"+data['image_filename'];
                table_image_modal.src = "/static/products_images/"+data['image_filename'];
            }

        }
    }
}

function setSelectDefault(product_id, product_type, product_unit) {
    var select_p_type_field = document.getElementById("update_p_type_select_"+product_id);
    select_p_type_field.value = product_type;

    var select_unit_field = document.getElementById("update_unit_select_"+product_id);
    select_unit_field.value = product_unit;
}

function deleteProduct(product_id) {
    product_id = parseInt(product_id);
    var http = new XMLHttpRequest();
    var url = "/products/delete/"+product_id;
    http.open('GET', url, true);
    http.send();
    http.onload = function(){
        var data = JSON.parse(http.responseText);
        if(data['status'] == true){
            document.getElementById('flash-msg').innerHTML =
                '<div class="alert alert-info">'+
                    data['result'] +
                '</div>';
            var table_row = document.getElementById('table_row_'+product_id);
            table_row.remove();
        }
        else{
            document.getElementById('flash-msg').innerHTML =
                '<div class="alert alert-danger">'+
                    data['result'] +
                '</div>';
        }
    }
}