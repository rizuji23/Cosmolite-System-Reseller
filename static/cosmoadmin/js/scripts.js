$('.btnedit').click(function () {
    id = $(this).attr('id')
    $('#dataproduk').val(id)
})

function deletebarang(ids) {
    csrf = $("[name='csrfmiddlewaretoken']").val();
    Swal.fire({
        title: 'Apakah anda yakin??',
        text: "Data ini tidak akan bisa dikembalikan!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Iya'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: '/cosmoadmin/detelebarang/',
                data: {
                    'id': ids,
                    'csrfmiddlewaretoken': csrf
                },
                method: 'POST',
                success: function (data) {
                    Swal.fire(
                        'Deleted!',
                        'Your file has been deleted.',
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

$(document).ready(function () {
    harga = $('.hargabarang').text()
    var hg = harga.replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1.");
    $('.hargabarang').text('Rp. ' + hg)
})

function detailbarang(id) {
    csrf = $("[name='csrfmiddlewaretoken']").val();
    $.ajax({
        url: '/cosmoadmin/detailbarang/',
        data: {
            'id': id,
            'csrfmiddlewaretoken': csrf
        },
        method: 'POST',
        success: function (data) {
            $('#detaildatabarang').html(data.datas);
            $('#detailbarang').modal('show')
        }
    })
}

$('.btneditkategori').click(function () {
    produk = $(this).attr('id')
    csrf = $("[name='csrfmiddlewaretoken']").val();
    $.ajax({
        url: '/cosmoadmin/getkategori/',
        data: {
            'id': produk,
            'csrfmiddlewaretoken': csrf
        },
        method: 'POST',
        success: function (data) {
            $('#modaleditk').html(data.datas);
            $('#modaleditkategori').modal('show')
        }
    })
})



$('.btneditsubkategori').click(function () {
    produk = $(this).attr('id')
    csrf = $("[name='csrfmiddlewaretoken']").val();
    $.ajax({
        url: '/cosmoadmin/getsubkategori/',
        data: {
            'id': produk,
            'csrfmiddlewaretoken': csrf
        },
        method: 'POST',
        success: function (data) {
            $('#modaleditsk').html(data.datas);
            $('#modaleditsubkategori').modal('show')
        }
    })
})

$('.btndeletekategori').click(function () {
    kategori = $(this).attr('id')
    csrf = $("[name='csrfmiddlewaretoken']").val();
    Swal.fire({
        title: 'Apakah anda yakin??',
        text: "Data ini tidak akan bisa dikembalikan!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Iya'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: '/cosmoadmin/deletekategori/',
                data: {
                    'id': kategori,
                    'csrfmiddlewaretoken': csrf
                },
                method: 'POST',
                success: function (data) {
                    Swal.fire(
                        'Deleted!',
                        'Your file has been deleted.',
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
})

$('.btndeletesubkategori').click(function () {
    subkategori = $(this).attr('id')
    csrf = $("[name='csrfmiddlewaretoken']").val();
    Swal.fire({
        title: 'Apakah anda yakin??',
        text: "Data ini tidak akan bisa dikembalikan!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Iya'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: '/cosmoadmin/deletesubkategori/',
                data: {
                    'id': subkategori,
                    'csrfmiddlewaretoken': csrf
                },
                method: 'POST',
                success: function (data) {
                    Swal.fire(
                        'Deleted!',
                        'Your file has been deleted.',
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
})