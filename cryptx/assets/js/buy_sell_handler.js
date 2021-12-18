

$(document).ready(()=>{
    
    $("#buy_quantity").on('keyup',(e)=>{

        let qty = document.getElementById("buy_quantity").value;
        qty=parseFloat(qty);
        
        let total_price = (current_price*qty).toFixed(2);
        margin_required = document.getElementById("margin_required")
        console.log(margin_required.type)
        margin_required.innerHTML=total_price;
    
    })

    $("#sell_quantity").on('keyup',(e)=>{

        let qty = document.getElementById("sell_quantity").value;
        qty=parseFloat(qty);
        
        let total_price = (current_price*qty).toFixed(2);
        //TODO  :replace total_price with quantity of coins 
        document.getElementById("sell_price").value=total_price;
    
    })


    $("#buy_form").on('submit',(e)=>{
        e.preventDefault();

        let form = $("#buy_form");
        let url = "/orders/handle_buy/";

        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            success: function (data) {
                alert(data.msg);
            },
            error: function (data) {
                alert('An error occurred.');
            },
        });
    })
    $("#sell_form").on('submit',(e)=>{
        e.preventDefault();

        let form = $("#sell_form");
        let url = "/orders/handle_sell/";

        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            success: function (data) {
                alert(data.msg);
            },
            error: function (data) {
                alert('An error occurred.');
            },
        });
    })
    

})