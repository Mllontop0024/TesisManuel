var inP     =   $('.input-field');

inP.on('blur', function () {
    if (!this.value) {
        $(this).parent('.f_row').removeClass('focus');
    } else {
        $(this).parent('.f_row').addClass('focus');
    }
}).on('focus', function () {
    $(this).parent('.f_row').addClass('focus');
    $('.btn').removeClass('active');
    $('.f_row').removeClass('shake');
});


$('.resetTag').click(function(e){
    e.preventDefault();
    $('.formBox').addClass('level-forget').removeClass('level-reg');
});

$('.back').click(function(e){
    e.preventDefault();
    $('.formBox').removeClass('level-forget').addClass('level-login');
});



$('.regTag').click(function(e){
    e.preventDefault();
    $('.formBox').removeClass('level-reg-revers');
    $('.formBox').toggleClass('level-login').toggleClass('level-reg');
    if(!$('.formBox').hasClass('level-reg')) {
        $('.formBox').addClass('level-reg-revers');
    }
});
$('.btn').each(function() {
     $(this).on('click', function(e){
        e.preventDefault();
        
        var finp =  $(this).parent('form').find('input');
       
       console.log(finp.html());
       
        if (!finp.val() == 0) {
            $(this).addClass('active');
        }
        
        setTimeout(function () {
            
            inP.val('');
            
            $('.f_row').removeClass('shake focus');
            $('.btn').removeClass('active');
            
        }, 2000);
         
        if(inP.val() == 0) {
            inP.parent('.f_row').addClass('shake');
        }
         
        //inP.val('');
        //$('.f_row').removeClass('focus');
        
    });
});



/**/

$("#btnPagar").click(function(e) {
    e.preventDefault();
    for(var i = 0; i < localStorage.length; i++) {              
      var clave = localStorage.key(i);
      var producto = $.parseJSON(localStorage.getItem(clave));
/*id producto, */

      
    }
    alert(estudianteMayor.nota + " " + estudianteMayor.nombre);
});

/* $("#btnIngresar").click(function (e){
    e.preventDefault();
    var correo = document.getElementById('txtCorreoLogin').value;
    console.log(correo)
    var password = document.getElementById('txtContraseñaLogin').value;
    console.log(password)
    correo = correo.replace(/ /g, "")
    password = password.replace(/ /g, "")
    if (correo == "" || password == "") {
        Swal.fire({
            icon: 'warning',
            title: 'Oops...',
            text: 'Debe completar los campos',
            showConfirmButton: false,
            timer: 1500,
            timerProgressBar: true,
        })
    } else {
        var datos = [];
        var parametros = { 'correoL': correo, 'contrasenaL': password }
        $.ajax({
            data: parametros,
            url: "/logueo",
            type: "POST",
            dataType: "json",
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status + " \n" + xhr.responseText, "\n" + thrownError);
            },
            success: function(response) {
                console.log("bien");
                console.log(response.datosCliente.length);
                if (response.datosCliente.length > 0) {
                    datos[0] = response.datosCliente;
                }
            },
            complete: function() {
                if (datos.length > 0) {
                    const Toast = Swal.mixin({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 2000,
                        timerProgressBar: true,
                        onOpen: (toast) => {
                            toast.addEventListener('mouseenter', Swal.stopTimer)
                            toast.addEventListener('mouseleave', Swal.resumeTimer)
                        }
                    })
                    Toast.fire({
                        icon: 'success',
                        title: 'Acceso correcto'
                    });
                    sessionStorage.setItem(0, JSON.stringify(datos[0]));
                    location.href='/logueo/';
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Usuario o contraseña incorrecto.',
                        showConfirmButton: false,
                        timer: 1500,
                        timerProgressBar: true,
                    })
                }
            }
        })
    }
}); */



function detectarUsuario(){
    if (sessionStorage.getItem(0)!=null){
        var correo=JSON.parse(sessionStorage.getItem(0))
        document.getElementById('correoUsuario').innerHTML +=correo[0];
        document.getElementById('correoContactanos').value +=correo[0];
        document.getElementById('correoCon').value +=correo[0];
        document.getElementById('correoCon1').value +=correo[0];
    }
}

function cerrarSesion() {
    sessionStorage.setItem(0, null);
    location.href = '/'
}

