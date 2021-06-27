$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})


$('.plus-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var elm = this.parentNode.children[2] 
    console.log(id)
    $.ajax({
        type : "GET",
        url : "/pluscart",
        data : {prod_id : id},
        success : function(data){
            elm.innerHTML = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total_amount').innerText = data.totalamount 
            console.log(data)
            console.log("Success")
        }
    })
})


$('.minus-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var elm = this.parentNode.children[2] 
    console.log(id)
    $.ajax({
        type : "GET",
        url : "/minuscart",
        data : {prod_id : id},
        success : function(data){
            elm.innerHTML = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total_amount').innerText = data.totalamount 
            console.log(data)
            console.log("Success")
        }
    })
})


$('.remove-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var elm = this
    console.log(id)
    $.ajax({
        type : "GET",
        url : "/removecart",
        data : {prod_id : id},
        success : function(data){ 
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total_amount').innerText = data.totalamount 
            elm.parentNode.parentNode.parentNode.parentNode.remove()
            console.log(data)
            console.log("Success")
        }
    })
})

