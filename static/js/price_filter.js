const rangeInput = document.querySelectorAll(".range-input input"),
priceInput = document.querySelectorAll(".price-input input"),
range = document.querySelector(".slider .progress");
let priceGap = 100;

priceInput.forEach(input =>{
    input.addEventListener("input", e =>{
        let minPrice = parseInt(priceInput[0].value),
        maxPrice = parseInt(priceInput[1].value);

        if((maxPrice - minPrice >= priceGap) && maxPrice <= rangeInput[1].max){
            if(e.target.className === "input-min"){
                rangeInput[0].value = minPrice;
                range.style.left = ((minPrice / rangeInput[0].max) * 100) + "%";
            }else{
                rangeInput[1].value = maxPrice;
                range.style.right = 100 - (maxPrice / rangeInput[1].max) * 100 + "%";
            }
        }
    });
});

rangeInput.forEach(input =>{
    input.addEventListener("input", e =>{
        minVal = parseInt(rangeInput[0].value),
        maxVal = parseInt(rangeInput[1].value);

        order_by = $("#order_by").val();
        page = $('.page-item').parent().find('li.active').find('a').data('value');
        var catagory = []
        var markedCheckbox = document.getElementsByName('cat');
        for (var checkbox of markedCheckbox) {
            if (checkbox.checked)
                catagory.push(checkbox.value)
        }

        var size = []
        var markedCheckbox = document.getElementsByName('pro_size');
        for (var checkbox of markedCheckbox) {
            if (checkbox.checked)
                size.push(checkbox.value)
        }

        var design = []
        var markedCheckbox = document.getElementsByName('design');
        for (var checkbox of markedCheckbox) {
            if (checkbox.checked)
                design.push(checkbox.value)
        }

        var material = []
        var markedCheckbox = document.getElementsByName('material');
        for (var checkbox of markedCheckbox) {
            if (checkbox.checked)
                material.push(checkbox.value)
        }

        var color = []
        var markedCheckbox = document.getElementsByName('color');
        for (var checkbox of markedCheckbox) {
            if (checkbox.checked)
                color.push(checkbox.value)
        }



        if((maxVal - minVal) < priceGap){
            if(e.target.className === "range-min"){
                rangeInput[0].value = maxVal - priceGap
            }else{
                rangeInput[1].value = minVal + priceGap;
            }
        }else{
            priceInput[0].value = minVal;
            priceInput[1].value = maxVal;
            range.style.left = ((minVal / rangeInput[0].max) * 100) + "%";
            range.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
        }
            data = {
                'order_by': order_by,
                'page': page,
                'catagory': catagory,
                'size': size,
                'design': design,
                'color': color,
                'material': material,
                'product_min_price':minVal,
                'product_max_price':maxVal
            }
            $.ajax({
                  type: 'GET',
                  url: '/product-list/',
                  data: data,
                  dataType: "json",
                     success: function(response){
                        $('#filter_product').html(response.data)
                  }
            });
    });
    });
