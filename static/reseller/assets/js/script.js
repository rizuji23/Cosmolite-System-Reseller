var delay = 5000;
var $element = $(".bandage-keranjang");
var $element1 = $(".belanja-produk-animate");

setInterval(function () {
	$element.removeClass("animate__shakeY");
	setTimeout(function () {
		$element.addClass("animate__shakeY");
	})
}, delay);

setInterval(function () {
	$element1.removeClass("animate__shakeX");
	setTimeout(function () {
		$element1.addClass("animate__shakeX");
	})
}, delay);


$("#checkAll").click(function () {
	$('input:checkbox').not(this).prop('checked', this.checked);
});

$("input#jk").on('click', function () {
	var $box = $(this);
	if ($box.is(":checked")) {
		var group = "input#jk[name='" + $box.attr("name") + "']";
		$(group).prop("checked", false);
		$box.prop("checked", true);
	} else {
		$box.prop("checked", false);
	}
});

$("input#radio").on('click', function () {
	var $box1 = $(this);
	if ($box1.is(":checked")) {
		var group = "input#radio[name='" + $box1.attr("name") + "']";
		$(group).prop("checked", false);
		$box1.prop("checked", true);
	} else {
		$box1.prop("checked", false);
	}
});

$('a.btn-tambah, .btn-kurang').click(function (e) {
	e.preventDefault();
});

$('.btn-tambah').click(function () {
	$('.input-total').val(function (i, val) {
		return +val + 1
	});
})

$('.btn-kurang').click(function () {
	$('.input-total').val(function (i, val) {
		return +val - 1
	});
})


$('.owl-carousel').owlCarousel({
	center: true,
	items: 2,
	loop: true,
	margin: 10,
	autoplay: true,
	autoplayTimeout: 3000,
	responsive: {
		0: {
			items: 1
		},
		768: {
			items: 2
		}
	}
})


var lst = 0;
nb = document.getElementById("navbar");
window.addEventListener("scroll", function () {
	var st = window.pageYOffset || document.documentElement.st;
	if (st > lst) {
		nb.style.top = "-100px";
	} else {
		nb.style.top = "0px";
	}
	lst = st;
})


function googleTranslateElementInit() {
	new google.translate.TranslateElement({
			pageLanguage: 'en'
		},
		'google_translate_element'
	);
}

$('.section-6-main a').click(function () {
	var lang = $(this).data('lang');
	var $frame = $('.goog-te-menu-frame:first');

	if (!$frame.size()) {
		alert("Error: Could not find Google translate frame.");
		return false;
	}
	$frame.contents().find('.goog-te-menu2-item span.text:contains(' + lang + ')').get(0).click();
	return false;
});

function openNav() {
	document.getElementById("mySidenav").style.width = "100%";
}

function closeNav() {
	document.getElementById("mySidenav").style.width = "0";
}

function openFilter() {
	document.getElementById("myFilter").style.height = "100%";
}

function closeFilter() {
	document.getElementById("myFilter").style.height = "0";
}

//start update

function provinsi() {
	$.ajax({
		url: 'https://dev.farizdotid.com/api/daerahindonesia/provinsi',
		dataType: 'json',
		success: function (data) {
			let provin = data.provinsi

			$.each(provin, function (i, result) {
				$('#provinsi').append(`<option value="${result.id}">${result.nama}</option>`)
			})
		}
	})
}

$(document).ready(function () {
	$('.carousel .carousel-item').first().addClass('active')

	provinsi()

	$('#provinsi').change(function () {
		var id_pro = $(this).val()

		$.ajax({
			url: 'https://dev.farizdotid.com/api/daerahindonesia/kota',
			data: {
				'id_provinsi': id_pro
			},
			dataType: 'json',
			success: function (data) {
				let kotakab = data.kota_kabupaten
				$.each(kotakab, function (i, result) {
					$('#kotakab').append(`<option value="${result.id}">${result.nama}</option>`)
				})
			}
		})
	})

	$('#kotakab').change(function () {
		var id_kotkab = $(this).val()

		$.ajax({
			url: 'https://dev.farizdotid.com/api/daerahindonesia/kecamatan',
			data: {
				'id_kota': id_kotkab
			},
			dataType: 'json',
			success: function (data) {
				let kecamatan = data.kecamatan
				$.each(kecamatan, function (i, result) {
					$('#kecamatan').append(`<option value="${result.id}">${result.nama}</option>`)
				})
			}
		})
	})

	$('#kecamatan').change(function () {
		var id_kec = $(this).val()

		$.ajax({
			url: 'https://dev.farizdotid.com/api/daerahindonesia/kelurahan',
			data: {
				'id_kecamatan': id_kec
			},
			dataType: 'json',
			success: function (data) {
				let kelurahan = data.kelurahan
				$.each(kelurahan, function (i, result) {
					$('#kelurahan').append(`<option value="${result.id}">${result.nama}</option>`)
				})
			}
		})
	})

	$('.btnshare').click(function () {
		ids = $(this).attr('id')
		data = "http://localhost:8000/share/" + ids
		$('.links').text(data)

		$('#sharelink').modal('show')
	})

})

$('#tambahalamat').click(function () {
	label = $('#label').val()
	provinsi = $('select#provinsi option:selected').text()
	kotakab = $('select#kotakab option:selected').text()
	kecamatan = $('select#kecamatan option:selected').text()
	kelurahan = $('select#kelurahan option:selected').text()
	kodepos = $('#kodepos').val()
	alamat_lengkap = $('#alamat_lengkap').val()
	csrf = $("[name='csrfmiddlewaretoken']").val();

	console.log(kotakab)

	$.ajax({
		url: '/addalamat/',
		data: {
			'label': label,
			'provinsi': provinsi,
			'kotakab': kotakab,
			'kecamatan': kecamatan,
			'kelurahan': kelurahan,
			'kodepos': kodepos,
			'alamat_lengkap': alamat_lengkap,
			'csrfmiddlewaretoken': csrf
		},
		method: 'POST',
		success: function (data) {
			if (data) {
				$('.ale').html(`
				<div class="alert alert-success" role="alert">
				Alamat sudah ditambah...
			  </div>
				`)

				$('#tambahAlamat').modal('toggle');

			} else {
				$('.ale').html(`
				<div class="alert alert-danger" role="alert">
				Alamat gagal ditambah!!
				</div>
				`)

				$('#tambahAlamat').modal('toggle');

			}
		}
	})
})


$(document).ready(function () {
	harga = $('#hargas').text()
	var hg = harga.replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1.");
	$('#hargas').text('Rp. ' + hg)

	$('#qty').val($('.qtys').val())

	hitungtotal($('.qtys').val())

	$('.btnminus').click(function () {
		var $input = $('.qtys').val();
		var count = parseInt($('.qtys').val()) - 1;
		count = count < 3 ? 3 : count;
		$('.qtys').val(count);
		$('.qtys').change();
		$('#qty').val(count);
		$('#qty').change();
		hitungtotal(count)
		return false;
	});
	$('.btnplus').click(function () {
		var $input = $('.qtys').val();
		$('.qtys').val(parseInt($('.qtys').val()) + 1);
		$('#qty').val(parseInt($('.qtys').val()) + 1);
		$('#qty').change();
		$('.qtys').change();
		hitungtotal(parseInt($('.qtys').val()) + 1)
		return false;

	});

	function hitungtotal(count) {
		var harga = $("#harga_produks").val()
		var qty = count
		var kurir = $('.ongkir').val()
		var total = parseInt(harga) * parseInt(qty)
		var total2 = total.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1.")
		var total3 = $('.total2').val(total)
		$('.total2').val(total)
		$('#totals').text("Rp " + total2)

	}

	function kurirtotal(ongkirs) {
		var total = $('.total2').val()
		var to = parseInt(total) + parseInt(ongkirs)
		var total2 = to.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1.");
		$('.total2').val(to)
		$('#totals').text("Rp " + total2)
		console.log(to)
	}

	$('.btnalamat').click(function () {
		ids = $(this).attr('id')
		$('#alamat').val(ids)
		$('#dikirim').text($('.label').text())
		$('#listAlamat').modal('hide');
	})

	$('.btnbank').click(function () {
		ids = $(this).attr('id')

		$('#pembayaran').val(ids)
		$('#pembayaran2').text($('.nama_bank').text())
		$('#listBank').modal('hide');
	})

	$('.btnkurir').click(function () {
		ids = $(this).attr('id')
		$('#pengiriman2').text($('.nama_kurir').text())
		$('#pengiriman').val(ids)
		kurirtotal($('.ongkir').val())
		$('#listKurir').modal('hide');
	})


})


function sudahTiba(ids) {
	csrf = $("[name='csrfmiddlewaretoken']").val();
	Swal.fire({
		title: 'Apakah anda yakin??',
		text: "Pastikan barang sudah sampai dengan benar",
		icon: 'info',
		showCancelButton: true,
		confirmButtonColor: '#3085d6',
		cancelButtonColor: '#d33',
		confirmButtonText: 'Iya'
	}).then((result) => {
		if (result.isConfirmed) {
			$.ajax({
				url: '/sudahtiba/',
				data: {
					'id': ids,
					'csrfmiddlewaretoken': csrf
				},
				method: 'POST',
				success: function (data) {
					Swal.fire(
						'Sudah Tiba!',
						'Silahkan berjualan dan menangkan komisi keuntungan',
						'success'
					).then((result) => {
						if (result.isConfirmed) {
							location.reload()
						}
					})
				}
			})
		}
	})
}