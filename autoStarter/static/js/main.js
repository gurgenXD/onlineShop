$(function () {
    $('body').css('margin-bottom', $('.footer').outerHeight());
    $('#MapContacts').css('height', ($(window).height() - $('.navbar-light').outerHeight() - $('.navbar-dark').height()));
});

$(".cgi-h .categories-grid-item-img").each(function() {
    $(this).css('height', ($(this).parent('.cgi-h').outerHeight()-$(this).parent('.cgi-h').find('span').outerHeight()));
});

$(function () {
    $(".zoom-image").SmartPhoto();
});

$(document).ready(function DDAni(){
    $('.navbar-light .dropdown').on('show.bs.dropdown', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideDown("fast");
        $(this).toggleClass('open');  
    });

    $('.navbar-light .dropdown').on('hide.bs.dropdown', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideUp("fast");
        $(this).toggleClass('open');  
    });
});

$(document).ready(function(){
    $(".navbar-dark .dropdown").hover(            
        function() {
            $('.dropdown-menu', this).not('.in .dropdown-menu').stop( true, true ).slideDown("fast");
            $(this).toggleClass('open');        
        },
        function() {
            $('.dropdown-menu', this).not('.in .dropdown-menu').stop( true, true ).slideUp("fast");
            $(this).toggleClass('open');       
        }
    );
});

function formatNumber(n) {
    if (n < 0) { throw 'must be non-negative: ' + n; } 
    if (n === 0) { return '0'; }

    var output = [];

    for (; n > 0; n = Math.floor(n/1000)) {
        output.unshift(n % 1000);
    }

    return output.join(' ');
}

$(function () {
    'use strict'
    $('[data-toggle="offcanvas"]').on('click', function () {
        $('.offcanvas-collapse').toggleClass('open')
    })
})

$(function() {
    Stickyfill.add($('.sticky'));
});

$(document).ready(function(){
    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('.scroll-to-top').fadeIn(200);
        } 
        else {
            $('.scroll-to-top').fadeOut(200);
        }
    });
    $('.scroll-to-top').click(function(){
        $('html, body').animate({scrollTop : 0},300);
        return false;
    });
});

$(document).ready(function(){
    $(window).scroll(function(){
        if ($(this).scrollTop() > 20) {
            $('.navbar-light').addClass('navbar-scroll');
        } 
        else {
            $('.navbar-light').removeClass('navbar-scroll');
        }
    });
});

$(function() {
    $('.carousel-item').matchHeight({
        byRow: false
    });
});

$(function() {
    $(".phone-input").mask("+7 (999) 999-99-99");
    $(".time-input").mask("Позвонить в: 99:99");
});

$('.slider-for').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    fade: true,
    asNavFor: '.slider-nav'
});
$('.slider-nav').slick({
    slidesToShow: 5,
    slidesToScroll: 1,
    asNavFor: '.slider-for',
    dots: false,
    centerMode: false,
    focusOnSelect: true,
    arrows: false,
});

$(document).ready(function(){
    $('.count').prop('disabled', true);
    $(document).on('click','.form-add .plus',function(){
        num_count = $(this).parent(".input-group-append").siblings('.count');
		nmb = parseInt(num_count.val());
		if (nmb >= parseInt(num_count.attr('max'))) {
			nmb = parseInt(num_count.attr('max'));
		} else {
			nmb = nmb + 1;
		}
		num_count.val(nmb.toString());
    });
    $(document).on('click','.form-add .minus',function(){
        num_count = $(this).parent(".input-group-prepend").siblings('.count');
        nmb = parseInt(num_count.val());
        if (nmb <= parseInt(num_count.attr('min'))) {
            nmb = parseInt(num_count.attr('min'));
        } else {
            nmb = nmb - 1;
        }
        num_count.val(nmb.toString());
    });

//ADD TO CART
	$('.add-to-cart').click(function(e) {
		e.preventDefault();
        product_id = $(this).attr('data-id');
        qty = $('.count').val()
		data = {
            product_id: product_id,
            qty: qty,
        }
		$.ajax({
			type: "GET",
			url: $('.form-add').attr('action'),
            data: data,
			success: function(data) {
                $('.cart-info').html(data.cart_len + ' | ' + data.total_price.toLocaleString() + '  ₽');
                $('.add-to-cart').css('display','none');
                $('.in-cart').css('display','block');
			}
		});
    });

//REMOVE FROM CART
    $('.remove-from-cart').click(function(e) {
        e.preventDefault();
		product_id = $(this).attr('data-id');
		data = {
			product_id: product_id,
		}
        $.ajax({
        	type: "GET",
        	url: $('.form-remove').attr('action'),
        	data: data,
            success: function(data) {
                $('.total-price').html(data.total_price.toLocaleString());
                $('.cart-info').html(data.cart_len + ' | ' + data.total_price.toLocaleString() + '  ₽');
        		$('.cart-item-' + product_id).css('display','none');
        	}
        });
    });

//CHANGE QUATITY
    $('.form-quantity .minus').click(function() {
        num_count = $(this).parent(".input-group-prepend").siblings('.count');
        nmb = parseInt(num_count.val());
        if (nmb <= parseInt(num_count.attr('min'))) {
            nmb = parseInt(num_count.attr('min'));
        } else {
            nmb = nmb - 1;
        }
        num_count.val(nmb.toString());

        quantity = num_count.val();
        product_id = num_count.attr('data-id');

        console.log(quantity, product_id);

        data = {
            quantity: quantity,
            product_id: product_id,
        }
        $.ajax({
            type: "GET",
            url: $('.form-quantity').attr('action'),
            data: data,
            success: function(data) {
                $('.item-total-price-' + product_id).html(data.cost.toLocaleString());
                $('.total-price').html(data.total_price.toLocaleString());
                $('.cart-info').html(data.cart_len + ' | ' + data.total_price.toLocaleString() + '  ₽');
            }
        });
    });

	$('.form-quantity .plus').click(function() {
		num_count = $(this).parent(".input-group-append").siblings('.count');
		nmb = parseInt(num_count.val());
		if (nmb >= parseInt(num_count.attr('max'))) {
			nmb = parseInt(num_count.attr('max'));
		} else {
			nmb = nmb + 1;
		}
		num_count.val(nmb.toString());

		quantity = num_count.val();
        product_id = num_count.attr('data-id');
        
		data = {
			quantity: quantity,
			product_id: product_id,
		}
		$.ajax({
			type: "GET",
			url: $('.form-quantity').attr('action'),
			data: data,
			success: function(data) {
				$('.item-total-price-' + product_id).html(data.cost.toLocaleString());
                $('.total-price').html(data.total_price.toLocaleString());
                $('.cart-info').html(data.cart_len + ' | ' + data.total_price.toLocaleString() + '  ₽');
			}
		});
    });

	$('.one_click_submit').click(function(e) {
        e.preventDefault();
        product_id = $(this).attr('data-id');
        quantity = $('.count').val();
        user_name = $('#user_name ').val();
        user_phone = $('#user_phone ').val();
        user_comment = $('#user_comment ').val();
        
		data = {
            quantity: quantity,
            product_id: product_id,
            user_comment: user_comment,
            user_name: user_name,
            user_phone: user_phone,
        }

		$.ajax({
			type: "GET",
			url: $('#order_one_click').attr('action'),
			data: data,
			success: function(data) {
                if (data.alert_success) {
                    $('#order_one_click .alert-success').removeClass('d-none');
                    $('#order_one_click .alert-success').addClass('d-block');
                } else {
                    $('#order_one_click .alert-danger').removeClass('d-none');
                    $('#order_one_click .alert-danger').addClass('d-block');
                }
			}
		});
    });
    
	$('#callback-form .callback-submit').click(function(e) {
        e.preventDefault();
        csrf_token = $('#callback-form [name="csrfmiddlewaretoken"]').val();
        phone_number = $('#callback-form .phone-input').val();
        time_to_callback = $('#callback-form .time-input').val();
        
		data = {
            "csrfmiddlewaretoken": csrf_token,
            phone_number: phone_number,
            time_to_callback: time_to_callback,
        }

		$.ajax({
			type: "POST",
			url: $('#callback-form').attr('action'),
			data: data,
			success: function(data) {
                if (data.alert_success) {
                    $('#callback-form .alert-success').removeClass('d-none');
                    $('#callback-form .alert-success').addClass('d-block');
                } else {
                    $('#callback-form .alert-danger').removeClass('d-none');
                    $('#callback-form .alert-danger').addClass('d-block');
                }
			}
		});
    });

	$('#feedback-form .feedback-submit').click(function(e) {
        e.preventDefault();
        csrf_token = $('#feedback-form [name="csrfmiddlewaretoken"]').val();
        phone_or_email = $('#feedback-form .phone_or_email').val();
        name = $('#feedback-form .sub_name').val();
        message = $('#feedback-form .sub_message').val();
        recaptcha_response = $('#feedback-form [name="g-recaptcha-response"]').val();
        
		data = {
            "csrfmiddlewaretoken": csrf_token,
            phone_or_email: phone_or_email,
            name: name,
            message: message,
            'g-recaptcha-response': recaptcha_response,
        }

		$.ajax({
			type: "POST",
			url: $('#feedback-form').attr('action'),
			data: data,
			success: function(data) {
                if (data.alert_success) {
                    $('#feedback-form .alert-success').removeClass('d-none');
                    $('#feedback-form .alert-success').addClass('d-block');
                }
                else {
                    $('#feedback-form .alert-danger').removeClass('d-none');
                    $('#feedback-form .alert-danger').addClass('d-block');
                }
			}
		});
    });
    
	$('#sort-products').change(function() {
        $('#cars-filter').submit();
    });
    
	$('#cars-brand').change(function() {
        $('#cars-filter').submit();
    });
    
	$('#cars-name').change(function() {
        $('#cars-filter').submit();
    });
    
	$('#cars-date').change(function() {
        $('#cars-filter').submit();
    });
    
    $('.val_price').on('blur', function() {
        $('#cars-filter').submit();
    });
    
    $('.manufacturer').change(function() {
        $('#cars-filter').submit();
    });
});